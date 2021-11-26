USE sql_invoicing;


-- This needs to be executed as independent script
DROP PROCEDURE IF EXISTS get_clients;

DELIMITER $$
CREATE PROCEDURE get_clients ()
BEGIN
	SELECT * FROM clients;
END$$

DELIMITER ;
-- till here

CALL get_clients();

-- Parameterized sp with default values
DROP PROCEDURE IF EXISTS get_clients_by_state;

DELIMITER $$
CREATE PROCEDURE sql_invoicing.get_clients_by_state(state CHAR(2))
BEGIN
	IF state is NULL THEN
		SET state = 'CA';
	END IF;

	SELECT 	* FROM clients c
	WHERE 	c.state = state;
END$$
DELIMITER ;

CALL get_clients_by_state(NULL);
CALL get_clients_by_state('CA');



-- https://www.ibm.com/docs/en/db2-for-zos/11?topic=codes-sqlstate-values-common-error
-- paramaterized sp with validations
DROP PROCEDURE IF EXISTS make_payments;

DELIMITER $$
CREATE PROCEDURE sql_invoicing.make_payments
(
	invoice_id INT,
	payment_amount DECIMAL(9, 2),
	payment_date DATE
)
BEGIN
	IF	payment_amount <= 0	THEN
		-- signal is like exception
		SIGNAL SQLSTATE '22003'
			SET MESSAGE_TEXT = 'Invalid Payment Amount';
	END IF;

	UPDATE 	invoices i
	SET		i.payment_total = payment_amount,
			i.payment_date = payment_date
	WHERE 	i.invoice_id = invoice_id;
END$$
DELIMITER ;

SELECT * FROM invoices i WHERE invoice_id = 2;
CALL sql_invoicing.make_payments(2, 100, '2019-01-01'); -- valid update
CALL sql_invoicing.make_payments(2, -100, '2019-01-01'); -- invalid update
CALL sql_invoicing.make_payments(2, 8.18, '2019-02-12'); -- restoring to previous value



-- output param sp
DELIMITER $$
CREATE PROCEDURE sql_invoicing.get_unpaid_invoices_for_client
(
	client_id INT,
	OUT invoices_count INT,
	OUT invoices_total DECIMAL(9, 2)
)
BEGIN
	SELECT 	COUNT(*), SUM(invoice_total)
	INTO	invoices_count, invoices_total
	FROM	sql_invoicing.invoices i
	WHERE 	i.client_id = client_id
			AND payment_total = 0;
END$$
DELIMITER ;

-- user/session variables
set @invoices_count_variable = 0, @invoices_total_variable = 0;
CALL get_unpaid_invoices_for_client(3, @invoices_count_variable, @invoices_total_variable);
SELECT @invoices_count_variable, @invoices_total_variable;


-- Local varibles in sp
DROP PROCEDURE IF EXISTS sql_invoicing.get_risk_factor;

DELIMITER $$
$$
CREATE PROCEDURE sql_invoicing.get_risk_factor ()
BEGIN
	-- risk_factor = invoices_total / invoices_count * 5
	DECLARE	risk_factor DECIMAL(9, 2) DEFAULT 0;
	DECLARE invoices_total DECIMAL(9, 2);
	DECLARE	invoices_count INT;

	SELECT 	COUNT(*), SUM(invoice_total)
	INTO	invoices_count, invoices_total
	FROM	sql_invoicing.invoices;

	SET	risk_factor = invoices_total / invoices_count * 5;
	SELECT risk_factor;
END$$
DELIMITER ;


CALL get_risk_factor();


-- FUNCTIONS
DROP FUNCTION IF EXISTS sql_invoicing.get_risk_factor_for_client;

DELIMITER $$
$$
CREATE FUNCTION sql_invoicing.get_risk_factor_for_client
(
	client_id INT
)
RETURNS INT
-- DETERMINISTIC
READS SQL DATA
-- MODIFIES SQL DATA
BEGIN
	-- risk_factor = invoices_total / invoices_count * 5
	DECLARE	risk_factor DECIMAL(9, 2) DEFAULT 0;
	DECLARE invoices_total DECIMAL(9, 2);
	DECLARE	invoices_count INT;

	SELECT 	COUNT(*), SUM(invoice_total)
	INTO	invoices_count, invoices_total
	FROM	sql_invoicing.invoices i
	WHERE 	i.client_id = client_id;

	SET	risk_factor = invoices_total / invoices_count * 5;
	RETURN IFNULL(risk_factor, 0);
END$$
DELIMITER ;

SET @risk_f = get_risk_factor_for_client(3);
SELECT @risk_f;

SELECT client_id, name, get_risk_factor_for_client(client_id) from clients c;
