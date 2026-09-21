import pandas as pd

from src.transform import transform_customers, transform_orders

def test_transform_customers_fills_empty_city():
    df = pd.DataFrame({
    "id": [1],
    "nama": ["Andi"],
    "umur": [25],
    "kota": [None],
    "total_belanja": ["175000"],
    "updated_at": ["2026-09-21 10:00:00"],
    })

    result = transform_customers(df)

    assert result.loc[0, "kota"] == "Unknown"
    assert result.loc[0, "total_belanja"] == 175000

def test_transform_customers_invalid_total_becomes_nan():
    df = pd.DataFrame({
    "id": [1],
    "nama": ["Andi"],
    "umur": [25],
    "kota": ["Jakarta"],
    "total_belanja": ["abc"],
    "updated_at": ["2026-09-21 10:00:00"],
    })

    result = transform_customers(df)

    assert pd.isna(result.loc[0, "total_belanja"])

def test_transform_orders_amount_becomes_numeric():
    df = pd.DataFrame({
    "order_id": [101],
    "customer_id": [1],
    "amount": ["50000"],
    "updated_at": ["2026-09-21 10:00:00"],
    })

    result = transform_orders(df)

    assert result.loc[0, "amount"] == 50000