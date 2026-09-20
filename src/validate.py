import pandas as pd


def validate_customers(df):
    errors = []

    if df["id"].isnull().any():
        errors.append("Customer id contains NULL values")

    if df["nama"].isnull().any():
        errors.append("Customer nama contains NULL values")

    if df["umur"].isnull().any():
        errors.append("Customer umur contains NULL values")

    if df["kota"].isnull().any():
        errors.append("Customer kota contains NULL values")

    if df["total_belanja"].isnull().any():
        errors.append(
            "Customer total_belanja contains NULL or invalid values"
        )

    return errors


def validate_orders(df):
    errors = []

    if df["order_id"].isnull().any():
        errors.append("Order order_id contains NULL values")

    if df["customer_id"].isnull().any():
        errors.append("Order customer_id contains NULL values")

    if df["amount"].isnull().any():
        errors.append(
            "Order amount contains NULL or invalid values"
        )

    return errors


def get_invalid_customers(df):
    return df[df["total_belanja"].isnull()].copy()


def get_valid_customers(df):
    return df[df["total_belanja"].notnull()].copy()
