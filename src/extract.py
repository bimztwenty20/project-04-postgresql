import pandas as pd

CUSTOMERS_PATH = "data/raw/customers.csv"
ORDERS_PATH = "data/raw/orders.csv"


def extract_customers():
    return pd.read_csv(CUSTOMERS_PATH)


def extract_orders():
    return pd.read_csv(ORDERS_PATH)


def extract_incremental_customers(last_successful_run):
    df = pd.read_csv(CUSTOMERS_PATH)

    df["updated_at"] = pd.to_datetime(
        df["updated_at"]
    )

    if last_successful_run is None:
        return df

    return df[
        df["updated_at"] > last_successful_run
    ]


def extract_incremental_orders(last_successful_run):
    df = pd.read_csv(ORDERS_PATH)

    df["updated_at"] = pd.to_datetime(
        df["updated_at"]
    )

    if last_successful_run is None:
        return df

    return df[
        df["updated_at"] > last_successful_run
    ]
