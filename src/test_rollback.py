from src.connection import get_connection


def test_transaction_rollback():
    valid_order_id = 109
    invalid_order_id = 110

    with get_connection() as conn:
        try:
            with conn.cursor() as cur:
                # Insert pertama seharusnya valid.
                cur.execute(
                    """
                    INSERT INTO sales.orders
                        (order_id, customer_id, amount)
                    VALUES
                        (%s, %s, %s)
                    """,
                    (valid_order_id, 3, 100000),
                )

                # Insert kedua sengaja gagal karena
                # customer_id 999 tidak ada.
                cur.execute(
                    """
                    INSERT INTO sales.orders
                        (order_id, customer_id, amount)
                    VALUES
                        (%s, %s, %s)
                    """,
                    (invalid_order_id, 999, 50000),
                )

                conn.commit()

        except Exception:
            conn.rollback()

    # Pastikan order 109 ikut ter-rollback.
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT order_id
                FROM sales.orders
                WHERE order_id = %s
                """,
                (valid_order_id,),
            )

            result = cur.fetchone()

            assert result is None
