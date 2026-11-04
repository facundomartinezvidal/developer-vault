CREATE TABLE orders (
    id SERIAL PRIMARY KEY,
    customer_id INT,
    customer_email TEXT,
    status TEXT,
    total FLOAT,
    product_ids TEXT,
    created_at TIMESTAMP
);
