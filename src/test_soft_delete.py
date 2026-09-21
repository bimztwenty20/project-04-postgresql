from src.connection import get_connection
from src.load import soft_delete_missing_customers


def test_soft_delete_missing_customers():
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                UPDATE sales.customers
                SET is_deleted = FALSE
                WHERE id = 7
                """
            )

        soft_delete_missing_customers(
            conn,
            [1, 2, 3, 4, 5, 6]
        )

        conn.commit()

        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT is_deleted
                FROM sales.customers
                WHERE id = 7
                """
            )

            result = cur.fetchone()

    assert result[0] is True
