import pandas as pd

def read_excel_file(file_path, sheet_name, skiprows, header_rows):
    sheet_df = pd.read_excel(
        file_path,
        sheet_name=sheet_name,
        skiprows=skiprows,
        header=header_rows,
    )

    if "Unnamed: 0" in sheet_df.columns:
        sheet_df.drop(columns=["Unnamed: 0"], inplace=True)

    sheet_df = sheet_df.fillna("")
    sheet_df = sheet_df.drop_duplicates()
    return sheet_df.dropna()