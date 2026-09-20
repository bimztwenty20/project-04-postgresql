from src.connection import get_connection
from src.watermark import get_last_successful_run


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
        "Customer watermark:",
        customer_watermark
    )

    print(
        "Order watermark:",
        order_watermark
    )
