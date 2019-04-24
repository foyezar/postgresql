# PostgreSQL

## customers.sql
```sql
-- ----------------------------
--  Table structure for customers
-- ----------------------------
DROP TABLE IF EXISTS "public"."customers";
CREATE TABLE "public"."customers" (
	"first_name" varchar(100) COLLATE "default",
	"id" int4 NOT NULL,
	"last_name" varchar(255) COLLATE "default"
)
WITH (OIDS=FALSE);

-- ----------------------------
--  Records of customers
-- ----------------------------
BEGIN;
INSERT INTO "public"."customers" VALUES ('Rolf', '1', 'Smith');
INSERT INTO "public"."customers" VALUES ('Jose', '2', 'Salvatierra');
INSERT INTO "public"."customers" VALUES ('Anne', '3', 'Watson');
INSERT INTO "public"."customers" VALUES ('Craig', '4', 'Scott');
INSERT INTO "public"."customers" VALUES ('Michael', '5', 'Adam');
COMMIT;

-- ----------------------------
--  Primary key structure for table customers
-- ----------------------------
ALTER TABLE "public"."customers" ADD PRIMARY KEY ("id") NOT DEFERRABLE INITIALLY IMMEDIATE;
```

## items.sql
```sql
-- ----------------------------
--  Table structure for items
-- ----------------------------
DROP TABLE IF EXISTS "public"."items";
CREATE TABLE "public"."items" (
	"name" varchar(255) NOT NULL COLLATE "default",
	"id" int4 NOT NULL,
	"price" numeric(10,2)
)
WITH (OIDS=FALSE);

-- ----------------------------
--  Records of items
-- ----------------------------
BEGIN;
INSERT INTO "public"."items" VALUES ('Pen', '1', '5.00');
INSERT INTO "public"."items" VALUES ('Fountain Pen', '2', '11.30');
INSERT INTO "public"."items" VALUES ('Ink', '3', '3.50');
INSERT INTO "public"."items" VALUES ('Laptop', '4', '899.00');
INSERT INTO "public"."items" VALUES ('Screen', '5', '275.50');
INSERT INTO "public"."items" VALUES ('Hard Drive', '6', '89.99');
COMMIT;

-- ----------------------------
--  Primary key structure for table items
-- ----------------------------
ALTER TABLE "public"."items" ADD PRIMARY KEY ("id") NOT DEFERRABLE INITIALLY IMMEDIATE;
```

## purchases.sql
```sql
-- ----------------------------
--  Table structure for purchases
-- ----------------------------
DROP TABLE IF EXISTS "public"."purchases";
CREATE TABLE "public"."purchases" (
	"id" int4 NOT NULL,
	"item_id" int4,
	"customer_id" int4
)
WITH (OIDS=FALSE);

-- ----------------------------
--  Records of purchases
-- ----------------------------
BEGIN;
INSERT INTO "public"."purchases" VALUES ('1', '4', '1');
INSERT INTO "public"."purchases" VALUES ('2', '5', '1');
INSERT INTO "public"."purchases" VALUES ('3', '6', '1');
INSERT INTO "public"."purchases" VALUES ('4', '1', '3');
INSERT INTO "public"."purchases" VALUES ('5', '3', '5');
INSERT INTO "public"."purchases" VALUES ('6', '2', '5');
INSERT INTO "public"."purchases" VALUES ('7', '4', '2');
INSERT INTO "public"."purchases" VALUES ('8', '2', '4');
INSERT INTO "public"."purchases" VALUES ('9', '3', '4');
INSERT INTO "public"."purchases" VALUES ('10', '6', '5');
COMMIT;

-- ----------------------------
--  Primary key structure for table purchases
-- ----------------------------
ALTER TABLE "public"."purchases" ADD PRIMARY KEY ("id") NOT DEFERRABLE INITIALLY IMMEDIATE;

-- ----------------------------
--  Foreign keys structure for table purchases
-- ----------------------------
ALTER TABLE "public"."purchases" ADD CONSTRAINT "fk_customer_purchase" FOREIGN KEY ("customer_id") REFERENCES "public"."customers" ("id") ON UPDATE NO ACTION ON DELETE NO ACTION NOT DEFERRABLE INITIALLY IMMEDIATE;
ALTER TABLE "public"."purchases" ADD CONSTRAINT "fk_purchase_item" FOREIGN KEY ("item_id") REFERENCES "public"."items" ("id") ON UPDATE NO ACTION ON DELETE NO ACTION NOT DEFERRABLE INITIALLY IMMEDIATE;
```

## CRUD

### SELECT
```sql
- SELECT * FROM customers;
- SELECT customers.first_name AS "First Name"
FROM customers;
- SELECT customers.first_name, customers.last_name
FROM customers
WHERE customers.first_name = 'Rolf';
- UPDATE items SET price = 4.00 WHERE id = 3;
- DELETE FROM items WHERE id = 4;
- SELECT * FROM customers
WHERE last_name like '%t_';
```

### JOIN
```sql
# Set - group of unordered unique elements
# INTERSECT - common to two or multiple sets
# INNER JOIN akin Set intersection
# INNER JOIN - selects rows from tab1 and tab2 where they match the selecting column

- SELECT * FROM customers INNER JOIN orders
ON customers.id = orders.customer_id;

# LEFT JOIN
# This selects all rows from the tab1, on the left, the rows from the tab2, on the right, if they match
# If they don't match, the data for the right table in blank

# RIGHT JOIN
# This selects all the rows from the table on the right, and then the rows from the table on left if they match

# FULL JOIN
# This selects all rows from both tables, matching them if there is a match on the selecting column

- SELECT customers.first_name, customers.last_name, items.name, items.price FROM items 
INNER JOIN purchases
ON items.id = purchases.item_id
INNER JOIN customers
ON customers.id = purchases.customer_id;

- SELECT customers.first_name, customers.last_name, COUNT(purchases.id) 
FROM customers
LEFT JOIN purchases
ON customers.id = purchases.customer_id
GROUP BY customers.id;

- SELECT customers.first_name, customers.last_name, SUM(items.price) AS "Total Price"
FROM items
INNER JOIN purchases ON items.id = purchases.item_id
INNER JOIN customers ON purchases.customer_id = customers.id
GROUP BY customers.id;

- SELECT customers.first_name, customers.last_name, SUM(items.price) AS "total_spent"
FROM items
INNER JOIN purchases ON items.id = purchases.item_id
INNER JOIN customers ON purchases.customer_id = customers.id
GROUP BY customers.id
ORDER BY total_spent DESC;

- SELECT customers.first_name, customers.last_name, SUM(items.price) AS "total_spent"
FROM items
INNER JOIN purchases ON items.id = purchases.item_id
INNER JOIN customers ON purchases.customer_id = customers.id
GROUP BY customers.id
ORDER BY total_spent DESC
LIMIT 2;
```

### CREATE
```sql
- CREATE TABLE IF NOT EXISTS public.users (
	id int4 PRIMARY KEY,
	name CHARACTER VARYING(100) NOT NULL
);

- CREATE TABLE IF NOT EXISTS public.users (
	id int4,
	name CHARACTER VARYING(100) NOT NULL,
	CONSTRAINT user_id_pkey PRIMARY KEY (id)
);

# FOREIGN KEY
- create table IF NOT EXISTS videos (
	id int4 primary key,
	user_id int4 REFERENCES public.users,
	name CHARACTER VARYING(255) NOT NULL
)
```

### INSERT
```sql
- INSERT INTO public.users(id, name)
VALUES (1, 'Foyez');
- INSERT INTO public.users
VALUES (2, 'Farhan');

- CREATE SEQUENCE user_id_seq START 3;
- ALTER TABLE public.users
ALTER COLUMN id
SET DEFAULT nextval('user_id_seq');
- ALTER SEQUENCE user_id_seq OWNED BY public.users.id;
```

### INDEX
```sql
# INDEX
- CREATE INDEX user_name_index
ON public.users(name);

# MULTI COLUMN INDEX
- CREATE INDEX index_name ON public.movies(id, user_id);

# WHEN INDEX CORUPTED OR SEARCH BECOMES SLOWER
- REINDEX INDEX index_name;
- REINDEX DATABASE db_name;
- REINDEX TABLE table_name;
```

### DROP
```sql
- DROP TABLE public.users;
- DROP TABLE public.users RESTRICT;
- DROP TABLE public.users CASECADE;
- DROP TABLE IF EXISTS public.users;
- DROP DATABASE public.users;
- DROP SEQUENCE public.users;
- DROP VIEW public.users;
```

### VIEW
```sql
- CREATE VIEW total_revenue_per_customer AS
SELECT customers.id, customers.first_name, customers.last_name, SUM(items.price) FROM customers
INNER JOIN purchases ON customers.id = purchases.customer_id
INNER JOIN items ON purchases.item_id = items.id
GROUP BY customers.id;

- CREATE VIEW awesome_customer AS
SELECT * FROM total_revenue_per_customer WHERE sum >= 150;

- CREATE VIEW expensive_items AS
SELECT * FROM items WHERE price >= 100
WITH LOCAL CHECK OPTION;

- CREATE VIEW expensive_items AS
SELECT * FROM items WHERE price >= 100;
- CREATE VIEW non_luxury_items AS
SELECT * FROM expensive_items WHERE price < 1000
WITH CASCADED CHECK OPTION;
- INSERT INTO non_luxury_items(id, name, price)
VALUES (12, 'pencil', 2.00);
# This will work

- CREATE VIEW expensive_items AS
SELECT * FROM items WHERE price >= 100;
- CREATE VIEW non_luxury_items AS
SELECT * FROM expensive_items WHERE price < 1000
WITH CASCADED CHECK OPTION;
- INSERT INTO non_luxury_items(id, name, price)
VALUES (12, 'pencil', 2.00);
# CASECADED ALSO CHECKS FOR OTHER VIEWS
# This will not work

# inserting or updating data of the view can be validated using LOCAL OR CASCADED check option
```

### Built-in Functions
* COUNT
* SUM
* AVG
* MAX
* MIN

```sql
- SELECT customers.first_name, customers.last_name, COUNT(purchases.id) AS purchase_count
FROM customers
INNER JOIN purchases ON customers.id = purchases.customer_id
GROUP BY customers.id;

- SELECT MAX(items.price) FROM items
INNER JOIN purchases ON items.id = purchases.item_id;
```

### HAVING CONSTRUCT
```sql
# HAVING construct allow to filter after the aggregation has taken place

SELECT customers.first_name, customers.last_name, COUNT(purchases.id) AS purchse_count
FROM customers
INNER JOIN purchases ON customers.id = purchases.customer_id
GROUP BY customers.id
HAVING COUNT(purchases.id) > 3;
```

### Date types
* timestamp
* date
* time
* interval

```sql
- SELECT timestamp '2005-10-08 05:16:45';
- SELECT NOW();
- SELECT TO_CHAR(NOW(), 'FMDay DDth FMMonth, DD-MM-YYYY HH:MI:SS');
- SELECT TO_TIMESTAMP('Wednesday 24th April, 2019 12:08:32', 'FMDay DDth FMMonth, YYYY HH:MI:SS');
```

### Other data types
* BYTEA
* ENUM
* JSON

```sql
# ENUM - can put specific set of strings
- CREATE TYPE mood AS ENUM('extremely unhappy', 'unhappy', 'ok', 'happy', 'extremely happy');
# only these 4 types can be inserted in mood type
- CREATE TABLE students (
	name character varying(255),
	current_mood mood
);
- INSERT INTO students
VALUES ('Raiyyan', 'happy');
- SELECT * FROM students
WHERE current_mood > 'ok'; # 'happy', 'extremely happy'
```

### NESTED SELECT
```sql
- SELECT * FROM items WHERE price >
(SELECT AVG(price) FROM items);

- CREATE VIEW expensive_items_diff AS
SELECT *, items.price -
(SELECT AVG(price) FROM items
WHERE price > 100) AS "average_diff"
FROM items WHERE price > 100;
```