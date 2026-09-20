from connection import get_connection

def main():
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO sales.orders
                    (order_id, customer_id, amount)
                VALUES
                    (%s, %s, %s)
                """,
                (108, 2, 175000),
            )

        conn.commit()

        print("Transaction committed successfully!!")


if __name__ == "__main__" :
    main()