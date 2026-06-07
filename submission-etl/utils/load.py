from sqlalchemy import create_engine


def store_to_csv(df, filename="products.csv"):
    """
    Menyimpan DataFrame ke CSV.
    """

    try:

        if df is None or df.empty:
            print("Data kosong, CSV tidak dibuat.")
            return False

        df.to_csv(
            filename,
            index=False
        )

        print(f"CSV berhasil disimpan: {filename}")

        return True

    except Exception as e:

        print(f"CSV error: {e}")

        return False


def store_to_postgresql(df, db_url):
    """
    Optional:
    Menyimpan data ke PostgreSQL.
    Tidak digunakan untuk target Basic (10/12),
    tetapi boleh disiapkan.
    """

    try:

        if df is None or df.empty:
            print("Data kosong.")
            return False

        engine = create_engine(db_url)

        with engine.connect() as connection:

            df.to_sql(
                name="fashion_products",
                con=connection,
                if_exists="replace",
                index=False
            )

        print("Data berhasil disimpan ke PostgreSQL.")

        return True

    except Exception as e:

        print(f"PostgreSQL error: {e}")

        return False

import gspread
from google.oauth2.service_account import Credentials


def store_to_google_sheets(
    df,
    spreadsheet_name,
    credential_file="google-sheets-api.json"
):
    try:
        scopes = [
            "https://www.googleapis.com/auth/spreadsheets",
            "https://www.googleapis.com/auth/drive"
        ]

        creds = Credentials.from_service_account_file(
            credential_file,
            scopes=scopes
        )

        client = gspread.authorize(creds)

        spreadsheet = client.open(spreadsheet_name)

        worksheet = spreadsheet.sheet1

        worksheet.clear()

        df_copy = df.copy()

        for col in df_copy.columns:
            if "time" in col.lower():
                df_copy[col] = df_copy[col].astype(str)

        worksheet.update(
            [df_copy.columns.tolist()]
            + df_copy.values.tolist()
        )

        print("Google Sheets berhasil disimpan.")

        return True

    except Exception as e:
        print(f"Google Sheets error: {e}")
        return False