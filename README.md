# Smart Canteen Management System (SCMS)
### An Intelligent, QR-Based Food Ordering, Automated Inventory & Sales Analytics Platform
**IPU MCA 269 Minor Project (GGSIPU New Delhi)**

---

## 🎯 Project Overview
The **Smart Canteen Management System (SCMS)** is an enterprise-grade web application engineered to transform traditional college canteens into automated, digital dining facilities. Built with **Python, Django 5, MySQL 8, Bootstrap 5, and Scikit-learn**, it provides:

- 📱 **Contactless QR Ordering:** Instant digital menu access and checkout by scanning table or counter QR codes without any native mobile app download.
- 🍳 **Kitchen Display System (KDS):** Paperless digital ticketing for kitchen staff with live status transitions (`Pending` $\rightarrow$ `Confirmed` $\rightarrow$ `Preparing` $\rightarrow$ `Ready` $\rightarrow$ `Completed`).
- 📦 **Automated Bill of Materials (BOM) Inventory:** Real-time atomic deduction of raw ingredient stock based on exact recipes with automated low-stock warnings.
- 🤖 **ML Predictive Demand Forecasting:** Scikit-learn regression models forecasting daily food demand to eliminate shortages and cut down campus food wastage.
- 📊 **Executive BI Analytics:** Comprehensive management dashboard tracking daily revenues, top dishes, peak lunch hours, and ingredient variance.

---

## 📂 Repository Structure
```
smart-canteen-management-system/
├── docs/
│   ├── PROJECT_SYNOPSIS.md                  # Formal IPU MCA 269 Synopsis
│   ├── SRS_DOCUMENT.md                      # IEEE 830 Software Requirements Spec
│   ├── SYSTEM_DESIGN_AND_DIAGRAMS.md        # HLD, LLD, DFDs, ERD & UML Diagrams
│   └── TEAM_RESPONSIBILITIES_AND_SPRINT_PLAN.md # 4-Member Matrix & 4-Week Schedule
├── requirements.txt                         # Python environment dependencies
└── README.md                                # Project guide and execution manual
```

---

## 👥 Team Configuration (4 Members)
1. **Member 1 (Backend Lead & Architect):** Django 5 core, Custom User model, RBAC, atomic order engine, and RESTful APIs.
2. **Member 2 (Frontend & UI/UX Engineer):** Responsive Bootstrap 5 UI, Mobile QR cart, Kitchen Display System (KDS), and Chart.js dashboards.
3. **Member 3 (Database & Inventory Engineer):** MySQL 8 relational schema, BOM recipe mapping, atomic stock deduction, and audit logs.
4. **Member 4 (ML & Data Analytics Engineer):** Sales dataset pipeline, feature engineering, Scikit-learn regression models, MAE/RMSE evaluation, and academic documentation.

---

## ⚙️ Quick Start & Setup Guide

### 1. Prerequisites
- Python 3.11 or higher
- MySQL Server 8.0+
- Git

### 2. Environment Setup
```bash
# Clone or navigate into the workspace
cd "C:\Users\Asus\.gemini\antigravity\scratch\smart-canteen-management-system"

# Create a virtual environment
python -m venv venv

# Activate the virtual environment
# Windows (PowerShell):
.\venv\Scripts\Activate.ps1
# Windows (CMD):
.\venv\Scripts\activate.bat

# Install dependencies
pip install -r requirements.txt
```

### 3. Database Configuration
Create a database named `smart_canteen_db` in MySQL:
```sql
CREATE DATABASE smart_canteen_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

---

## 📖 Evaluation Weightage Compliance (IPU MCA 269)
- **Requirements Analysis (45%):** Fully documented in [`docs/SRS_DOCUMENT.md`](docs/SRS_DOCUMENT.md).
- **System Designing (35%):** Fully modeled in [`docs/SYSTEM_DESIGN_AND_DIAGRAMS.md`](docs/SYSTEM_DESIGN_AND_DIAGRAMS.md).
- **Implementation & Viva (10%):** Step-by-step modular code execution roadmap in [`docs/TEAM_RESPONSIBILITIES_AND_SPRINT_PLAN.md`](docs/TEAM_RESPONSIBILITIES_AND_SPRINT_PLAN.md).
- **Technical Paper & Documentation (10%):** Outlines and presentation milestones documented in [`docs/PROJECT_SYNOPSIS.md`](docs/PROJECT_SYNOPSIS.md).

