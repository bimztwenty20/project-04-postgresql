CREATE OR REPLACE FUNCTION sales.update_updated_at()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;


DROP TRIGGER IF EXISTS trg_customers_updated_at
ON sales.customers;

CREATE TRIGGER trg_customers_updated_at
BEFORE UPDATE ON sales.customers
FOR EACH ROW
EXECUTE FUNCTION sales.update_updated_at();


DROP TRIGGER IF EXISTS trg_orders_updated_at
ON sales.orders;

CREATE TRIGGER trg_orders_updated_at
BEFORE UPDATE ON sales.orders
FOR EACH ROW
EXECUTE FUNCTION sales.update_updated_at();
