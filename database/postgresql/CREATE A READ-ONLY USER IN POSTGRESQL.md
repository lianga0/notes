## How to CREATE A READ-ONLY USER For POSTGRESQL

> https://www.datapine.com/documentation/database-user-read-only/

### CREATE A READ-ONLY USER IN POSTGRESQL
 

#### 1) Create a new User
 

Connect to your PostgreSQL server with the following command.

```
SUDO –U POSTGRES SQL  
```

Select the database you want to connect to datapine. 

```
\c <db name>
```

Create a new user to connect to datapine. 

```
CREATE ROLE <user name> LOGIN PASSWORD <password>;
```


### 2) Assign the necessary privileges to the new user

Grant connect to database

```
GRANT CONNECT ON DATABASE <db name>  to  <user name>;
```

Grant usage on schema

```
GRANT USAGE ON SCHEMA <schema name> TO <user name>;
```

Grant select on all tables in the schema

```
GRANT SELECT ON ALL TABLES IN SCHEMA <schema name> TO <user>;
```

Grant the user the access to all new tables added in future

```
ALTER DEFAULT PRIVILEGES IN SCHEMA <schema name> 
GRANT SELECT ON TABLES TO <user name>;
```
