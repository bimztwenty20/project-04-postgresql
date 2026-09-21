from src.connection import get_connection


def test_transaction_commit():
    order_id = 108

    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO sales.orders
                    (order_id, customer_id, amount)
                VALUES
                    (%s, %s, %s)
                """,
                (order_id, 2, 175000),
            )

        conn.commit()

    # Buka connection baru untuk memastikan data
    # benar-benar sudah committed.
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT order_id, customer_id, amount
                FROM sales.orders
                WHERE order_id = %s
                """,
                (order_id,),
            )

            result = cur.fetchone()

            assert result is not None
            assert result[0] == order_id
            assert result[1] == 2
            assert result[2] == 175000

            # Cleanup agar test tidak meninggalkan data.
            cur.execute(
                """
                DELETE FROM sales.orders
                WHERE order_id = %s
                """,
                (order_id,),
            )

        conn.commit()
