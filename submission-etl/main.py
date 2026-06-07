from utils.extract import scrape_products
from utils.transform import (
    transform_to_dataframe,
    transform_data
)
from utils.load import (
    store_to_csv,
    store_to_google_sheets
)


def main():
    """
    Menjalankan seluruh proses ETL:
    Extract -> Transform -> Load
    """

    print("=" * 50)
    print("MEMULAI ETL PIPELINE")
    print("=" * 50)

    # =====================================
    # EXTRACT
    # =====================================
    print("\n[1] Extracting data...")

    raw_data = scrape_products()

    if not raw_data:
        print("Tidak ada data yang berhasil diambil.")
        return

    print(f"Raw data berhasil diambil: {len(raw_data)}")

    # =====================================
    # TRANSFORM
    # =====================================
    print("\n[2] Transforming data...")

    df = transform_to_dataframe(raw_data)

    clean_df = transform_data(df)

    if clean_df.empty:
        print("Data kosong setelah transformasi.")
        return

    print(f"Clean data: {len(clean_df)}")

    # =====================================
    # LOAD
    # =====================================
    print("\n[3] Saving CSV...")

    success = store_to_csv(
        clean_df,
        "products.csv"
    )

    if success:
        print("ETL Pipeline selesai.")
    else:
        print("Gagal menyimpan CSV.")

    # =====================================
    # LOAD GOOGLE SHEETS
    # =====================================
    print("\n[4] Saving Google Sheets...")

    sheet_success = store_to_google_sheets(
        clean_df,
        "etl"
    )

    if sheet_success:
        print("Google Sheets berhasil diperbarui.")
    else:
        print("Gagal menyimpan ke Google Sheets.")

    print("\nETL Pipeline selesai.")


if __name__ == "__main__":
    main()