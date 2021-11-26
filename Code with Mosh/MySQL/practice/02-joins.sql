Use sql_store;

SELECT o.*, c.first_name, c.last_name, c.customer_id from orders o Join customers c on o.customer_id = c.customer_id;



-- which product was ordered by which customer
SELECT 	oi.order_id, oi.product_id, o.customer_id , p2.name, c.first_name, c.last_name
from
		order_items oi join products p2 on oi.product_id = p2.product_id
-- 		join orders o on oi.order_id = o.order_id
		join orders o USING (order_id)
-- 		join customers c on c.customer_id = o.customer_id
		join customers c using (customer_id)




-- self joins
select * from sql_hr.employees e
-- which employee reports to whom?
select 	e1.employee_id, e1.first_name, e1.last_name, e1.reports_to, CONCAT(e2.first_name,' ', e2.last_name) AS Manager
from 	sql_hr.employees e1 LEFT JOIN sql_hr.employees e2 on e1.reports_to = e2.employee_id



-- UNION
SELECT customer_id, first_name, last_name, points, 'Bronze' AS Type from customers c WHERE points < 2000
UNION
SELECT customer_id, first_name, last_name, points, 'Silver' from customers c WHERE points BETWEEN 2000 and 3000
UNION
SELECT customer_id, first_name, last_name, points, 'Gold' from customers c WHERE points > 3000 ORDER by first_name


-- Inerting updating and deleting data
SELECT * from customers c ;
desc customers ;
-- default is used to assign default values to columns while inserting
insert into customers values (DEFAULT, 'John', "Smith", '1990-01-01', NULL, 'address', 'city', 'CA', DEFAULT);
-- same as previous INSERT
insert into customers (first_name, last_name, birth_date, address, city, state)
values ('John', "Smith", '1990-01-01', 'address', 'city', 'CA');


INSERT into shippers (name)
values ('shipper1'), ('shipper2'), ('shipper3')



-- Copying tables
-- only create copy, doesn't copy constraints
Create table orders_archived as
Select * from orders o ;
