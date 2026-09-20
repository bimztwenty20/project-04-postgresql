from pathlib import Path

from src.extract import (
    extract_incremental_customers,
    extract_incremental_orders,
    extract_customers,
    extract_orders,
)

from src.transform import (
    transform_customers,
    transform_orders,
)
from src.validate import (
    validate_customers,
    validate_orders,
    get_invalid_customers,
    get_valid_customers,
)
from src.connection import get_connection

from src.watermark import (
    get_last_successful_run,
    update_last_successful_run,
)
from src.load import (
    load_customers,
    load_orders,
    soft_delete_missing_customers,
    soft_delete_missing_orders,
)


REJECTED_DIR = Path("data/rejected")


def main():

    print("=== INCREMENTAL PIPELINE START ===")

    # =========================
    # 1. GET WATERMARK
    # =========================

    print("\n[1] Get Watermark")

    with get_connection() as conn:

        customer_watermark = get_last_successful_run(
            conn,
            "customer_pipeline"
        )

        order_watermark = get_last_successful_run(
            conn,
            "order_pipeline"
        )

    print(
        f"Customer watermark: "
        f"{customer_watermark}"
    )

    print(
        f"Order watermark: "
        f"{order_watermark}"
    )

    # =========================
    # 2. INCREMENTAL EXTRACT
    # =========================

    print("\n[2] Incremental Extract")

    customers = extract_incremental_customers(
        customer_watermark
    )

    orders = extract_incremental_orders(
        order_watermark
    )

    print(
        f"Customers extracted: "
        f"{len(customers)}"
    )

    print(
        f"Orders extracted: "
        f"{len(orders)}"
    )

    # =========================
    # 3. TRANSFORM
    # =========================

    print("\n[3] Transform")

    customers = transform_customers(customers)
    orders = transform_orders(orders)

    print("Transform completed.")

    # =========================
    # 4. VALIDATE
    # =========================

    print("\n[4] Validate")

    customer_errors = validate_customers(customers)
    order_errors = validate_orders(orders)

    invalid_customers = get_invalid_customers(
        customers
    )

    valid_customers = get_valid_customers(
        customers
    )

    if customer_errors:
        print("Customer validation FAILED")

        for error in customer_errors:
            print(f"- {error}")

    if order_errors:
        print("Order validation FAILED")

        for error in order_errors:
            print(f"- {error}")

        print("\nPipeline stopped.")
        return

    print(
        f"Valid customers: "
        f"{len(valid_customers)}"
    )

    print(
        f"Invalid customers: "
        f"{len(invalid_customers)}"
    )

    print("Orders valid.")

    # =========================
    # 5. REJECT INVALID DATA
    # =========================

    print("\n[5] Rejected Data")

    REJECTED_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    if not invalid_customers.empty:

        rejected_path = (
            REJECTED_DIR /
            "customers_rejected.csv"
        )

        invalid_customers.to_csv(
            rejected_path,
            index=False
        )

        print(
            f"Rejected customers saved to: "
            f"{rejected_path}"
        )

    else:

        print("No rejected customers.")

    # =========================
    # 6. LOAD + WATERMARK
    # =========================

    print("\n[6] Load")

    with get_connection() as conn:

        try:

            # Load customers
            load_customers(
                conn,
                valid_customers
            )

            source_customers = extract_customers()
            source_customer_ids = source_customers["id"].tolist()

            soft_delete_missing_customers(
                conn,
                source_customer_ids
            )

            # Load orders
            load_orders(
                conn,
                orders
            )

            source_orders = extract_orders()
            source_order_ids = source_orders["order_id"].tolist()

            soft_delete_missing_orders(
                conn,
                source_order_ids
            )


            # =========================
            # CUSTOMER WATERMARK
            # =========================

            if not customers.empty:

                new_customer_watermark = (
                    customers["updated_at"].max()
                )

                update_last_successful_run(
                    conn,
                    "customer_pipeline",
                    new_customer_watermark
                )

                print(
                    f"New customer watermark: "
                    f"{new_customer_watermark}"
                )

            # =========================
            # ORDER WATERMARK
            # =========================

            if not orders.empty:

                new_order_watermark = (
                    orders["updated_at"].max()
                )

                update_last_successful_run(
                    conn,
                    "order_pipeline",
                    new_order_watermark
                )

                print(
                    f"New order watermark: "
                    f"{new_order_watermark}"
                )

            # =========================
            # COMMIT
            # =========================

            conn.commit()

            print("Load completed.")
            print("Transaction committed.")

        except Exception as error:

            conn.rollback()

            print("Pipeline failed.")
            print("Transaction rolled back.")
            print(f"Error: {error}")

            raise

    print("\n=== INCREMENTAL PIPELINE SUCCESS ===")


if __name__ == "__main__":
    main()
