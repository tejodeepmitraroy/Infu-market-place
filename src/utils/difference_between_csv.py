import pandas as pd
import os


def difference_between_csv(
    first_csv_filepath: str,
    second_csv_filepath: str,
    first_column: str = "",
    second_column: str = "",
):
    if not os.path.exists(first_csv_filepath):
        print(f"File not found: {first_csv_filepath}")
        return None

    if not os.path.exists(second_csv_filepath):
        print(f"File not found: {second_csv_filepath}")
        return None

    first_df = pd.read_csv(first_csv_filepath)
    second_df = pd.read_csv(second_csv_filepath)

    # Convert the 'C' columns to sets
    set1 = set(first_df[first_column])
    set2 = set(second_df[second_column])

    unique_to_df1 = set1 - set2

    df_unique_to_first_df = first_df[first_df[first_column].isin(unique_to_df1)]

    # print(df_unique_to_first_df)

    return df_unique_to_first_df[first_column].tolist()
