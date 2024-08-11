import pandas as pd
import os


def csvCreator(data: list[any], schema: list[str], csv_filepath: str):

    if os.path.exists(csv_filepath):

        df_existing = pd.read_csv(csv_filepath)
    else:

        df_existing = pd.DataFrame(columns=schema)

    new_data = pd.json_normalize(data)

    new_data = new_data.reindex(columns=schema)

    new_data = new_data.dropna(how="all")

    if not new_data.empty:
        df_combined = pd.concat([new_data, df_existing]).drop_duplicates(
            subset=[schema[0]]
        )

        df_combined.to_csv(csv_filepath, index=False)
        print("CSV file created successfully.")
