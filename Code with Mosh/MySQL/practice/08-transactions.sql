
-- Recreate DB
-- Creating transaction

Start Transaction;

insert into sql_store.orders(customer_id, order_date, status)
VALUES (1, '2019-01-01', 1);

INSERT into order_items VALUES (LAST_INSERT_ID(), 1, 1, 1);

COMMIT;

-- we can use ROLLBACK instead of COMMIT to test some temporary changes
-- by delfault, insert/update/delete are wrapped in transaction block, we can check and update this by
SHOW variables LIKE 'autocommit';


SELECT * FROM sql_store.orders o ;
SELECT * FROM sql_store.order_items oi ;



-- CONCURRENCY PROBLEMS
SHOW variables LIKE 'transaction_isolation';
SET TRANSACTION ISOLATION LEVEL SERIALIZABLE; -- only applies to next transaction
SET SESSION TRANSACTION ISOLATION LEVEL SERIALIZABLE; -- for current session
SET GLOBAL TRANSACTION ISOLATION LEVEL READ UNCOMMITTED; -- everywhere

-- READ UNCOMMITTED - can read uncomitted data - dirty reads
-- READ COMITTED - multiple reads in same transaction may return different results, if data modified by other transaction
-- REPEATABLE READ - solves above problem, causes phantom reads
-- SERIALIZABLE - solves all problems, but slows down overall performance and hurts scalability
