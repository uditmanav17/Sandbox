


-- Aggregate functions
-- only operate with non null values
SELECT
	MAX(invoice_total) as highest,
	MIN(invoice_total) as lowest,
	AVG(invoice_total) as average,
	SUM(invoice_total) as total,
	SUM(invoice_total * 1.1) as new_total,
	COUNT(invoice_total) as number_of_invoices,
	COUNT(payment_date) as number_of_payments,
	COUNT(*) as total_records,
	COUNT(DISTINCT client_id) as distinct_clients
FROM sql_invoicing.invoices i;

-- group by
-- total sales per client
SELECT		client_id , SUM(invoice_total) as total_sales
from 		sql_invoicing.invoices i
group by 	client_id
HAVING		total_sales > 500
ORDER BY 	total_sales DESC;

SELECT		state, city , SUM(invoice_total) as total_sales
from 		sql_invoicing.invoices i
			join sql_invoicing.clients c using (client_id)
group by 	state, city
ORDER BY 	total_sales DESC;


-- customers in virginia who spent more than 100$
select		*
FROM 		sql_store.customers c
			JOIN orders o using (customer_id)
			JOIN order_items oi using (order_id)
WHERE 		state ='VA';


-- rollup operator (only mysql)
SELECT		client_id , SUM(invoice_total) as total_sales
from 		sql_invoicing.invoices i
group by 	client_id with ROLLUP
ORDER BY 	total_sales DESC;



-- ALL Keyword
-- invoices larger than all invoices of client 3
SELECT 		*
FROM 		sql_invoicing.invoices i
WHERE 		invoice_total > ALL(SELECT invoice_total from sql_invoicing.invoices i2 where client_id = 3);
-- same as
SELECT 		*
FROM 		sql_invoicing.invoices i
WHERE 		invoice_total > (SELECT max(invoice_total) from sql_invoicing.invoices i2 where client_id = 3);


-- ANY Keyword
-- invoices larger than NAY invoices of client 3
SELECT 		*
FROM 		sql_invoicing.invoices i
WHERE 		invoice_total > ANY(SELECT invoice_total from sql_invoicing.invoices i2 where client_id = 3);
-- same as
SELECT 		*
FROM 		sql_invoicing.invoices i
WHERE 		invoice_total > (SELECT MIN(invoice_total) from sql_invoicing.invoices i2 where client_id = 3);


-- Correlated Sub Queries
-- get invoices larger than client's average invoice amount
SELECT 		*
FROM 		sql_invoicing.invoices i
WHERE 		invoice_total > (	SELECT 	AVG(invoice_total)
								FROM	sql_invoicing.invoices i2
								WHERE 	i2.client_id = i.client_id );


-- EXISTS keyword
-- clients having invoice
SELECT * from sql_invoicing.clients
WHERE 	client_id in (SELECT DISTINCT client_id from sql_invoicing.invoices i2);
-- ** same as (exists query is better in cases when subquery resultset is large)
SELECT	* FROM sql_invoicing.clients c
WHERE EXISTS ( SELECT client_id from sql_invoicing.invoices i WHERE client_id=c.client_id);

-- find products that have never been ordered
SELECT * FROM sql_store.order_items oi;
SELECT * FROM sql_store.products p
WHERE NOT EXISTS (	SELECT product_id from sql_store.order_items oi WHERE product_id=p.product_id);



-- ** subqueries in select clause
SELECT
	invoice_id,
	invoice_total,
	(SELECT AVG(invoice_total) from sql_invoicing.invoices i ) AS invoice_average,
	invoice_total - (SELECT invoice_average) AS difference
FROM sql_invoicing.invoices i;
