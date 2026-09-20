def get_last_successful_run(conn, pipeline_name):
    with conn.cursor() as cur:
        cur.execute(
            """
            SELECT last_successful_run
            FROM sales.pipeline_metadata
            WHERE pipeline_name = %s
            """,
            (pipeline_name,)
        )

        row = cur.fetchone()

        if row is None:
            raise ValueError(
                f"Pipeline '{pipeline_name}' tidak ditemukan."
            )

        return row[0]


def update_last_successful_run(
    conn,
    pipeline_name,
    new_watermark
):
    with conn.cursor() as cur:
        cur.execute(
            """
            UPDATE sales.pipeline_metadata
            SET last_successful_run = %s
            WHERE pipeline_name = %s
            """,
            (
                new_watermark,
                pipeline_name
            )
        )
