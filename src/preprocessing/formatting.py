import pandas as pd


class FeatureFormatter:
    def __init__(self, df: pd.DataFrame):
        self.df = df.copy()

    def split_blood_pressure(self):
        if "blood_pressure" in self.df.columns:
            bp = self.df["blood_pressure"].str.split("/", expand=True)
            self.df["systolic"] = bp[0].astype(int)
            self.df["diastolic"] = bp[1].astype(int)
            self.df.drop(columns=["blood_pressure"], inplace=True)
        return self.df

    def format(self):
        self.split_blood_pressure()
        return self.df
