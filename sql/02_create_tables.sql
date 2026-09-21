CREATE TABLE IF NOT EXISTS sales.customers (
    id INTEGER PRIMARY KEY,
    nama VARCHAR(100) NOT NULL,
    umur INTEGER,
    kota VARCHAR(100),
    total_belanja NUMERIC(12, 2),

    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,

    is_deleted BOOLEAN NOT NULL DEFAULT FALSE
);

CREATE TABLE IF NOT EXISTS sales.orders (
    order_id INTEGER PRIMARY KEY,
    customer_id INTEGER NOT NULL,
    amount NUMERIC(12, 2) NOT NULL,

    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,

    is_deleted BOOLEAN NOT NULL DEFAULT FALSE,

    CONSTRAINT fk_orders_customers
        FOREIGN KEY (customer_id)
        REFERENCES sales.customers(id)
);

CREATE INDEX IF NOT EXISTS idx_orders_customer_id
    ON sales.orders(customer_id);

CREATE TABLE IF NOT EXISTS sales.pipeline_metadata (
    pipeline_name VARCHAR(100) PRIMARY KEY,
    last_successful_run TIMESTAMP NOT NULL
);
