# E-SHOP DATABASE SYSTEM
System for e-shops to manage warehouse and register new orders.

## SET-UP

1. Create database using sql code from repository.
     - code is compatible only with MS SQL

![db diagram](https://github.com/45676f725a75796576/eshop_system/blob/main/eshop_diagram.jpg "db diagram")

Don't forget to create login for user `admin`.

Example code for login:
```
CREATE LOGIN admin
WITH PASSWORD = 'Str0ngP455w0rd',
     CHECK_POLICY = ON,
     CHECK_EXPIRATION = ON;
GO
```
*use it on master*

### CONFIGURATION FILE

Before doing something check configuration file in `./src/.env`.

Check if server address is correct, it can be IPv4, IPv6 or domain.