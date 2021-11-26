-- Create user
CREATE USER john@127.0.0.1;
CREATE USER john@localhost; -- only from local
CREATE USER john@'abc.com'; -- only abc.com domain
CREATE USER john@'%.abc.com'; -- sub domains
CREATE USER john IDENTIFIED BY 'password';


-- Show user
select * from mysql.`user` u;


-- dropping users
drop user john;


-- changing password
SET PASSWORD for john = '1234'; -- for different user, if current admin
SET PASSWORD = '1234'; -- for current user

-- granting privileges
-- https://dev.mysql.com/doc/refman/8.0/en/privileges-provided.html
-- 1: web/desktop app
CREATE USER moon_app IDENTIFIED BY '1234';
GRANT SELECT, INSERT, UPDATE, DELETE, EXECUTE
ON sql_store.*
TO moon_app;

-- 2: grant admin privileges
GRANT ALL
ON *.*
TO john;


-- Viewing Privieges
SHOW GRANTS FOR john;
SHOW GRANTS FOR moon_app;

-- REVOKING Privieges
REVOKE EXECUTE
ON sql_store.*
FROM moon_app;
