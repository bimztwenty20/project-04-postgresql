import pandas as pd

from src.validate import (
validate_customers,
validate_orders,
get_invalid_customers,
get_valid_customers,
)

def test_valid_customer_has_no_errors():
    df = pd.DataFrame({
    "id": [1],
    "nama": ["Andi"],
    "umur": [25],
    "kota": ["Jakarta"],
    "total_belanja": [175000],
    })

    errors = validate_customers(df)

    assert errors == []


def test_customer_with_null_total_belanja_is_invalid():
    df = pd.DataFrame({
    "id": [8],
    "nama": ["Hadi"],
    "umur": [35],
    "kota": ["Jakarta"],
    "total_belanja": [None],
    })

    errors = validate_customers(df)

    assert (
        "Customer total_belanja contains NULL or invalid values"
        in errors
    )


def test_invalid_customer_is_separated():
    df = pd.DataFrame({
    "id": [1, 2],
    "nama": ["Andi", "Hadi"],
    "umur": [25, 35],
    "kota": ["Jakarta", "Jakarta"],
    "total_belanja": [175000, None],
    })

    invalid = get_invalid_customers(df)

    assert len(invalid) == 1
    assert invalid.iloc[0]["id"] == 2


def test_valid_customers_are_separated():
    df = pd.DataFrame({
    "id": [1, 2],
    "nama": ["Andi", "Hadi"],
    "umur": [25, 35],
    "kota": ["Jakarta", "Jakarta"],
    "total_belanja": [175000, None],
    })

    valid = get_valid_customers(df)

    assert len(valid) == 1
    assert valid.iloc[0]["id"] == 1


def test_valid_order_has_no_errors():
    df = pd.DataFrame({
    "order_id": [101],
    "customer_id": [1],
    "amount": [50000],
    })

    errors = validate_orders(df)

    assert errors == []


def test_order_with_null_amount_is_invalid():
    df = pd.DataFrame({
    "order_id": [101],
    "customer_id": [1],
    "amount": [None],
    })

    errors = validate_orders(df)

    assert (
        "Order amount contains NULL or invalid values"
        in errors
    )