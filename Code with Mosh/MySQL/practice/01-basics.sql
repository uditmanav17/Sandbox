
SELECT * from sql_store.customers c;

SELECT
	first_name,
	last_name,
	points,
	(points + 10) * 100 as discount_factor
from sql_store.customers;


SELECT DISTINCT state from sql_store.customers c;

-- queries are case insensitive
SELECT * from sql_store.customers c WHERE state ='VA';
SELECT * from sql_store.customers c WHERE state ='va';

-- AND OR NOT
SELECT 	*
from 	sql_store.customers
WHERE 	NOT (birth_date > '1990-01-01'
		OR (points > 1000 AND state = 'VA'));

-- EXERCISE - from orders_items get items for order #6 where total price > 30
SELECT 	*, quantity * unit_price AS total_price from sql_store.order_items
WHERE	order_id = 6 and (quantity * unit_price) > 30;

-- IN operater
-- return products with quantity equal 49, 38, 72
SELECT * from sql_store.products p where quantity_in_stock in (49, 38, 72);

-- Between Operator
SELECT * from sql_store.customers where points >=1000 and points <=3000;
SELECT * from sql_store.customers where points BETWEEN 1000 and 3000;

-- LIKE operator - wildcards -> '%' and '_'
SELECT * from sql_store.customers WHERE last_name LIKE 'b%';
SELECT * from sql_store.customers WHERE last_name LIKE '%b%';
SELECT * from sql_store.customers WHERE last_name LIKE '_o%';
SELECT * from sql_store.customers WHERE last_name LIKE '%y';
SELECT * from sql_store.customers WHERE last_name LIKE 'b____y';

-- Exercise - customers whose address contain 'trail' or 'avenue'
SELECT * from sql_store.customers WHERE address LIKE '%trail%' OR address LIKE '%avenue%';
-- Exercise - customers having phone ending with 9
SELECT * from sql_store.customers WHERE phone LIKE '%9';


-- REGEXP operator
-- ends with field
SELECT * from sql_store.customers WHERE last_name REGEXP 'field$';
-- starts with mac
SELECT * from sql_store.customers WHERE last_name REGEXP '^mac';
-- contains mac or field
SELECT * from sql_store.customers WHERE last_name REGEXP 'mac|field';
-- starts with mac or ends with field or contains rose
SELECT * from sql_store.customers WHERE last_name REGEXP '^mac|field$|rose';
-- contains ge or ie or me
SELECT * from sql_store.customers WHERE last_name REGEXP '[gim]e';
SELECT * from sql_store.customers WHERE last_name REGEXP '[a-h]e';


-- LIMIT operator
-- limit 0ffset, pick - skip first 6 records pick next 3
SELECT * from sql_store.customers order by first_name limit 6, 3
-- Exercise - top 3 loyal customers
SELECT * from sql_store.customers order by points DESC limit 3;
