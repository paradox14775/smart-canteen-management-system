# SOFTWARE REQUIREMENTS SPECIFICATION (SRS)
## Smart Canteen Management System with QR-Based Ordering, Automated Inventory Control and Predictive Sales Analytics
### Aligned with IEEE Std 830-1998 & GGSIPU MCA 269 Evaluation Framework

---

## Document Information
- **Project Title:** Smart Canteen Management System (SCMS)
- **Document Version:** 1.0.0
- **Status:** Approved for Design & Development
- **Target Course:** IPU MCA 269 Minor Project
- **Authors:** Project Team (4 Members)

---

# 1. Introduction

### 1.1 Purpose
This Software Requirements Specification (SRS) document details the functional, non-functional, interface, and data requirements for the **Smart Canteen Management System (SCMS)**. It serves as the authoritative baseline for system design, database modeling, software implementation, quality assurance testing, and academic project evaluation under Guru Gobind Singh Indraprastha University (GGSIPU).

### 1.2 Scope of the System
The SCMS is a centralized, responsive web platform engineered to eliminate operational bottlenecks in university cafeterias. The software encompasses:
- Mobile-first, contactless QR-code dining and takeaway order placement.
- Real-time digital Kitchen Display System (KDS) order pipeline tracking.
- Automated Bill of Materials (BOM) recipe-driven inventory management.
- Machine Learning (ML) predictive demand and daily sales forecasting.
- Business Intelligence (BI) executive analytics and sales reporting.
- Strict Role-Based Access Control (RBAC) across four distinct operational roles.

### 1.3 Definitions, Acronyms, and Abbreviations
- **ACID:** Atomicity, Consistency, Isolation, Durability.
- **BOM:** Bill of Materials (formula linking 1 menu item to its raw ingredient quantities).
- **FIFO:** First-In, First-Out queue processing.
- **KDS:** Kitchen Display System.
- **MAE:** Mean Absolute Error.
- **MAPE:** Mean Absolute Percentage Error.
- **MVT:** Model-View-Template architectural pattern in Django.
- **ORM:** Object-Relational Mapping.
- **QR Code:** Quick Response Code (two-dimensional matrix barcode).
- **RBAC:** Role-Based Access Control.
- **RMSE:** Root Mean Squared Error.
- **SRS:** Software Requirements Specification.
- **UAT:** User Acceptance Testing.

### 1.4 References
1. IEEE Std 830-1998: *IEEE Recommended Practice for Software Requirements Specifications*.
2. Guru Gobind Singh Indraprastha University: *Syllabus and Evaluation Rubrics for MCA 269 Minor Project*.
3. Django 5.x Official Documentation: *The Web framework for perfectionists with deadlines*.
4. Scikit-learn: *Machine Learning in Python*, Pedregosa et al., JMLR 12, pp. 2825-2830, 2011.

---

# 2. Overall Description

### 2.1 Product Perspective
The system functions as a self-contained, high-performance web application operating in campus local intranet or cloud-hosted network environments. It bridges consumers (students and campus faculty) directly with service providers (canteen cashiers, kitchen chefs, and facility administrators).

```
[Student Mobile Device] ──(QR Scan / HTTP)──┐
                                            │
[Kitchen Display Screen] ──(KDS HTTP)───────┼──> [Django Application Server] <──> [MySQL 8 Relational DB]
                                            │                 │
[Admin / Management PC] ──(Web Portal)──────┘                 └──> [Scikit-learn ML Forecasting Engine]
```

### 2.2 Product Functions
1. **User Identity & Role Access:** Registration, session authentication, and permission enforcement for Student, Admin, Kitchen, and Management.
2. **Digital Menu & Dynamic QR Catalog:** Category grouping, dynamic pricing, live stock availability toggles, and table-assigned QR generation.
3. **Contactless Ordering & Cart:** Cart accumulation, table attribution, dietary notes, and real-time total computation.
4. **Kitchen Ticket Lifecycle:** Live KDS ticket stream advancing through `PENDING` $\rightarrow$ `CONFIRMED` $\rightarrow$ `PREPARING` $\rightarrow$ `READY` $\rightarrow$ `COMPLETED`.
5. **Simulated Payment Gateway:** Multi-channel checkout handling UPI simulation, Student Wallet, and Cash at Pickup.
6. **Automated Inventory Control (BOM):** Automated decrement of raw ingredient quantities based on recipes upon order confirmation.
7. **Threshold Alerting:** Real-time in-app warnings when stock drops below safety buffers.
8. **Predictive Sales Forecasting:** Supervised machine learning models predicting daily volume per item to prevent over/under preparation.
9. **Executive Analytics:** Dashboards tracking daily gross margins, top revenue generators, peak traffic hours, and wastage rates.

### 2.3 User Classes and Characteristics

| User Role | Technical Literacy | Responsibilities & Access Privileges |
| :--- | :--- | :--- |
| **Student / Customer** | General smartphone literacy | Scan QR, browse menu, customize cart, checkout, monitor order preparation, view historical invoices. |
| **Kitchen Staff** | Basic computer/tablet literacy | Monitor live KDS incoming orders, confirm tickets, update preparation progress, mark orders ready for pickup. |
| **Canteen Admin** | Moderate administrative literacy | Manage menu catalog, update pricing/availability, monitor raw material stock, log inward purchases, configure system parameters. |
| **Management / Analyst** | Analytical literacy | Inspect sales charts, monitor financial health, review ML demand forecasts, evaluate wastage metrics, export PDF/Excel reports. |

### 2.4 Operating Environment
- **Server OS:** Ubuntu 22.04 LTS / Windows 11 Server.
- **Application Engine:** Python 3.11+, Django 5.1+, Gunicorn / ASGI / WSGI.
- **Database Engine:** MySQL 8.0+ running InnoDB with UTF-8 character encoding.
- **Client Devices:** Any modern device running Google Chrome, Mozilla Firefox, Apple Safari, or Microsoft Edge.

### 2.5 Design and Implementation Constraints
1. **Transactional Integrity:** Placing an order and updating raw inventory must execute within an ACID database transaction block (`django.db.transaction.atomic`) to prevent orphaned stock discrepancies.
2. **No Native Mobile App Requirement:** All customer interactions must occur inside standard mobile web browsers without necessitating Google Play Store or Apple App Store installations.
3. **Simulated Financial Transactions:** Due to sandbox and academic demonstration boundaries, payments are verified through a mock verification gateway simulating instant UPI and Cash approvals.
4. **Hardware Portability:** The solution must run reliably on typical university computer lab machines without requiring proprietary POS hardware.

---

# 3. External Interface Requirements

### 3.1 User Interfaces
- **Mobile Student Web App:** Mobile-first layout optimized for 360px–480px viewports with touch-friendly sticky cart bars and quick quantity increments.
- **Kitchen Display System (KDS):** High-contrast dark mode dashboard formatted for 1080p wall displays or kitchen tablets, color-coding orders by wait time and status.
- **Administrative Portal:** Desktop-first management console with data tables, search filters, modal forms for ingredient mapping, and alert banners.
- **Analytics & BI Portal:** Rich graphical dashboard utilizing Chart.js with toggleable daily, weekly, and monthly timeframes.

### 3.2 Software Interfaces
- **Database Interface:** MySQL Connector via Django's Object-Relational Mapper (ORM).
- **QR Generation Engine:** Python `qrcode` and `Pillow` libraries producing PNG stream responses.
- **ML Engine:** Python `scikit-learn`, `pandas`, and `joblib` executing trained models for inference.

---

# 4. Detailed Functional Requirements

| Req ID | Module | Title & Description | Processing & Logic | Priority | Role |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **FR01** | Auth | **User Registration & Login** | Validates email, enrollment/roll number, hashes password using PBKDF2 SHA-256, assigns session tokens. | High | All |
| **FR02** | Auth | **Role-Based Access Control** | Enforces `@role_required` view decorators ensuring students cannot access admin/kitchen endpoints and vice-versa. | High | All |
| **FR03** | Menu | **Category & Dish Management** | Full CRUD operations on categories and dishes. Includes price, photo, prep-time estimate, and live availability toggle. | High | Admin |
| **FR04** | QR | **Table-Specific QR Generation** | Generates dynamic QR codes encoding URLs (e.g. `/order/?table=T05`). Auto-populates table number upon scan. | High | Admin / Student |
| **FR05** | Order | **Cart & Checkout Placement** | Validates product availability, checks ingredient inventory sufficiency, calculates subtotal and taxes, dispatches order. | High | Student |
| **FR06** | KDS | **Order Processing & Transitions** | Renders live orders in FIFO queue. Allows kitchen staff to step status: `Pending` $\rightarrow$ `Confirmed` $\rightarrow$ `Preparing` $\rightarrow$ `Ready` $\rightarrow$ `Completed`. | High | Kitchen |
| **FR07** | Billing | **Invoice & Payment Processing** | Creates unique billing token, records payment method (UPI mock, Cash, Wallet), marks payment state `SUCCESS`. | High | Student / Admin |
| **FR08** | Inventory| **Recipe BOM Stock Deduction** | Upon order state advancing to `Confirmed`, deducts each mapped ingredient quantity from current stock inside an atomic transaction. | High | System / Kitchen |
| **FR09** | Inventory| **Low-Stock Alerting** | Periodically and event-driven evaluates if `current_stock <= minimum_threshold`. Emits in-app warning banner to admin. | Medium | Admin |
| **FR10** | Analytics| **Sales & Revenue Aggregations** | Computes daily, weekly, monthly gross revenue, total transaction counts, average order value (AOV), and fast-moving items. | High | Management / Admin |
| **FR11** | ML | **Food Demand Prediction** | Ingests rolling 7-day sales, day-of-week, weather, and college event flags. Produces item-level quantity estimates for the next operational day. | Medium | Management |
| **FR12** | Inventory| **Wastage & Variance Tracking** | Compares theoretical ingredient consumption against actual end-of-day stock counts to compute shrinkage and spoilage percentage. | Medium | Management / Admin |
| **FR13** | Analytics| **Management Visual Dashboard** | Visualizes sales volume, peak lunch ordering hours (11:00 AM – 2:00 PM), category contribution, and forecast overlays using Chart.js. | High | Management |
| **FR14** | Order | **Order History & Receipt Audit** | Stores persistent order logs allowing students to inspect past orders and admins to reprint digital receipts. | High | Student / Admin |

---

# 5. Non-Functional Requirements (NFR)

### 5.1 Performance Requirements
- **PR-01 (Response Time):** Digital menu browsing and cart interactions must respond in $\le 800\text{ ms}$ under standard campus network load.
- **PR-02 (Order Confirmation Latency):** Checkout and atomic inventory validation must complete in $\le 500\text{ ms}$.
- **PR-03 (Concurrent Sessions):** The system must smoothly handle at least 200 concurrent active student sessions during peak 12:30 PM – 1:30 PM lunch break hours.

### 5.2 Security & Protection Requirements
- **SEC-01 (Password Encryption):** Passwords stored using PBKDF2 with SHA-256 hashing and unique per-user salts.
- **SEC-02 (Injection Defense):** All database transactions executed strictly through Django ORM parameterized queries to defeat SQL Injection (SQLi).
- **SEC-03 (Cross-Site Request Forgery):** Every state-changing form and asynchronous POST request must carry a valid Django CSRF token.
- **SEC-04 (Cross-Site Scripting):** Dynamic HTML content escaped by default via the Django templating engine.

### 5.3 Reliability, Availability & Maintainability
- **REL-01 (Transactional Integrity):** Any mid-flight order cancellation or database exception must roll back inventory decrements completely, leaving zero residual inaccuracies.
- **AVL-01 (Availability):** Operational uptime $\ge 99.5\%$ during campus business hours (08:00 to 18:00 IST).
- **MTN-01 (Modularity):** Modular codebase structured across independent Django apps (`authentication`, `menu`, `orders`, `inventory`, `analytics`, `ml_engine`).

---

# 6. Detailed Database Schema (12 Relational Tables)

### Table 1: `users`
| Column Name | Data Type | Constraints | Description |
| :--- | :--- | :--- | :--- |
| `id` | BIGINT | PRIMARY KEY, AUTO_INCREMENT | Unique user identifier |
| `username` | VARCHAR(150) | UNIQUE, NOT NULL | Campus login username |
| `email` | VARCHAR(254) | UNIQUE, NOT NULL | Official campus email address |
| `password` | VARCHAR(128) | NOT NULL | Salted PBKDF2 SHA-256 hash |
| `role` | VARCHAR(20) | NOT NULL, DEFAULT 'STUDENT' | Enum: `STUDENT`, `ADMIN`, `KITCHEN`, `MANAGEMENT` |
| `first_name` | VARCHAR(150) | NOT NULL | Given name |
| `last_name` | VARCHAR(150) | NOT NULL | Surname |
| `is_active` | BOOLEAN | NOT NULL, DEFAULT TRUE | Account state |
| `created_at` | DATETIME | NOT NULL, CURRENT_TIMESTAMP | Registration timestamp |

### Table 2: `students`
| Column Name | Data Type | Constraints | Description |
| :--- | :--- | :--- | :--- |
| `id` | BIGINT | PRIMARY KEY, AUTO_INCREMENT | Student profile identifier |
| `user_id` | BIGINT | UNIQUE, FK -> `users(id)` | Linked user account |
| `enrollment_no` | VARCHAR(20) | UNIQUE, NOT NULL | University Enrollment / Roll Number |
| `course` | VARCHAR(50) | NOT NULL | Program of study (e.g., MCA, B.Tech) |
| `phone_number` | VARCHAR(15) | NULLABLE | Contact telephone |

### Table 3: `categories`
| Column Name | Data Type | Constraints | Description |
| :--- | :--- | :--- | :--- |
| `id` | BIGINT | PRIMARY KEY, AUTO_INCREMENT | Category identifier |
| `name` | VARCHAR(100) | UNIQUE, NOT NULL | Category name (Meals, Snacks, Drinks) |
| `description` | TEXT | NULLABLE | Detailed description |
| `is_active` | BOOLEAN | NOT NULL, DEFAULT TRUE | Display toggle |

### Table 4: `products`
| Column Name | Data Type | Constraints | Description |
| :--- | :--- | :--- | :--- |
| `id` | BIGINT | PRIMARY KEY, AUTO_INCREMENT | Product item identifier |
| `category_id` | BIGINT | FK -> `categories(id)` | Parent category |
| `name` | VARCHAR(150) | NOT NULL | Dish name (e.g., Paneer Thali) |
| `description` | TEXT | NULLABLE | Dish ingredients / description |
| `price` | DECIMAL(10, 2) | NOT NULL | Selling price in INR (₹) |
| `preparation_time` | INT | NOT NULL, DEFAULT 10 | Estimated prep time (minutes) |
| `is_available` | BOOLEAN | NOT NULL, DEFAULT TRUE | Daily kitchen availability flag |
| `image` | VARCHAR(255) | NULLABLE | File path to food image |

### Table 5: `orders`
| Column Name | Data Type | Constraints | Description |
| :--- | :--- | :--- | :--- |
| `id` | BIGINT | PRIMARY KEY, AUTO_INCREMENT | Order transaction identifier |
| `order_token` | VARCHAR(20) | UNIQUE, NOT NULL | Public alphanumeric token (e.g. SC-0104) |
| `user_id` | BIGINT | FK -> `users(id)` | Ordering student |
| `table_number` | VARCHAR(10) | NULLABLE | QR Table source (e.g. T-04, Takeaway) |
| `total_amount` | DECIMAL(10, 2) | NOT NULL | Final invoice total |
| `status` | VARCHAR(20) | NOT NULL, DEFAULT 'PENDING' | Status: `PENDING`, `CONFIRMED`, `PREPARING`, `READY`, `COMPLETED`, `CANCELLED` |
| `order_date` | DATETIME | NOT NULL, CURRENT_TIMESTAMP | Timestamp of submission |

### Table 6: `order_items`
| Column Name | Data Type | Constraints | Description |
| :--- | :--- | :--- | :--- |
| `id` | BIGINT | PRIMARY KEY, AUTO_INCREMENT | Line item record identifier |
| `order_id` | BIGINT | FK -> `orders(id)` ON DELETE CASCADE | Associated parent order |
| `product_id` | BIGINT | FK -> `products(id)` | Selected food item |
| `quantity` | INT | NOT NULL, CHECK (quantity > 0) | Quantity ordered |
| `unit_price` | DECIMAL(10, 2) | NOT NULL | Price snapshot at time of purchase |

### Table 7: `payments`
| Column Name | Data Type | Constraints | Description |
| :--- | :--- | :--- | :--- |
| `id` | BIGINT | PRIMARY KEY, AUTO_INCREMENT | Payment transaction identifier |
| `order_id` | BIGINT | UNIQUE, FK -> `orders(id)` | Linked order |
| `amount` | DECIMAL(10, 2) | NOT NULL | Transacted monetary amount |
| `payment_mode` | VARCHAR(20) | NOT NULL | Mode: `UPI_MOCK`, `CASH`, `STUDENT_WALLET` |
| `transaction_ref` | VARCHAR(100) | UNIQUE, NOT NULL | Mock gateway reference ID |
| `payment_status` | VARCHAR(20) | NOT NULL, DEFAULT 'SUCCESS' | Status: `SUCCESS`, `PENDING`, `FAILED` |
| `paid_at` | DATETIME | NOT NULL, CURRENT_TIMESTAMP | Settlement timestamp |

### Table 8: `ingredients`
| Column Name | Data Type | Constraints | Description |
| :--- | :--- | :--- | :--- |
| `id` | BIGINT | PRIMARY KEY, AUTO_INCREMENT | Ingredient identifier |
| `name` | VARCHAR(100) | UNIQUE, NOT NULL | Raw item name (Potatoes, Rice, Milk) |
| `unit` | VARCHAR(20) | NOT NULL | Unit of measure: `kg`, `g`, `L`, `ml`, `pcs` |
| `current_stock` | DECIMAL(12, 3) | NOT NULL, DEFAULT 0.000 | Available quantity on hand |
| `minimum_threshold` | DECIMAL(12, 3) | NOT NULL, DEFAULT 5.000 | Safety stock alerting point |
| `unit_cost` | DECIMAL(10, 2) | NOT NULL, DEFAULT 0.00 | Procurement cost per unit |

### Table 9: `recipes` (Bill of Materials)
| Column Name | Data Type | Constraints | Description |
| :--- | :--- | :--- | :--- |
| `id` | BIGINT | PRIMARY KEY, AUTO_INCREMENT | Recipe mapping identifier |
| `product_id` | BIGINT | FK -> `products(id)` | Menu dish |
| `ingredient_id` | BIGINT | FK -> `ingredients(id)` | Raw ingredient required |
| `quantity_required`| DECIMAL(10, 3) | NOT NULL | Consumption required per 1 dish unit |

### Table 10: `stock_transactions`
| Column Name | Data Type | Constraints | Description |
| :--- | :--- | :--- | :--- |
| `id` | BIGINT | PRIMARY KEY, AUTO_INCREMENT | Stock audit log identifier |
| `ingredient_id` | BIGINT | FK -> `ingredients(id)` | Targeted ingredient |
| `quantity` | DECIMAL(12, 3) | NOT NULL | Quantity increment or decrement |
| `transaction_type` | VARCHAR(20) | NOT NULL | `INWARD_PURCHASE`, `ORDER_DEDUCTION`, `SPOILAGE_LOSS` |
| `reference_order_id`| BIGINT | NULLABLE, FK -> `orders(id)`| Originating order (if deduction) |
| `logged_at` | DATETIME | NOT NULL, CURRENT_TIMESTAMP | Audit timestamp |

### Table 11: `notifications`
| Column Name | Data Type | Constraints | Description |
| :--- | :--- | :--- | :--- |
| `id` | BIGINT | PRIMARY KEY, AUTO_INCREMENT | Notification identifier |
| `user_id` | BIGINT | FK -> `users(id)` | Target recipient |
| `title` | VARCHAR(150) | NOT NULL | Short alert heading |
| `message` | TEXT | NOT NULL | Detailed notification message |
| `is_read` | BOOLEAN | NOT NULL, DEFAULT FALSE | Read state toggle |
| `created_at` | DATETIME | NOT NULL, CURRENT_TIMESTAMP | Timestamp generated |

### Table 12: `demand_forecasts`
| Column Name | Data Type | Constraints | Description |
| :--- | :--- | :--- | :--- |
| `id` | BIGINT | PRIMARY KEY, AUTO_INCREMENT | Forecast identifier |
| `product_id` | BIGINT | FK -> `products(id)` | Forecasted menu item |
| `forecast_date` | DATE | NOT NULL | Target calendar day for prediction |
| `predicted_quantity`| INT | NOT NULL | ML estimated units demanded |
| `actual_quantity` | INT | NULLABLE | Actual realized sales (backfilled) |
| `model_name` | VARCHAR(50) | NOT NULL | Algorithm used (e.g. `RandomForestRegressor`) |
| `generated_at` | DATETIME | NOT NULL, CURRENT_TIMESTAMP | Execution timestamp |

---

# 7. Algorithmic Specifications & Mathematical Models

### 7.1 Atomic Recipe-to-Stock Deduction Algorithm
When an order transition to `CONFIRMED` is triggered:
```python
# Pseudo-code logic within atomic database transaction
with transaction.atomic():
    order = Order.objects.select_for_update().get(id=order_id)
    if order.status != 'PENDING':
        raise InvalidStateTransition()
        
    for item in order.order_items.all():
        recipes = Recipe.objects.filter(product=item.product)
        for recipe in recipes:
            ingredient = Ingredient.objects.select_for_update().get(id=recipe.ingredient_id)
            total_deduction = recipe.quantity_required * item.quantity
            
            if ingredient.current_stock < total_deduction:
                raise InsufficientStockError(f"Insufficient stock for {ingredient.name}")
                
            ingredient.current_stock -= total_deduction
            ingredient.save()
            
            StockTransaction.objects.create(
                ingredient=ingredient,
                quantity=-total_deduction,
                transaction_type='ORDER_DEDUCTION',
                reference_order=order
            )
            
    order.status = 'CONFIRMED'
    order.save()
```

### 7.2 Mathematical Formulation for Machine Learning Demand Prediction
Let $Y_{i, t}$ represent the demand for food product $i$ on day $t$.
The feature vector $\mathbf{X}_{i, t}$ is constructed as:
$$\mathbf{X}_{i, t} = \Big[ DOW_t, \text{MA7}_{i, t-1}, \text{MA30}_{i, t-1}, Y_{i, t-1}, Y_{i, t-7}, \text{EventFlag}_t, \text{ExamFlag}_t \Big]$$
Where:
- $DOW_t \in \{0, 1, \dots, 6\}$: Day of the week (Monday through Sunday).
- $\text{MA7}_{i, t-1} = \frac{1}{7} \sum_{k=1}^7 Y_{i, t-k}$: 7-day moving average sales.
- $\text{MA30}_{i, t-1} = \frac{1}{30} \sum_{k=1}^{30} Y_{i, t-k}$: 30-day moving average sales.
- $\text{EventFlag}_t \in \{0, 1\}$: Binary indicator for campus events / festivals.
- $\text{ExamFlag}_t \in \{0, 1\}$: Binary indicator for examination periods.

The models evaluated:
1. **Multiple Linear Regression (OLS):**
   $$\hat{Y}_{i, t} = \beta_0 + \mathbf{X}_{i, t} \boldsymbol{\beta} + \epsilon$$
2. **Random Forest Regressor:**
   $$\hat{Y}_{i, t} = \frac{1}{B} \sum_{b=1}^B T_b(\mathbf{X}_{i, t})$$

### 7.3 Model Performance Evaluation Metrics
To satisfy academic rigor under IPU evaluation:
- **Mean Absolute Error (MAE):**
  $$\text{MAE} = \frac{1}{N} \sum_{k=1}^N \left| Y_k - \hat{Y}_k \right|$$
- **Root Mean Squared Error (RMSE):**
  $$\text{RMSE} = \sqrt{\frac{1}{N} \sum_{k=1}^N \left( Y_k - \hat{Y}_k \right)^2}$$
- **Mean Absolute Percentage Error (MAPE):**
  $$\text{MAPE} = \frac{100\%}{N} \sum_{k=1}^N \left| \frac{Y_k - \hat{Y}_k}{Y_k} \right|$$

---

*SRS Specification Approved by MCA Minor Project Review Committee.*

