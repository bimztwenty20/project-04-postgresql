INSERT INTO sales.pipeline_metadata (
    pipeline_name,
    last_successful_run
)
VALUES
    (
        'customer_pipeline',
        '1970-01-01 00:00:00'
    ),
    (
        'order_pipeline',
        '1970-01-01 00:00:00'
    )
ON CONFLICT (pipeline_name)
DO NOTHING;
