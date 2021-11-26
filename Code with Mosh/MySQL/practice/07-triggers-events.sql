use sql_invoicing;

-- whenever an payment is done, update payment_total in invoices table
DROP TRIGGER IF EXISTS payments_after_insert;
DELIMITER $$
CREATE TRIGGER payments_after_insert
	AFTER INSERT ON payments
	FOR EACH ROW
BEGIN
	UPDATE 	invoices
	SET		payment_total = payment_total + NEW.amount
	WHERE 	invoice_id = NEW.invoice_id;
END $$

DELIMITER ;


INSERT into payments VALUES (DEFAULT, 5, 3, '2021-11-04', 11, 1);
SELECT * FROM payments p;
SELECT * FROM invoices i;


-- whenever an payment is done, update payment_total in invoices table
DROP TRIGGER IF EXISTS payments_after_delete;
DELIMITER $$
CREATE TRIGGER payments_after_delete
	AFTER DELETE ON payments
	FOR EACH ROW
BEGIN
	UPDATE 	invoices
	SET		payment_total = payment_total - OLD.amount
	WHERE 	invoice_id = OLD.invoice_id;
END $$

DELIMITER ;


DELETE FROM payments WHERE client_id = 5 and invoice_id = 3 and amount = 11;
SELECT * FROM payments p;
SELECT * FROM invoices i;

-- Show all triggers
SHoW TRIGGERS like 'payments%';


-- EVENTS
Show variables;
Show variables like 'event%';
SET GLOBAL event_scheduler = ON;

DELIMITER $$
CREATE EVENT yearly_delete_stale_audit_rows
ON SCHEDULE
-- 	AT '2020-01-10'
-- 	EVERY 1 HOUR
	EVERY 1 YEAR STARTS '2021-01-01' ENDS '2031-01-01'
DO BEGIN
	DELETE FROM payment_audit
	WHERE action_date < NOW() - INTERVAL 1 YEAR;
END $$
DELIMITER ;

SHOW EVENTS;
DROP EVENT IF EXISTS yearly_delete_stale_audit_rows;
ALTER EVENT yearly_delete_stale_audit_rows DISABLE;
ALTER EVENT yearly_delete_stale_audit_rows ENABLE;
