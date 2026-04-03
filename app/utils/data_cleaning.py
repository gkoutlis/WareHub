import pandas as pd

REQUIRED_COLUMNS = ["name", "description", "price", "stock_quantity", "supplier_id"]


def clean_products_dataframe(df: pd.DataFrame) -> pd.DataFrame:

    df.columns = [str(col).strip().lower() for col in df.columns]

    missing_columns = [col for col in REQUIRED_COLUMNS if col not in df.columns]
    if missing_columns:
        raise ValueError(f"Missing required columns: {missing_columns}")

    df = df[REQUIRED_COLUMNS].copy()

    df = df.dropna(how="all")

    df["name"] = df["name"].astype(str).str.strip()
    df["description"] = df["description"].astype(str).str.strip()

    df["name"] = df["name"].replace(["", "nan", "None"], pd.NA)
    df["description"] = df["description"].replace(["nan", "None"], "")

    df["price"] = pd.to_numeric(df["price"], errors="coerce")
    df["stock_quantity"] = pd.to_numeric(df["stock_quantity"], errors="coerce")
    df["supplier_id"] = pd.to_numeric(df["supplier_id"], errors="coerce")

    df = df.dropna(subset=["name", "price", "stock_quantity", "supplier_id"])

    df = df[df["price"] >= 0]
    df = df[df["stock_quantity"] >= 0]
    df = df[df["supplier_id"] > 0]

    df["stock_quantity"] = df["stock_quantity"].astype(int)
    df["supplier_id"] = df["supplier_id"].astype(int)

    df["price"] = df["price"].round(2)

    return df
