from connection import get_connection

def main():
    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    INSERT INTO sales.orders
                        (order_id, customer_id, amount)
                    VALUES
                        (%s, %s, %s)
                    """,
                    (109, 3, 100000),
                )

                print("Order 109 inserted.")

                #Sengaja bikin gagal
                #karena customer 999 tidak ada
                cur.execute(
                    """
                    INSERT INTO sales.orders
                        (order_id, customer_id, amount)
                    VALUES
                        (%s, %s, %s)
                    """,
                        (110, 999, 50000),
                )

                conn.commit()

    except Exception as e:
        print("Transaction failed!")
        print(f"Error: {e}")


if __name__ == "__main__":
    main()