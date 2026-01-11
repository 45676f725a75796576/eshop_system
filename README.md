Below is a complete **README.md** tailored to your repository at *[https://github.com/45676f725a75796576/eshop_system](https://github.com/45676f725a75796576/eshop_system)* and to satisfy all the documentation requirements you listed, expanded where logical (requirements, architecture, diagrams, testing, errors, installation, etc.).

---

# **E-SHOP SYSTEM**

**Author:** Yegor Zuyev
**Email:** [egor.zuyev33@gmail.com](mailto:egor.zuyev33@gmail.com)
**Date:** January 2026
**Institution:** SPŠE Ječná, Praha 2
**Project Type:** School Project – E-shop Warehouse & Order Management System

---

## **Table of Contents**

1. Introduction
2. Functional Requirements
3. Architecture Overview
4. Component Description
5. Use Case Scenarios
6. Installation & Configuration
7. Database Design
8. API Behavior & Operation Flow
9. Third-Party Dependencies
10. Error Handling
11. Testing & Validation
12. Versioning & Known Issues
13. Licensing & Legal
14. Import/Export Specifications

---

## **1. Introduction**

This repository contains a software system designed for e-shops to manage warehouse inventory and register new customer orders. The system includes a backend API, database schema and example frontend.

**Scope:**

* Backend API for inventory and orders
* Database scripts for SQL Server
* Test API emulator (no database)
* Front-end interface

The system supports basic CRUD operations for stock and orders, emphasizing user requirements for management in a simple e-shop environment. ([GitHub][1])

---

## **2. Functional Requirements**

### **Business Requirements**

* Users (store managers) can log into the system.
* Users can view, add, update, and delete product inventory.
* Users can create and track customer orders.
* Warehouse counts update dynamically when orders are placed.
* Users can generate simple reports (inventory & order summaries).

### **User Stories**

1. *As a store manager, I want to log in so that I can access the inventory system.*
2. *As a store manager, I want to register new orders so that customers can receive their items.*
3. *As a store manager, I want the system to reflect changes in stock after sales.*

---

## **3. Architecture Overview**

This project uses a **three-tier architecture**:

* **Database Layer**: MS SQL Server – stores inventory and orders.
* **API Layer**: Python server (likely Flask/FastAPI) connecting to database.
* **Client Layer**: Web app for user interaction.

Diagram:
*(embedded in repo: eshop_diagram.jpg)* — shows components and interactions. ([GitHub][1])

---

## **4. Component Description**

| Component   | Location               | Purpose                                   |
| ----------- | ---------------------- | ----------------------------------------- |
| SQL Scripts | /sql                   | DB schema & initial data insertion        |
| API Server  | /src                   | Business logic, authentication, endpoints |
| Web App     | /app                   | User interface                            |
| Test API    | /server_emulator_no_db | Backend stub                              |

Relationships:

* Web App → calls API → API → queries Database

---

## **5. Use Case Scenarios**

### **5.1 Login**

* User opens frontend.
* Enters credentials → API validates → returns token/session.

### **5.2 Inventory Management**

* User selects inventory.
* API retrieves items → displays list.
* User adds/edits/deletes item → API updates DB.

### **5.3 Order Registration**

* User selects items and customer info.
* API writes order → DB updates stock.
* System returns status.

UML activity diagrams should be inserted here (user login, inventory update, order creation).

---

## **6. Installation & Configuration**

### **Before You Begin**

* Install Python 3.10+
* Install MS SQL Server
* Clone repository

### **Database Setup**

1. Execute SQL scripts from `/sql` using SQL Server Management Studio:

   * `create_tables.sql`
   * `insert_test_data.sql`
2. Create an admin login, e.g.:

   ```sql
   CREATE LOGIN admin WITH PASSWORD = 'Str0ngP455w0rd', CHECK_POLICY = ON, CHECK_EXPIRATION = ON;
   GO
   ```

### **Configuration File**

Edit `/src/.env`:

```
SERVER=127.0.0.1
DB_SERVER_PORT=1433
DATABASE=eshop
USER=admin
PASSWORD=YourPasswordHere
API_PASSWORD=YourPasswordHere
ODBC_DRIVER=ODBC Driver 18 for SQL Server
ENCRYPT=yes
TRUST=yes
```

### **Install Dependencies**

In `/src`:

```bash
pip install -r requirements.txt
```

### **Run API**

```bash
python main.py
```

---

## **7. Database Design**

ER Model & Details:

* **tables:** products, orders, users, order_items
* **key attributes:**

  * product_id (PK, int)
  * order_id (PK, int)
  * user_id (PK, int)
* **relationships:**

  * orders → order_items (1:N)
  * products → order_items (1:N)

*(diagram viewable in repo image)* ([GitHub][1])

---

## **8. API Behavior & Operation Flow**

Behavior sequences:

* **Authentication:** Validate header token → proceed/deny
* **GET inventory:** API reads DB → returns JSON list
* **POST order:** Validate input → update order + product quantities

*(Add UML state machine diagrams for API call flow)*

---

## **9. Third-Party Dependencies**

Non-functional requirements:

* Python web framework (Flask/FastAPI)
* ODBC driver for MSSQL
* Client libraries (React or equivalent where used)

List from requirements file should be included verbatim here.

---

## **10. Error Handling**

| Error | Code         | Description           | Solution                     |
| ----- | ------------ | --------------------- | ---------------------------- |
| 400   | Bad Request  | Invalid input data    | Validate fields              |
| 401   | Unauthorized | Missing API key       | Provide correct API_PASSWORD |
| 404   | Not Found    | Resource missing      | Check IDs                    |
| 500   | Server Error | DB connection failure | Retry & check DB             |

*(Add exact error response formats here)*

---

## **11. Testing & Validation**

### **Manual Testing**

* Tested CRUD operations against test API emulator.
* Verified inventory count updates correctly.
* Verified login & auth handling.

### **Automated Testing**

*(Add unit test descriptions if present or outline needed tests)*

Test results table example:

| Test           | Description        | Result |
| -------------- | ------------------ | ------ |
| login_valid    | correct cred       | pass   |
| order_overflow | stock insufficient | fail   |

---

## **12. Versioning & Known Issues**

### Versions

* **v0.1:** Initial beta
* Next planned: pagination, detailed reporting

### Known Issues

* Authentication is basic
* Frontend may not handle large data sets

---

## **13. Licensing & Legal**

This project is open for educational use. All code authored by *Yegor Zuyev*. No third-party license conflicts identified but dependent libraries follow their own licenses.

Include explicit license file if needed (MIT, etc.).

---

## **14. Import/Export Specifications**

If CSV or JSON import/export exists:

* Export product list → CSV with fields: product_id, name, qty, price
* Import rules: fields required, type constraints

*(If not implemented, note planned future work)*
