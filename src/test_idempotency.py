from src.connection import get_connection


def test_orders_are_not_duplicated():
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT order_id, COUNT(*)
                FROM sales.orders
                GROUP BY order_id
                HAVING COUNT(*) > 1
                """
            )

            duplicates = cur.fetchall()

    assert duplicates == []
