# E-SHOP DATABASE SYSTEM
*Yegor Zuyev, e-mail: egor.zuyev33@gmail.com*

System for e-shops to manage warehouses and register new orders.

---

## Setup

1. Create the database using the SQL code from the repository.  
2. The code is compatible **only with Microsoft SQL Server**.  
3. Refer to the database diagram for structure.  

![Database diagram](https://github.com/45676f725a75796576/eshop_system/blob/main/eshop_diagram.jpg?raw=true "database diagram")

**Important:** Don’t forget to create a login for the user `admin` or alternatively you can create user and login in Microsoft SQL Server Management Studio.  

**Example SQL code for login:**

```sql
CREATE LOGIN admin
WITH PASSWORD = 'Str0ngP455w0rd',
     CHECK_POLICY = ON,
     CHECK_EXPIRATION = ON;
GO

```
*execute this on `master` database*

### CONFIGURATION FILE

Before performing any operations, check the configuration file at `./src/.env`.

Ensure that the server address is correct; it can be an IPv4 address, IPv6 address, or domain name.

!After creating new login for admin, update password in configuration file!

```
SERVER=127.0.0.1 # database server ip address
DB_SERVER_PORT=1433 # database server port
DATABASE=eshop # database
USER=admin # database user
PASSWORD=Q9!rT4Z@eM2K#L8x # password for database user
API_PASSWORD=Q9!rT4Z@eM2K#L8x # password for API to authorize
ODBC_DRIVER=ODBC Driver 18 for SQL Server # Driver to connect database
ENCRYPT=yes # encrypt communication between API and database server
TRUST=yes
```

### Test Data

Script for inserting test data for database is saved in `./database_insert_test_data.sql`.
Use it to test functionality.

*Test data are made by ChatGPT*

#### Test API

Project contains test API without real database for testing functionality of user app, without creating real database.

**This test API is created by ChatGPT**