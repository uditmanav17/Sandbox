-- https://dev.mysql.com/doc/refman/8.0/en/numeric-functions.html
SELECT ROUND(5.37) ;
SELECT ROUND(5.37, 1) ;

SELECT TRUNCATE(5.37, 1);

SELECT CEILING(5.37); -- same as CEIL
SELECT CEIL(5.37); -- same as CEILING

SELECT FLOOR(5.37);

SELECT ABS(-5.37);

SELECT CEIL(5.37, 1);

SELECT RAND();

-- https://dev.mysql.com/doc/refman/8.0/en/string-functions.html
-- length, lower, upper, ltrim, rtrim, trim
SELECT LEFT("Kindergarden", 4);
SELECT RIGHT("Kindergarden", 6);
SELECT SUBSTRING("Kindergarden", 3, 5);
SELECT LOCATE('e', "Kindergarden");
SELECT REPLACE("Kindergarden", "gar", "tam");
SELECT CONCAT("first", " ","last");


-- https://dev.mysql.com/doc/refman/8.0/en/date-and-time-functions.html
SELECT NOW(), CURDATE(), CURTIME(), CURRENT_TIMESTAMP(), CURRENT_DATE(), CURRENT_TIME() ;
SELECT YEAR(NOW()), MONTH(NOW()), DAY(NOW()), HOUR(NOW()), MINUTE(NOW()), SECOND(NOW());
SELECT DAYNAME(NOW()), MONTHNAME(NOW()), EXTRACT(DAY FROM NOW()), EXTRACT(MONTH FROM NOW());
-- https://dev.mysql.com/doc/refman/8.0/en/date-and-time-functions.html#function_date-format
SELECT DATE_FORMAT(NOW(), '%a') ;
SELECT DATE_ADD(NOW(), INTERVAL 2 DAY);
SELECT DATE_ADD(NOW(), INTERVAL 2 YEAR);
SELECT DATE_ADD(NOW(), INTERVAL -2 MONTH);
SELECT DATE_SUB(NOW(), INTERVAL 2 MONTH);
SELECT DATEDIFF('2019-01-16', '2019-01-20');
SELECT TIME_TO_SEC('09:00') - TIME_TO_SEC('09:02');

-- IFNULL and COALESCE keyword
SELECT * FROM sql_store.orders o;
SELECT order_id, IFNULL(shipper_id, 'NOT ASSIGNED') FROM sql_store.orders o;
-- if shipper_id is null, return comment, if comment also null return 'not assigned'
SELECT order_id, COALESCE(shipper_id, comments, 'NOT ASSIGNED') FROM sql_store.orders o;

-- IF keyword
SELECT * from sql_store.orders o;
SELECT order_id, order_date, IF(YEAR(order_date) >= '2018', 'Current', 'Archived') AS order_status from sql_store.orders o;

-- CASE operator
SELECT 	order_id, order_date,
		CASE
			WHEN	YEAR(order_date) <= '2017'	THEN	'last to last year'
			WHEN	YEAR(order_date) = '2018'	THEN	'last year'
			ELSE	'current'
		END AS `YEAR`
from 	sql_store.orders o;
