import pandas as pd
import numpy as np

def set_dataframe(dir, include_optimen_hours=True, data_prepared=False):
    df = pd.read_csv(dir)
    if not data_prepared:
        df = df.iloc[:,[0,3,5,6,7,8,9]]
        df = add_duration(df)
    df = df.astype({
        'Date': 'datetime64[ns]',
    })
    df = add_month_column(df)

    if not include_optimen_hours:
        df = df[df['Customer'] !='OPTIMEN (OPT)']

    return df

def add_duration(df):
    df["Duration_minutes"] = np.where(df["Duration"].str[-2:] == '30',0.5,0.0)
    df["Duration_hours"] = df["Duration"].str.extract('(\d+)').astype(float)
    df["Duration"] = df["Duration_hours"] + df["Duration_minutes"]
    df.drop(columns=["Duration_minutes", "Duration_hours"], inplace=True)
    return df

def add_month_column(df):
    df['Month'] = df['Date'].dt.month_name()
    df['Month_int'] = df['Date'].dt.month
    month_order = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
    df['Month'] = pd.Categorical(df['Month'], categories=month_order, ordered=True)
    return df

def group_by_customer(df):
    group_customer = df.groupby('Customer')['Duration'].sum().reset_index()
    group_customer["Percentage"] = (group_customer["Duration"]/group_customer["Duration"].sum() * 100).round(2)
    group_customer["Percentage"] = group_customer["Percentage"].apply(lambda x: str(x) + '%')
    group_customer.set_index("Customer", inplace=True)
    return group_customer

def get_customers_available(df):
    return df["Customer"].unique()

def get_years_available(df):
    return df["Date"].dt.year.unique()