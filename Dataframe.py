import pandas as pd
import numpy as np

class Dataframe():
    def __init__(self, dir, data_prepared=False):
        self.dir = dir
        self.data_prepared = data_prepared
        self.df = pd.read_csv(dir)
        self._prepare_dataframe()

    def _prepare_dataframe(self):
        if not self.data_prepared:
            self.df = self.df.iloc[:, [0, 3, 5, 6, 7, 8, 9]]
            self.df = self.add_duration(self.df)
        self.df = self.df.astype({'Date': 'datetime64[ns]'})
        self.df = self.add_month_column(self.df)

    def add_duration(self, df):
        df["Duration_minutes"] = np.where(df["Duration"].str[-2:] == '30', 0.5, 0.0)
        df["Duration_hours"] = df["Duration"].str.extract('(\d+)').astype(float)
        df["Duration"] = df["Duration_hours"] + df["Duration_minutes"]
        df.drop(columns=["Duration_minutes", "Duration_hours"], inplace=True)
        return df

    def add_month_column(self, df):
        df['Month'] = df['Date'].dt.month_name()
        df['Month_int'] = df['Date'].dt.month
        month_order = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
        df['Month'] = pd.Categorical(df['Month'], categories=month_order, ordered=True)
        return df

    def group_by_customer(self):
        group_customer = self.df.groupby('Customer')['Duration'].sum().reset_index()
        group_customer["Percentage"] = (group_customer["Duration"] / group_customer["Duration"].sum() * 100).round(2)
        group_customer["Percentage"] = group_customer["Percentage"].apply(lambda x: str(x) + '%')
        group_customer.set_index("Customer", inplace=True)
        return group_customer

    def get_customers_available(self):
        return self.df["Customer"].unique()

    def get_years_available(self):
        return self.df["Date"].dt.year.unique()
    
def filter_by_year(df,years):
    df_list = []
    for year in years:
        df_year = df[df['Date'].dt.year == year]
        df_list.append(df_year)
    return pd.concat(df_list)

def filter_by_date(df,start, end):
    if end is not None:
        return df[(start <= df["Date"]) & (df["Date"]<= end)]
    else:
        return df[start <= df["Date"]]

def filter_by_customer(df, customers):
    df_list = []
    for customer in customers:
        df_customer = df[df['Customer'] == customer]
        df_list.append(df_customer)
    return pd.concat(df_list)