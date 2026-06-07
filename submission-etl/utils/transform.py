import pandas as pd


EXCHANGE_RATE = 16000


def transform_to_dataframe(data):
    """
    Mengubah hasil scraping menjadi DataFrame.
    """
    return pd.DataFrame(data)


def transform_data(df):
    """
    Membersihkan dan mentransformasi data sesuai rubric Dicoding.
    """

    try:

        if df.empty:
            return pd.DataFrame()

        df = df.copy()

        # ==================================================
        # HAPUS DATA INVALID
        # ==================================================

        df = df[df["Title"] != "Unknown Product"]

        df = df[df["Price"] != "Price Unavailable"]

        df = df[~df["Rating"].str.contains(
            "Invalid Rating",
            na=False
        )]

        df = df[~df["Rating"].str.contains(
            "Not Rated",
            na=False
        )]

        # ==================================================
        # PRICE
        # "$102.15" -> 1634400.0
        # ==================================================

        df["Price"] = (
            df["Price"]
            .str.replace("$", "", regex=False)
            .astype(float)
            * EXCHANGE_RATE
        )

        # ==================================================
        # RATING
        # "Rating: ⭐ 4.8 / 5" -> 4.8
        # ==================================================

        df["Rating"] = (
            df["Rating"]
            .str.extract(r"(\d+\.\d+)")
            .astype(float)
        )

        # ==================================================
        # COLORS
        # "3 Colors" -> 3
        # ==================================================

        df["Colors"] = (
            df["Colors"]
            .str.extract(r"(\d+)")
            .astype(int)
        )

        # ==================================================
        # SIZE
        # "Size: M" -> "M"
        # ==================================================

        df["Size"] = (
            df["Size"]
            .str.replace("Size:", "", regex=False)
            .str.strip()
        )

        # ==================================================
        # GENDER
        # "Gender: Men" -> "Men"
        # ==================================================

        df["Gender"] = (
            df["Gender"]
            .str.replace("Gender:", "", regex=False)
            .str.strip()
        )

        # ==================================================
        # HAPUS NULL & DUPLIKAT
        # ==================================================

        df.dropna(inplace=True)

        df.drop_duplicates(inplace=True)

        # ==================================================
        # TIPE DATA SESUAI RUBRIC
        # ==================================================

        df["Title"] = df["Title"].astype("string")

        df["Price"] = df["Price"].astype(float)

        df["Rating"] = df["Rating"].astype(float)

        df["Colors"] = df["Colors"].astype(int)

        df["Size"] = df["Size"].astype("string")

        df["Gender"] = df["Gender"].astype("string")

        df["timestamp"] = pd.to_datetime(
            df["timestamp"]
        )

        print(f"Total clean data: {len(df)}")

        return df

    except Exception as e:

        print(f"Transform error: {e}")

        return pd.DataFrame()