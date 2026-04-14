# 🏗️ Cloud Medallion Architecture POC
### AdventureWorksLT | Bronze → Silver → Gold | Microsoft Fabric

---

## 📋 Overview

This repository contains a complete **Medallion Architecture** solution built on Microsoft Fabric using the **AdventureWorksLT** dataset. It implements a Bronze → Silver → Gold data pipeline using PySpark notebooks across 3 Fabric Lakehouses.

Based on **Lab 2: Implement the Medallion Architecture** with all placeholders pre-filled and ready to run.

### Architecture

```
AdventureWorksLT CSV Files (7 SalesLT tables)
    │  Uploaded to Bronze Lakehouse Files/vbdsqldb/
    │
    ▼
┌─────────────────────────────────────────────┐
│  🥉 BRONZE Lakehouse                        │
│  Files/vbdsqldb/                             │
│    salesltaddress.csv          (450 rows)    │
│    salesltcustomer.csv         (850 rows)    │
│    salesltcustomeraddress.csv  (850 rows)    │
│    salesltproduct.csv          (54 rows)     │
│    salesltproductcategory.csv  (41 rows)     │
│    salesltsalesorderheader.csv (1,000 rows)  │
│    salesltsalesorderdetail.csv (2,976 rows)  │
└──────────────────┬──────────────────────────┘
                   │
                   ▼  Notebook: "Bronze to Silver"
┌─────────────────────────────────────────────┐
│  🥈 SILVER Lakehouse                        │
│  Tables/ (Delta format)                      │
│    salesOrderHeader  (dates randomized)      │
│    salesOrderDetail                          │
│    salesCustomer                             │
│    salesCustomerAddress                      │
│    salesProduct                              │
│    salesProductCategory                      │
└──────────────────┬──────────────────────────┘
                   │
                   ▼  Notebook: "Silver to Gold"
┌─────────────────────────────────────────────┐
│  🥇 GOLD Lakehouse                          │
│  Tables/ (Delta format — Star Schema)        │
│    dimCustomer   (surrogate key + address)   │
│    dimProduct    (surrogate key + category)   │
│    dimDate       (generated 2000–2024)       │
│    factSales     (joined with dim keys)      │
└─────────────────────────────────────────────┘
```

---

## 🚀 Quick Start

### Prerequisites
- Microsoft Fabric workspace with capacity (trial or paid)
- Python 3.8+ (for generating sample data)

### Step 1: Create Lakehouses
In your Fabric workspace, create 3 lakehouses:
1. `bronze`
2. `silver`
3. `gold`

### Step 2: Generate and Upload Sample Data

```bash
cd data
python generate_adventureworks.py
```

This generates 7 CSV files in `data/output/`. Upload all of them to:
**Bronze Lakehouse → Files → vbdsqldb/**

### Step 3: Update Notebook Paths

Open `notebooks/Bronze_to_Silver.ipynb` and update:
- **Cell 2:** Replace `adventureWorksPath` with the ABFSS path to your Bronze lakehouse's `Files/vbdsqldb` folder
- **Cell 15:** Replace `basePathSilverLakeHouse` with the ABFSS path to your Silver lakehouse's `Tables` folder

Open `notebooks/Silver_to_Gold.ipynb` and update:
- **Cell 8:** Replace `basePathGoldLakeHouse` with the ABFSS path to your Gold lakehouse's `Tables` folder

> 💡 **How to find ABFSS paths:** Open a lakehouse → right-click the Files or Tables folder → Properties → copy the ABFS path

### Step 4: Import and Run Notebooks
1. In your workspace, **Import → Notebook → From this computer**
2. Upload `Bronze_to_Silver.ipynb` and `Silver_to_Gold.ipynb`
3. Attach the **bronze** and **silver** lakehouses to the Bronze to Silver notebook
4. Attach the **silver** and **gold** lakehouses to the Silver to Gold notebook
5. Run **Bronze to Silver** first → then **Silver to Gold**

### Step 5: Verify
- **Silver Lakehouse → Tables:** 6 delta tables
- **Gold Lakehouse → Tables:** 4 delta tables (dimCustomer, dimProduct, dimDate, factSales)

---

## 📁 Repository Structure

```
cloud-medallion-architecture-poc/
├── README.md
├── notebooks/
│   ├── Bronze_to_Silver.ipynb           # Completed notebook (paths pre-filled)
│   ├── Silver_to_Gold.ipynb             # Completed notebook (paths pre-filled)
│   ├── Bronze_to_Silver_TEMPLATE.ipynb  # Original template with <ENTER HERE> placeholders
│   └── Silver_to_Gold_TEMPLATE.ipynb    # Original template with <ENTER HERE> placeholders
├── data/
│   └── generate_adventureworks.py       # Generates all 7 AdventureWorksLT CSV files
├── .gitignore
└── LICENSE
```

---

## 📓 Notebook Details

### Bronze to Silver (20 cells)

| Step | What Happens |
|------|-------------|
| 1 | Enable V-Order + Optimize Write |
| 2 | Read all CSVs from `Files/vbdsqldb/` → create temp SQL views |
| 3–5 | Explore views (`SHOW VIEWS`, sample queries) |
| 6–13 | Select/rename columns for each table → create clean DataFrames |
| 9 | **Randomize OrderDate** — replaces static dates with random dates within past year |
| 14–20 | Write each DataFrame as a delta table to Silver Lakehouse |

**Tables created:** salesOrderHeader, salesOrderDetail, salesCustomer, salesCustomerAddress, salesProduct, salesProductCategory

### Silver to Gold (12 cells)

| Step | What Happens |
|------|-------------|
| 1 | Enable V-Order + Optimize Write |
| 2–3 | **dimCustomer** — Join `salesCustomer` + `salesCustomerAddress`, add surrogate key |
| 4–5 | **dimProduct** — Join `salesProduct` + `salesProductCategory`, add surrogate key |
| 6 | **dimDate** — Generate date dimension (Jan 2000 – Dec 2024) with Year, Month, Quarter, etc. |
| 7–9 | Write dimCustomer, dimProduct, dimDate to Gold |
| 10 | **factSales** — Join `salesOrderHeader` + `salesOrderDetail` + dimension keys via LEFT JOIN |
| 11–12 | Write dimDate and factSales to Gold |

**Tables created:** dimCustomer, dimProduct, dimDate, factSales

---

## 📊 Data Model (Star Schema)

```
                ┌──────────────┐
                │  dimCustomer  │
                │  ──────────── │
                │  CustomerIDKey│ (surrogate)
                │  CustomerID   │
                │  FirstName    │
                │  LastName     │
                │  CompanyName  │
                │  AddressID    │
                └──────┬───────┘
                       │
┌──────────────┐  ┌────┴──────────────┐  ┌──────────────┐
│   dimDate     │  │    factSales       │  │  dimProduct   │
│  ──────────── │  │  ─────────────────│  │  ──────────── │
│  Date         │◄─┤  OrderDate         │  │  ProductIDKey │ (surrogate)
│  Year         │  │  CustomerIDKey ────┼──┤  ProductID    │
│  Month        │  │  ProductIDKey  ────┼──┘  Name         │
│  Quarter      │  │  OrderQty          │     Color        │
│  DayOfWeek    │  │  UnitPrice         │     ListPrice    │
│  WeekOfYear   │  │  LineTotal         │     CategoryName │
└──────────────┘  └────────────────────┘  └──────────────┘
```

---

## 🔗 References

- [Lab 2: Implement the Medallion Architecture](https://learn.microsoft.com/en-us/fabric/data-engineering/) — Original lab source
- [Medallion Architecture](https://learn.microsoft.com/en-us/azure/databricks/lakehouse/medallion) — Architecture pattern
- [AdventureWorksLT](https://learn.microsoft.com/en-us/sql/samples/adventureworks-install-configure) — Source dataset

---

> 📝 **Workspace:** Cloud- Medallion Architecture POC | **Dataset:** AdventureWorksLT | **Last updated:** April 2026
