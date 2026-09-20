import pandas as pd
from src.extract import extract_customers, extract_orders

def transform_customers(df):
    df = df.copy()

    #Convert total_belanja menjadi numeric
    #Nilai yang tidak valid akan menjadi NaN
    df["total_belanja"] = pd.to_numeric(
        df["total_belanja"],
        errors="coerce"
    )

    #Isi kota yang kosong
    df["kota"] = df["kota"].fillna("Unknown")

    #Convert updated_at menjadi datetime
    df["updated_at"] = pd.to_datetime(
        df["updated_at"],
        errors="coerce"
    )

    return df

def transform_orders(df):
    df = df.copy()

    df["amount"] = pd.to_numeric(
        df["amount"],
        errors="coerce"
    )

    df["updated_at"] = pd.to_datetime(
        df["updated_at"]
    )

    return df

def main():
    customers = extract_customers()
    orders = extract_orders()

    customers = transform_customers(customers)
    orders = transform_orders(orders)

    print("TRANSFORMED CUSTOMERS")
    print(customers)
    print("\n")

    print("TRANSFORMED ORDERS")
    print(orders)


if __name__ == "__main__":
    main()