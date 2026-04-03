import pandas as pd
from io import BytesIO
from fastapi import UploadFile
from database import get_connection
from utils.data_cleaning import clean_products_dataframe


async def import_products_from_excel(file: UploadFile):



    if not file.filename.endswith((".xlsx", ".xls")):
        raise ValueError("Only Excel files are allowed (.xlsx or .xls).")


    contents = await file.read()

    try:
        df = pd.read_excel(BytesIO(contents))
    except Exception:
        raise ValueError("Failed to read Excel file. Make sure it is a valid Excel document.")


    cleaned_df = clean_products_dataframe(df)


    if cleaned_df.empty:
        raise ValueError("No valid rows found after cleaning the uploaded file.")

    conn = get_connection()
    cur = conn.cursor()

    inserted_count = 0
    skipped_rows = []

    try:

        for index, row in cleaned_df.iterrows():

            cur.execute(
                "SELECT id FROM suppliers WHERE id = %s",
                (row["supplier_id"],)
            )
            supplier = cur.fetchone()

            if not supplier:
                skipped_rows.append({
                    "row_number": int(index) + 2,  # +2 because Excel starts at row 2 after headers
                    "reason": f"Supplier ID {row['supplier_id']} does not exist."
                })
                continue


            cur.execute(
                "SELECT id FROM products WHERE LOWER(name) = LOWER(%s)",
                (row["name"],)
            )
            existing_product = cur.fetchone()

            if existing_product:
                skipped_rows.append({
                    "row_number": int(index) + 2,
                    "reason": f"Product '{row['name']}' already exists."
                })
                continue


            cur.execute(
                """
                INSERT INTO products (name, description, price, stock_quantity, supplier_id)
                VALUES (%s, %s, %s, %s, %s)
                """,
                (
                    row["name"],
                    row["description"],
                    row["price"],
                    row["stock_quantity"],
                    row["supplier_id"]
                )
            )

            inserted_count += 1

        conn.commit()

    except Exception:
        conn.rollback()
        raise

    finally:
        cur.close()
        conn.close()

    return {
        "message": "Import completed.",
        "rows_received": int(len(df)),
        "valid_rows_after_cleaning": int(len(cleaned_df)),
        "rows_inserted": inserted_count,
        "rows_skipped": len(skipped_rows),
        "skipped_details": skipped_rows
    }