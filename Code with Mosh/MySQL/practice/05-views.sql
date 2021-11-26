-- creating VIEWS
CREATE VIEW sales_by_client AS
SELECT
	c.client_id,
	c.name,
	SUM(invoice_total) AS total_sale
FROM	sql_invoicing.clients c
		JOIN sql_invoicing.invoices i using (client_id)
GROUP BY	client_id, name;

SELECT * FROM sales_by_client;
-- ** views only create reference to main table columns, so any update in views are reflected in base table

-- DROP views
DROP VIEW sales_by_client;

-- replace view
CREATE OR REPLACE VIEW sales_by_client AS
SELECT
	c.client_id,
	c.name,
	SUM(invoice_total) AS total_sale
FROM	sql_invoicing.clients c
		JOIN sql_invoicing.invoices i using (client_id)
GROUP BY	client_id, name;

-- ** Data in views can be updated if views don't have
-- distinct
-- Aggregate functions
-- group by / having
-- union
