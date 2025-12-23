# E-SHOP DATABASE SYSTEM

System for e-shops to manage warehouses and register new orders.

---

## Setup

1. Create the database using the SQL code from the repository.  
2. The code is compatible **only with Microsoft SQL Server**.  
3. Refer to the database diagram for structure.  

![Database diagram](https://github.com/45676f725a75796576/eshop_system/blob/main/eshop_diagram.jpg?raw=true "database diagram")

**Important:** Don’t forget to create a login for the user `admin`.  

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