import pandas as pd


def add_row_to_df(row, df):
    row = pd.Series(row, index= df.columns.to_list())
    return df.append(row, ignore_index=True)
