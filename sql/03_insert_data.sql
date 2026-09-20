INSERT INTO sales.customers (
    id, nama, umur, kota, total_belanja
)

VALUES
    (1, 'Andi', 25, 'Jakarta', 150000),
    (2, 'Budi', 31, 'Bandung', 250000),
    (3, 'Citra', 27, 'Jakarta', 175000),
    (4, 'Deni', 22, 'Surabaya', 90000),
    (5, 'Eka', 29, 'Bandung', 300000),
    (6, 'Fajar', 28, NULL, 200000),
    (7, 'Gina', 28, NULL, 125000),
    (8, 'Hadi', 35, 'Jakarta', NULL);

INSERT INTO sales.orders(
    order_id, customer_id, amount
)

VALUES
    (101, 1, 50000),
    (102, 1, 100000),
    (103, 2, 200000),
    (104, 3, 75000),
    (105, 5, 300000);