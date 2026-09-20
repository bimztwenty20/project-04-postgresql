
def load_customers(conn, customers):
    with conn.cursor() as cur:
        query = """
            insert into sales.customers
                (id, nama, umur, kota, total_belanja, updated_at, is_deleted)
            values
                (%s, %s, %s, %s, %s, %s, False)
            on conflict (id)
            do update set
                nama = excluded.nama,
                umur = excluded.umur,
                kota = excluded.kota,
                total_belanja = excluded.total_belanja,
                updated_at = excluded.updated_at,
                is_deleted = False
        """

        data = [
            (
                row.id,
                row.nama,
                row.umur,
                row.kota,
                row.total_belanja,
                row.updated_at
            )
            for row in customers.itertuples(index=False)
        ]

        cur.executemany(query, data)

def load_orders(conn, orders):
    with conn.cursor() as cur:
        query = """
            insert into sales.orders
                (order_id, customer_id, amount, updated_at, is_deleted)
            values
                (%s, %s, %s, %s, False)
            on conflict (order_id)
            do update set
                customer_id = excluded.customer_id,
                amount = excluded.amount,
                updated_at = excluded.updated_at,
                is_deleted = False
        """

        data = [
            (
                row.order_id,
                row.customer_id,
                row.amount,
                row.updated_at
            )
            for row in orders.itertuples(index=False)
        ]

        cur.executemany(query, data)

def soft_delete_customers(conn, source_customer_ids):
    with conn.cursor() as cur:
        query = """
            UPDATE sales.customers
            SET
                is_deleted = TRUE,
                updated_at = CURRENT_TIMESTAMP
            WHERE id <> ALL(%s)
              AND is_deleted = FALSE
        """

        cur.execute(query, (source_customer_ids,))

def soft_delete_orders(conn, source_order_ids):
    with conn.cursor() as cur:
        query = """
            UPDATE sales.orders
            SET
                is_deleted = TRUE,
                updated_at = CURRENT_TIMESTAMP
            WHERE order_id <> ALL(%s)
              AND is_deleted = FALSE
        """

        cur.execute(query, (source_order_ids,))

def soft_delete_missing_customers(conn, source_customer_ids):
    with conn.cursor() as cur:
        query = """
            UPDATE sales.customers
            SET
                is_deleted = TRUE,
                updated_at = CURRENT_TIMESTAMP
            WHERE id <> ALL(%s)
              AND is_deleted = FALSE
        """

        cur.execute(query, (source_customer_ids,))

def soft_delete_missing_orders(conn, source_order_ids):
    with conn.cursor() as cur:
        query = """
            UPDATE sales.orders
            SET
                is_deleted = TRUE,
                updated_at = CURRENT_TIMESTAMP
            WHERE order_id <> ALL(%s)
              AND is_deleted = FALSE
        """

        cur.execute(query, (source_order_ids,))
