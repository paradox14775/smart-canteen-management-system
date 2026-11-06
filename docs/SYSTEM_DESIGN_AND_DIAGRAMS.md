# SYSTEM DESIGN & ARCHITECTURE DOCUMENT (HLD & LLD)
## Smart Canteen Management System (SCMS)
### IPU MCA 269 Minor Project — System Design Specifications (35% Evaluation Weightage)

---

## 1. High-Level Design (HLD) Architecture

The Smart Canteen Management System utilizes a **Modular Monolithic Architecture** with Model-View-Template (MVT) design patterns, complemented by asynchronous RESTful endpoints.

```mermaid
graph TD
    subgraph Client_Layer ["Client Presentation Layer (Multi-Role Responsive UI)"]
        UI_Student["Student Mobile Web UI<br/>(QR Menu, Cart, Live Tracker)"]
        UI_Kitchen["Kitchen Display System (KDS)<br/>(Live Ticket Pipeline, Order Updates)"]
        UI_Admin["Admin Management Portal<br/>(Menu, Stock Inward, User Accounts)"]
        UI_Mgmt["Management & BI Dashboard<br/>(Sales Trends, ML Predictions, Wastage)"]
    end

    subgraph App_Layer ["Application & Controller Layer (Python / Django 5)"]
        Router["URL Router & Dispatcher"]
        Auth_Engine["Authentication & RBAC Middleware<br/>(Session & Token Validation)"]
        
        subgraph Core_Services ["Core Business Services"]
            Menu_Service["Menu & QR Engine<br/>(Dynamic Table QR Generator)"]
            Order_Service["Order Management Service<br/>(Atomic Transaction Engine)"]
            Billing_Service["Billing & Payment Simulation"]
            Inventory_Service["BOM Recipe & Inventory Engine<br/>(Auto Deduction & Stock Alerts)"]
        end

        subgraph Intelligence_Services ["Intelligence & Analytics Services"]
            ML_Service["Scikit-Learn ML Forecasting Engine<br/>(Feature Pipeline & Inference)"]
            Analytics_Service["Financial & KPI Aggregator<br/>(Daily Revenue, AOV, Spoilage)"]
            Notification_Service["Notification Alert Dispatcher"]
        end
    end

    subgraph Data_Layer ["Data Persistence & Storage Layer"]
        MySQL_DB[("MySQL 8.0 Enterprise Database<br/>(InnoDB Engine, Foreign Keys, ACID)")]
        ML_Model_Store[("Serialized ML Models<br/>(.joblib Model Binaries)")]
    end

    UI_Student -->|HTTP / QR Scan| Router
    UI_Kitchen -->|HTTP / AJAX Polling| Router
    UI_Admin -->|HTTP / Forms| Router
    UI_Mgmt -->|HTTP / Chart.js API| Router

    Router --> Auth_Engine
    Auth_Engine --> Menu_Service
    Auth_Engine --> Order_Service
    Auth_Engine --> Billing_Service
    Auth_Engine --> Inventory_Service
    Auth_Engine --> ML_Service
    Auth_Engine --> Analytics_Service
    Auth_Engine --> Notification_Service

    Menu_Service <--> MySQL_DB
    Order_Service <--> MySQL_DB
    Billing_Service <--> MySQL_DB
    Inventory_Service <--> MySQL_DB
    Analytics_Service <--> MySQL_DB
    Notification_Service <--> MySQL_DB
    ML_Service <--> MySQL_DB
    ML_Service <--> ML_Model_Store
```

---

## 2. Data Flow Diagrams (DFD)

### 2.1 DFD Level 0 (Context Diagram)
The Level 0 DFD illustrates external entities interacting with the boundary of the Smart Canteen Management System.

```mermaid
graph LR
    Student(("Student / Customer"))
    Kitchen(("Kitchen Staff"))
    Admin(("Canteen Admin"))
    Mgmt(("Management / Analyst"))
    
    System["0.0<br/>Smart Canteen Management System"]

    Student -->|"Registration, QR Scans, Orders, Payments"| System
    System -->|"Digital Receipts, Prep Status Updates"| Student

    System -->|"Incoming Order Tickets, Item Customizations"| Kitchen
    Kitchen -->|"Status Updates (Confirmed, Ready, Completed)"| System

    Admin -->|"Menu Items, Prices, Inward Stock, Recipes"| System
    System -->|"Low-Stock Alerts, Inventory Reconciliation"| Admin

    System -->|"Sales Reports, ML Demand Predictions, Spoilage"| Mgmt
    Mgmt -->|"Procurement Budgets & Recipe Modifications"| System
```

---

### 2.2 DFD Level 1 (Decomposition Diagram)
Decomposes the system into its primary subsystems, data flows, and relational data stores.

```mermaid
graph TD
    Student(("Student"))
    Kitchen(("Kitchen Staff"))
    Admin(("Admin"))
    Mgmt(("Management"))

    P1["1.0 User Authentication & RBAC"]
    P2["2.0 Menu & Dynamic QR Catalog"]
    P3["3.0 Order Placement & Processing"]
    P4["4.0 Kitchen Display & Status Tracking"]
    P5["5.0 Recipe-Based Inventory Deduction"]
    P6["6.0 ML Demand Forecasting & Analytics"]

    D1[("D1: Users & Profiles")]
    D2[("D2: Menu & Categories")]
    D3[("D3: Orders & Line Items")]
    D4[("D4: Inventory & Recipes (BOM)")]
    D5[("D5: Sales History & Forecasts")]

    Student -->|"Credentials"| P1
    Admin -->|"User Management"| P1
    P1 <--> D1

    Admin -->|"Category, Dishes, Pricing"| P2
    P2 <--> D2
    Student -->|"Scan Table QR & Read Menu"| P2

    Student -->|"Select Items & Checkout"| P3
    P3 -->|"Create Order Record"| D3
    P3 -->|"Fetch Item Prices"| D2

    D3 -->|"Read Active Tickets"| P4
    Kitchen -->|"Update Status: Preparing / Ready"| P4
    P4 -->|"Update Order State"| D3
    P4 -->|"Customer Status Notification"| Student

    P4 -->|"Trigger Order Confirmation"| P5
    P5 -->|"Fetch Recipes & Deduct Stock"| D4
    P5 -->|"Low-Stock Warning"| Admin

    D3 -->|"Historical Transactions"| P6
    D4 -->|"Raw Material Consumption"| P6
    P6 -->|"Store Model Forecasts"| D5
    P6 -->|"Visual KPI Dashboards & Predictions"| Mgmt
```

---

### 2.3 DFD Level 2 (Order Placement & Inventory Deduction Subsystem)
Highlights the atomic transactional process bridging order confirmation and raw stock consumption.

```mermaid
graph TD
    Student(("Student"))
    KDS(("Kitchen Display"))
    Admin(("Admin"))

    P3_1["3.1 Validate Cart & Stock Sufficiency"]
    P3_2["3.2 Generate Order Token & Payment Record"]
    P3_3["3.3 Post Ticket to Kitchen Queue"]
    P5_1["5.1 Retrieve Dish Recipe (BOM)"]
    P5_2["5.2 Calculate Required Ingredient Deductions"]
    P5_3["5.3 Execute Atomic Stock Decrement"]
    P5_4["5.4 Check Safety Stock Thresholds"]

    D_Menu[("D2: Products")]
    D_Orders[("D3: Orders & Order_Items")]
    D_Payments[("D3.1: Payments")]
    D_Recipes[("D4.1: Recipes (BOM)")]
    D_Stock[("D4.2: Ingredients")]
    D_Log[("D4.3: Stock_Transactions")]

    Student -->|"Submit Cart"| P3_1
    P3_1 <-->|"Check Availability"| D_Menu
    P3_1 <-->|"Check Stock Levels"| D_Stock

    P3_1 -->|"Valid Cart"| P3_2
    P3_2 -->|"Insert Record"| D_Orders
    P3_2 -->|"Record Payment"| D_Payments
    P3_2 -->|"Broadcast New Order"| P3_3

    P3_3 -->|"Display Order Ticket"| KDS
    KDS -->|"Confirm Order"| P5_1

    P5_1 <-->|"Query Ingredients per Dish"| D_Recipes
    P5_1 -->|"Recipe Quantities"| P5_2
    P5_2 -->|"Quantity x Order Units"| P5_3

    P5_3 -->|"Update current_stock"| D_Stock
    P5_3 -->|"Write Audit Entry"| D_Log
    P5_3 -->|"Evaluate current_stock <= threshold"| P5_4

    P5_4 -->|"If Breached: Send Notification"| Admin
```

---

## 3. UML Use-Case Diagram

```mermaid
graph LR
    subgraph Actors
        A1["Student / Customer"]
        A2["Kitchen Staff"]
        A3["Canteen Admin"]
        A4["Management / Analyst"]
    end

    subgraph Smart_Canteen_System ["Smart Canteen Management System Boundary"]
        UC1(["Register / Login (RBAC)"])
        UC2(["Scan QR & View Menu"])
        UC3(["Add Items to Cart & Order"])
        UC4(["Track Order Preparation Status"])
        UC5(["View Personal Order History"])
        
        UC6(["View Kitchen Queue (KDS)"])
        UC7(["Update Order Status (Confirm/Ready)"])
        
        UC8(["Manage Food Menu & Pricing"])
        UC9(["Generate Dynamic Table QR Codes"])
        UC10(["Manage Inventory & Log Purchases"])
        UC11(["Map Recipes to Dishes (BOM)"])
        UC12(["Receive Low-Stock Alerts"])
        
        UC13(["View Financial & Sales Analytics"])
        UC14(["Run ML Demand Forecast Model"])
        UC15(["Inspect Spoilage & Wastage Reports"])
    end

    A1 --> UC1
    A1 --> UC2
    A1 --> UC3
    A1 --> UC4
    A1 --> UC5

    A2 --> UC1
    A2 --> UC6
    A2 --> UC7

    A3 --> UC1
    A3 --> UC8
    A3 --> UC9
    A3 --> UC10
    A3 --> UC11
    A3 --> UC12

    A4 --> UC1
    A4 --> UC13
    A4 --> UC14
    A4 --> UC15
```

---

## 4. Entity-Relationship (ER) Diagram

Represents the complete 12-table relational schema using Crow's Foot cardinality notation.

```mermaid
erDiagram
    USERS ||--o| STUDENTS : "has profile"
    USERS ||--o{ ORDERS : "places"
    USERS ||--o{ NOTIFICATIONS : "receives"
    
    CATEGORIES ||--|{ PRODUCTS : "contains"
    PRODUCTS ||--o{ ORDER_ITEMS : "included in"
    PRODUCTS ||--|{ RECIPES : "composed of"
    PRODUCTS ||--o{ DEMAND_FORECASTS : "has predictions"

    ORDERS ||--|{ ORDER_ITEMS : "consists of"
    ORDERS ||--|| PAYMENTS : "settled via"
    ORDERS ||--o{ STOCK_TRANSACTIONS : "triggers"

    INGREDIENTS ||--|{ RECIPES : "used in"
    INGREDIENTS ||--o{ STOCK_TRANSACTIONS : "tracked by"

    USERS {
        bigint id PK
        string username UK
        string email UK
        string password
        string role
        datetime created_at
    }

    STUDENTS {
        bigint id PK
        bigint user_id FK,UK
        string enrollment_no UK
        string course
        string phone_number
    }

    CATEGORIES {
        bigint id PK
        string name UK
        text description
        boolean is_active
    }

    PRODUCTS {
        bigint id PK
        bigint category_id FK
        string name
        decimal price
        int preparation_time
        boolean is_available
    }

    ORDERS {
        bigint id PK
        string order_token UK
        bigint user_id FK
        string table_number
        decimal total_amount
        string status
        datetime order_date
    }

    ORDER_ITEMS {
        bigint id PK
        bigint order_id FK
        bigint product_id FK
        int quantity
        decimal unit_price
    }

    PAYMENTS {
        bigint id PK
        bigint order_id FK,UK
        decimal amount
        string payment_mode
        string transaction_ref UK
        string payment_status
        datetime paid_at
    }

    INGREDIENTS {
        bigint id PK
        string name UK
        string unit
        decimal current_stock
        decimal minimum_threshold
        decimal unit_cost
    }

    RECIPES {
        bigint id PK
        bigint product_id FK
        bigint ingredient_id FK
        decimal quantity_required
    }

    STOCK_TRANSACTIONS {
        bigint id PK
        bigint ingredient_id FK
        decimal quantity
        string transaction_type
        bigint reference_order_id FK
        datetime logged_at
    }

    NOTIFICATIONS {
        bigint id PK
        bigint user_id FK
        string title
        text message
        boolean is_read
        datetime created_at
    }

    DEMAND_FORECASTS {
        bigint id PK
        bigint product_id FK
        date forecast_date
        int predicted_quantity
        int actual_quantity
        string model_name
        datetime generated_at
    }
```

---

## 5. Sequence Diagram: Contactless QR Order to Kitchen Fulfilment

```mermaid
sequenceDiagram
    autonumber
    actor Student as Student (Mobile)
    participant QR as QR / Web Controller
    participant OrderEngine as Order & Billing Engine
    participant DB as MySQL Relational DB
    actor Chef as Kitchen Staff (KDS)
    participant BOM as Inventory / BOM Engine
    actor Admin as Canteen Admin

    Student->>QR: Scan Table QR (e.g. /order/?table=T04)
    QR->>DB: Fetch Active Menu & Item Prices
    DB-->>QR: Product List + Availability Flags
    QR-->>Student: Render Responsive Mobile Menu

    Student->>OrderEngine: Submit Cart (2x Veg Burger, 1x Cold Coffee)
    OrderEngine->>DB: Begin Atomic DB Transaction
    OrderEngine->>DB: Validate Stock & Insert Order (Status: PENDING)
    OrderEngine->>DB: Insert Order_Items & Record Mock Payment
    OrderEngine->>DB: Commit Transaction
    OrderEngine-->>Student: Display Token #SC-104 & Status: "Pending"

    Chef->>DB: KDS auto-polls / receives new Ticket #SC-104
    Chef->>OrderEngine: Click "Confirm & Start Preparing"
    OrderEngine->>BOM: Trigger Recipe Stock Deduction
    
    rect rgb(240, 248, 255)
        note over BOM,DB: Atomic BOM Deduction
        BOM->>DB: Query Recipe Ingredients (Buns, Patties, Milk, Coffee)
        BOM->>DB: Deduct Required Stock from current_stock
        BOM->>DB: Write Audit Entries into Stock_Transactions
        BOM->>DB: Check (current_stock <= minimum_threshold)
    end

    opt Threshold Breached
        BOM->>DB: Create Low-Stock Notification
        DB-->>Admin: Alert: "Milk stock below safety threshold (4.5 L remaining)"
    end

    Chef->>OrderEngine: Mark Status: "READY"
    OrderEngine->>DB: Update orders.status = 'READY'
    OrderEngine-->>Student: Push Notification: "Order #SC-104 is READY for pickup!"
    
    Student->>Chef: Show Token #SC-104 at Counter & Collect Food
    Chef->>OrderEngine: Mark Status: "COMPLETED"
    OrderEngine->>DB: Update orders.status = 'COMPLETED'
```

---

## 6. Order Lifecycle State Machine Diagram

```mermaid
stateDiagram-v2
    [*] --> PENDING : Student submits order through QR cart
    PENDING --> CONFIRMED : Kitchen staff confirms order
    PENDING --> CANCELLED : Student/Admin cancels before acceptance

    CONFIRMED --> PREPARING : Chef starts food preparation
    PREPARING --> READY : Food ready at pickup counter
    READY --> COMPLETED : Student verifies token & receives food
    
    CANCELLED --> [*] : Transaction rolled back
    COMPLETED --> [*] : Transaction finalized for sales analytics
```

---

## 7. Machine Learning Demand Forecasting Pipeline

```mermaid
flowchart TD
    RawData[("Historical Transaction Records<br/>(Order Date, Item, Quantity, Price)")] --> Preprocessing["Data Cleaning & Aggregation<br/>(Daily Sales per Item)"]
    
    subgraph Feature_Engineering ["Feature Engineering Pipeline"]
        FE1["Lag Features: Sales(t-1), Sales(t-7)"]
        FE2["Rolling Metrics: 7-Day MA, 30-Day MA"]
        FE3["Temporal Flags: Day-of-Week, Month, Weekend"]
        FE4["Academic Flags: Exam Period, Campus Festival"]
    end

    Preprocessing --> Feature_Engineering
    Feature_Engineering --> Matrix["Feature Matrix (X) & Target Vector (y)"]

    Matrix --> Split["Train/Test Temporal Split (80% Train / 20% Test)"]

    subgraph Model_Evaluation ["Model Training & Benchmarking"]
        M0["Baseline: 7-Day Moving Average"]
        M1["Multiple Linear Regression (OLS)"]
        M2["Random Forest Regressor (Ensemble)"]
    end

    Split --> M0
    Split --> M1
    Split --> M2

    M0 --> Eval["Metric Computation: MAE, RMSE, MAPE"]
    M1 --> Eval
    M2 --> Eval

    Eval --> Champion["Select Optimal Model (Lowest RMSE/MAE)"]
    Champion --> Serialize["Serialize Model Artifact (.joblib)"]
    Serialize --> Inference["Daily Batch Inference Service"]
    Inference --> DB_Forecast[("Table: demand_forecasts")]
    DB_Forecast --> Dashboard["Management Analytics & Prep Recommendations"]
```

---

*System Design specifications verified and ready for IPU MCA 269 Minor Project evaluation.*

