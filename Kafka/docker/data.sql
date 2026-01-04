

-- 2024-12-21 22:13:58.7330
CREATE TABLE orders (
id SERIAL PRIMARY KEY,
customer_id VARCHAR(50) NOT NULL,
customer_name VARCHAR(100),
customer_email VARCHAR(255),
product_id VARCHAR(50),
total_amount NUMERIC(10, 2),
order_date TIMESTAMPTZ,
status VARCHAR(50),
payment_method VARCHAR(50)
);

-- 2024-12-21 22:14:43.4620
INSERT INTO orders (
customer_id,
customer_name,
customer_email,
product_id,
total_amount,
order_date,
status,
payment_method
)
VALUES (
'CUST-1234',
'John Smith',
'john.smith@example.com',
'PROD-XYZ789',
59.95,
'2024-12-09T10:45:00Z',
'shipped',
'paypal'
)
RETURNING id;


