# GURU GOBIND SINGH INDRAPRASTHA UNIVERSITY (GGSIPU)
## MASTER OF COMPUTER APPLICATIONS (MCA)
### MCA 269: MINOR PROJECT SYNOPSIS

---

# Project Title
**Smart Canteen Management System with QR-Based Ordering, Automated Inventory Control and Predictive Sales Analytics**

**Short Title:** Smart Canteen Management System (SCMS)  
**Track:** Advanced Web Application & Applied Machine Learning  
**Project Category:** Group Project (4 Members)  
**Target Completion Timeline:** 4-Week Accelerated Schedule  

---

## 1. Introduction and Abstract
In higher education institutions and large collegiate campuses, cafeteria services encounter intense peak-period traffic during recess and lunch breaks. Traditional college canteens rely predominantly on manual ordering, handwritten token exchanges, cash transactions, and manual ledger accounting. This paradigm suffers from pervasive friction: lengthy queues, billing inaccuracies, stockouts, unmonitored food spoilage, and a lack of actionable management data.

The **Smart Canteen Management System (SCMS)** is an end-to-end web-based software product engineered to replace conventional canteen operations with an intelligent digital ecosystem. SCMS integrates:
1. **Dynamic QR-Code Ordering:** Students scan table/counter QR codes to browse real-time digital menus, place contactless orders, and track preparation statuses.
2. **Kitchen Display System (KDS):** Kitchen personnel receive live digital ticket streams with status progression (`Pending` $\rightarrow$ `Confirmed` $\rightarrow$ `Preparing` $\rightarrow$ `Ready` $\rightarrow$ `Completed`).
3. **Automated Bill of Materials (BOM) Inventory Control:** Transactional deduction of raw ingredients upon order confirmation, coupled with automatic low-stock alerting.
4. **Predictive Sales & Demand Forecasting:** Machine learning regression models (Scikit-learn Linear Regression and Random Forest Regressor) applied to historical sales time-series data to forecast daily food requirements and suppress ingredient wastage.
5. **Business Intelligence (BI) Analytics:** Centralized management dashboards tracking revenue streams, peak congestion hours, fast-moving items, and inventory turnover.

Developed on Python 3.11, Django 5.x, MySQL 8.x, and Bootstrap 5, SCMS strictly adheres to modular monolithic architecture principles, fulfilling IPU MCA 269 curriculum requirements for innovative concepts, robust software engineering, and measurable operational outcomes.

---

## 2. Problem Statement
Manual canteen setups in university environments exhibit several operational failures:
- **Queue Congestion:** High turnaround time per student during peak 30–45 minute lunch breaks leads to unmanageable lines and missed orders.
- **Billing and Calculation Discrepancies:** Manual entry and paper-slip billing cause revenue leakage, incorrect item delivery, and delayed settlement.
- **Disconnected Stock Management:** Canteen administrators lack real-time visibility into raw material depletion, causing sudden dish unavailability or excessive ingredient perishability.
- **Absent Demand Planning:** Food preparation volumes are dictated by guesswork rather than empirical consumption patterns, causing 15–25% food wastage or premature shortages.
- **Lack of Decision Support:** Canteen management possesses no centralized reporting on daily gross revenues, category-level profitability, or student demand patterns.

---

## 3. Project Objectives
Aligned with the **IPU MCA 269 Evaluation Rubrics** (45% Requirements Analysis, 35% Design & Modeling, 10% Implementation & Viva, 10% Technical Documentation):

1. **Eliminate Ordering Delays:** Implement unique table/counter QR codes allowing instant smartphone-based menu browsing and order dispatch without app installation.
2. **Automate Order Routing & Status Tracking:** Provide a synchronized Kitchen Display System (KDS) reducing paper ticketing and displaying real-time preparation states to students.
3. **Atomic Inventory Reconciliation:** Establish recipe-to-ingredient mappings (BOM) such that order confirmations trigger atomic MySQL database deductions with automated safety-stock alerts.
4. **Deliver ML-Powered Demand Forecasting:** Train Scikit-learn models (Linear Regression, Random Forest Regressor) against historical sales variables (day of week, events, previous 7-day moving averages) to predict daily consumption with documented MAE and RMSE metrics.
5. **Role-Based Access Control (RBAC):** Enforce strict segregation of duty across four roles: **Student**, **Canteen Admin**, **Kitchen Staff**, and **Management / Business Analyst**.
6. **Data-Driven Management Reporting:** Provide interactive visual analytics (daily revenue, item popularity rankings, wastage reports) through responsive dashboards.

---

## 4. Existing System vs. Proposed System

| Parameter | Existing Manual / Semi-Manual System | Proposed Smart Canteen System (SCMS) |
| :--- | :--- | :--- |
| **Ordering Process** | Physical counter queues; handwritten tokens or basic desktop cash registers. | Decentralized QR scanning via mobile browser; asynchronous order submission. |
| **Kitchen Communication** | Paper slips shouted or pinned to counters; vulnerable to loss and ordering chaos. | Digital Kitchen Display System (KDS) updated live with status buttons. |
| **Inventory Tracking** | End-of-day manual counts or ledger approximations; frequent stock discrepancies. | Real-time atomic deduction based on exact ingredient recipe formulations. |
| **Stock Warnings** | Reactive: noticed only when an ingredient is physically exhausted mid-shift. | Proactive: automated notification triggers when stock drops below minimum thresholds. |
| **Demand Planning** | Intuitive estimation resulting in food waste or mid-day stockouts. | Supervised Machine Learning regression forecasting daily dish demand. |
| **Operational Visibility** | Disconnected registers; delayed or zero periodic analytics. | Integrated multi-role web dashboards featuring revenue, sales, and inventory graphs. |

---

## 5. Technology Stack & Architectural Choice

### 5.1 Architecture
- **Paradigm:** Modular Monolithic Architecture with Model-View-Template (MVT) separation and RESTful API endpoints where asynchronous updates are required.
- **Rationale:** Highly maintainable for university project evaluation, avoids distributed microservice latency and deployment overhead, guarantees ACID transactional integrity across billing and inventory updates.

### 5.2 Technical Specifications
- **Programming Language:** Python 3.11+
- **Web Backend Framework:** Django 5.x & Django REST Framework (DRF)
- **Database Engine:** MySQL 8.x (Relational DBMS with InnoDB engine for transactional integrity and Foreign Key constraints)
- **Frontend / UI:** HTML5, CSS3, Modern JavaScript (ES6+), Bootstrap 5.3, Bootstrap Icons
- **QR Code Generation:** Python `qrcode` & `Pillow` libraries
- **Machine Learning & Data Analytics:** Scikit-learn, Pandas, NumPy, Joblib
- **Data Visualization:** Chart.js (Interactive client-side charting) & Matplotlib
- **Development & Modeling Tools:** VS Code, MySQL Workbench, Git/GitHub

---

## 6. Functional Modules Breakdown

### Module 1: Authentication & RBAC (Role-Based Access Control)
- Custom Django User model with roles: `STUDENT`, `ADMIN`, `KITCHEN_STAFF`, `MANAGEMENT`.
- Session security, password hashing (PBKDF2 SHA-256), login/logout views, and view-level authorization decorators (`@role_required`).

### Module 2: Student Portal & Order History
- Student profile management with University Enrollment / Roll Number and department info.
- Filterable order history, digital invoice receipts, and live order status tracker.

### Module 3: Digital Menu & Dynamic QR Management
- Admin module to manage categories (Beverages, Meals, Snacks, Specials), food items, base prices, prep times, and live availability toggles (`is_available`).
- Automatic generation and download of cryptographic/table-indexed QR codes printable for canteen tables.

### Module 4: Contactless QR Ordering & Shopping Cart
- Responsive, mobile-first ordering UI rendered upon QR scan (e.g., `/canteen/table/T-04/`).
- Session-backed shopping cart, item quantity selectors, special dietary notes, and total price calculation.

### Module 5: Order Processing & Kitchen Display System (KDS)
- FIFO ordering queue for kitchen staff.
- One-click order state transitions: `PENDING` $\rightarrow$ `CONFIRMED` $\rightarrow$ `PREPARING` $\rightarrow$ `READY` $\rightarrow$ `COMPLETED` / `CANCELLED`.
- Audio-visual alert ping when new orders arrive.

### Module 6: Billing & Simulated Payment Gateway
- Generation of unique Order Token IDs and digital bills.
- Simulated multi-modal checkout (College Smart Wallet / UPI Mock / Cash at Counter) with atomic payment status tracking.

### Module 7: Bill of Materials (BOM) & Automated Inventory Control
- Ingredient master catalog (raw ingredients, measurement units: kg, g, L, ml, pieces).
- Recipe mapping (`ProductIngredient` link table detailing exact ingredient proportions per dish).
- Atomic stock decrement upon order confirmation:
  $$\text{Remaining Stock} = \text{Current Stock} - (\text{Recipe Quantity} \times \text{Units Ordered})$$
- Automated low-stock threshold monitoring and threshold trigger warnings.

### Module 8: Sales & Financial Analytics
- Dynamic revenue reports: daily, weekly, monthly cash flow and transaction counts.
- Best-selling dishes, category revenue distribution, and peak-hour ordering congestion charts via Chart.js.

### Module 9: ML Predictive Food Demand Forecasting
- Feature engineering over historical sales records (Day of Week, Rolling 7-Day Average, Academic Calendar Flag, Weather/Seasonality index).
- Scikit-learn regression models trained to predict next-day item preparation requirements.
- Rigorous model benchmarking: Baseline Moving Average vs. Multiple Linear Regression vs. Random Forest Regressor evaluated on MAE, RMSE, and MAPE.

### Module 10: In-App Notification System
- Real-time customer pickup alerts (`Your Order #1042 is READY for pickup!`).
- Kitchen alerts for rush orders and Administrative alerts for ingredients breaching safety thresholds.

---

## 7. Database Entity Structure (12 Core Relations)
1. **`Users`**: Primary user credentials, email, password hash, role flag.
2. **`Students`**: One-to-One link to Users, holding roll number, degree/course, contact.
3. **`Categories`**: Food classification taxonomy.
4. **`Products`**: Menu items with pricing, category FK, preparation time, availability flag.
5. **`Orders`**: Central transaction entity holding student FK, timestamp, total amount, order state.
6. **`Order_Items`**: Line items per order capturing product FK, quantity ordered, unit price snapshot.
7. **`Payments`**: Payment transaction record, mode (UPI/Cash/Wallet), transaction ref, status.
8. **`Ingredients`**: Raw material inventory catalog, unit of measure, minimum threshold, stock on hand.
9. **`Recipes`**: Bill of Materials (BOM) bridging Products and Ingredients with required quantities.
10. **`Stock_Transactions`**: Audit log of stock movements (INWARD purchase, OUTWARD order deduction, SPOILAGE adjustment).
11. **`Notifications`**: In-app notifications indexed by user ID and read status.
12. **`Demand_Forecasts`**: Historical and predicted item consumption figures generated by ML models.

---

## 8. Team Member Role Allocation (4 Members)

| Member | Designated Role | Core Technical Responsibilities & Deliverables |
| :--- | :--- | :--- |
| **Member 1** | **Backend Lead & System Architect** | Django project scaffolding, Custom User authentication, RBAC decorators, Order processing business logic, Atomic transaction pipelines, API endpoints. |
| **Member 2** | **Frontend & UI/UX Engineer** | Responsive Bootstrap 5 interfaces, Student mobile ordering screen, Kitchen Display System (KDS), Admin portal layout, Chart.js dashboard integration. |
| **Member 3** | **Database & Inventory Engineer** | MySQL relational schema design, InnoDB table constraints, Recipe BOM mapping, automated stock deduction routines, stock transaction audit log, seed test data. |
| **Member 4** | **ML & Data Analytics Engineer** | Synthetic and historical sales data pipeline, Feature engineering, Scikit-learn regression models, Model evaluation (MAE/RMSE), Power BI / Management reports, Synopsis & Documentation lead. |

*Shared Team Responsibilities:* Requirement engineering, system design diagrams (DFD, UML, ERD), integration testing, final IPU MCA 269 project report drafting, technical paper formulation, and viva demonstration rehearsal.

---

## 9. Accelerated 4-Week Development Roadmap

```
Week 1: Requirements Formalization, System Design & Architecture
├── Finalize SRS (IEEE 830) and formal Project Synopsis
├── Construct DFD Level 0, 1, 2, UML Use-Case, Sequence, and ER Diagrams
├── Initialize Git repository, Django 5 project, and MySQL 8 database schema
└── Implement Custom User Model and Role-Based Access Control (RBAC)

Week 2: Core Ordering, QR Engine & Kitchen Display System (KDS)
├── Develop Menu Management & dynamic QR generation engine
├── Build Student QR-scan mobile ordering interface and session cart
├── Implement atomic order placement transaction and billing logic
└── Build real-time Kitchen Display System (KDS) with order lifecycle states

Week 3: Inventory Automation (BOM) & Machine Learning Pipeline
├── Implement Bill of Materials (Recipes) and automatic stock deduction
├── Configure low-stock threshold triggers and in-app notifications
├── Generate historical canteen transaction dataset for ML training
└── Train and benchmark Scikit-learn demand forecasting models (LinReg & RandomForest)

Week 4: Analytics Dashboards, System Testing & Academic Deliverables
├── Integrate Chart.js analytics into Admin/Management Dashboard
├── Execute Unit, Integration, and User Acceptance Testing (UAT)
├── Complete final IPU MCA 269 project report (Chapters 1–11)
├── Draft technical research paper and presentation slides (PPT)
└── System end-to-end rehearsal for academic viva
```

---

## 10. Expected Academic & Practical Deliverables
1. **Fully Functional Web Platform:** Responsive web application running with Student, Admin, Kitchen, and Management dashboards.
2. **Standardized Documentation:** Complete SRS document, HLD/LLD reports, and Final Dissertation matching IPU format guidelines.
3. **Diagram Suite:** High-resolution DFDs (Levels 0, 1, 2), UML Use-Case, Sequence, Class, State, and Crow's Foot ER Diagrams.
4. **Trained ML Artifact:** Serialized Scikit-learn demand prediction models (`.joblib`) with documented comparative metrics against baseline moving averages.
5. **Technical Paper & Presentation:** 6–8 page academic manuscript in IEEE format detailing the architecture, algorithms, and empirical results, accompanied by an executive defense slide deck (PPT).

---

**Submitted By:**  
MCA Final Year Project Group (4 Members)  
Department of Computer Applications  
Guru Gobind Singh Indraprastha University, New Delhi  

