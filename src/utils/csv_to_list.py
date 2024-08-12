import pandas as pd
import os

def csv_to_list(
    csv_filepath: str,
    column: str = "",
):
    if not os.path.exists(csv_filepath):
        print(f"File not found: {csv_filepath}")
        return None

    df = pd.read_csv(csv_filepath)

    return df[column].tolist()

    # if column != "":
    #     return df[column].tolist()
    # else:
    #     return df.values.tolist()
