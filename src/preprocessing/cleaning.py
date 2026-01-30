import pandas as pd


class DataCleaner:
    def __init__(self, df: pd.DataFrame):
        self.df = df.copy()

    def standardize_columns(self):
        self.df.columns = (
            self.df.columns.str.strip()
                            .str.lower()
                            .str.replace(" ", "_")
        )
        return self.df

    def handle_missing(self):
        # Sleep disorder has many nulls → fill as "None"
        if "sleep_disorder" in self.df.columns:
            self.df["sleep_disorder"] = self.df["sleep_disorder"].fillna("None")
        return self.df

    def drop_unnecessary(self):
        if "person_id" in self.df.columns:
            self.df.drop(columns=["person_id"], inplace=True)
        return self.df

    def clean(self):
        self.standardize_columns()
        self.handle_missing()
        self.drop_unnecessary()
        return self.df
