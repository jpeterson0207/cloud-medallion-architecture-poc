"""Generate AdventureWorksLT sample CSV files for the Medallion Architecture POC.

Run: python generate_adventureworks.py
Output: output/ directory with 7 CSV files
"""
import csv
import os
import random
from datetime import datetime, timedelta

random.seed(42)
OUT_DIR = os.path.join(os.path.dirname(__file__), "output")
os.makedirs(OUT_DIR, exist_ok=True)

def write_csv(filename, headers, rows):
    path = os.path.join(OUT_DIR, filename)
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(headers)
        w.writerows(rows)
    print(f"  {filename}: {len(rows)} rows")

# ---------- SalesLTAddress ----------
cities = [
    ("Bothell","Washington","United States"),("Seattle","Washington","United States"),
    ("Redmond","Washington","United States"),("San Francisco","California","United States"),
    ("Los Angeles","California","United States"),("New York","New York","United States"),
    ("Chicago","Illinois","United States"),("Dallas","Texas","United States"),
    ("London","England","United Kingdom"),("Toronto","Ontario","Canada"),
    ("Sydney","New South Wales","Australia"),("Berlin","Brandenburg","Germany"),
    ("Paris","Ile-de-France","France"),("Tokyo","Kanto","Japan"),("Mumbai","Maharashtra","India"),
]
rows = []
for i in range(1, 451):
    c, s, co = random.choice(cities)
    rows.append([i, f"{random.randint(100,9999)} {random.choice(['Main','Oak','Pine','Elm'])} {random.choice(['St','Ave','Blvd'])}",
        "" if random.random()<0.6 else f"Suite {random.randint(1,500)}", c, s, co,
        f"{random.randint(10000,99999)}", "00000000-0000-0000-0000-000000000000", datetime.now().isoformat()])
write_csv("salesltaddress.csv", ["AddressID","AddressLine1","AddressLine2","City","StateProvince","CountryRegion","PostalCode","rowguid","ModifiedDate"], rows)

# ---------- SalesLTCustomer ----------
fnames = ["John","Jane","Bob","Alice","Charlie","Diana","Edward","Fiona","George","Helen","Ivan","Julia","Kevin","Laura","Michael","Nancy","Oscar","Patricia","Quinn","Rachel"]
lnames = ["Smith","Johnson","Williams","Brown","Jones","Garcia","Miller","Davis","Rodriguez","Martinez","Hernandez","Lopez","Wilson","Anderson","Thomas","Taylor"]
rows = []
for i in range(1, 851):
    fn, ln = random.choice(fnames), random.choice(lnames)
    rows.append([i, False, random.choice(["Mr.","Ms.","Mrs.","Dr.",""]), fn, random.choice(fnames)[0] if random.random()>0.5 else "", ln,
        "" if random.random()<0.9 else random.choice(["Jr.","Sr."]),
        f"{fn.lower()}{i}@{random.choice(['adventure-works','contoso','fabrikam'])}.com",
        "", f"AW{str(i).zfill(8)}",
        f"({random.choice(['206','425','312','212'])}) {random.randint(100,999)}-{random.randint(1000,9999)}",
        f"{fn} {ln}", "", "00000000-0000-0000-0000-000000000000", datetime.now().isoformat()])
write_csv("salesltcustomer.csv", ["CustomerID","NameStyle","Title","FirstName","MiddleName","LastName","Suffix","CompanyName","SalesPerson","AccountNumber","EmailAddress","Phone","rowguid","ModifiedDate"], rows)

# ---------- SalesLTCustomerAddress ----------
rows = [[cid, random.randint(1,450), random.choice(["Main Office","Shipping","Home"])] for cid in range(1,851)]
write_csv("salesltcustomeraddress.csv", ["CustomerID","AddressID","AddressType"], rows)

# ---------- SalesLTProductCategory ----------
cats = [(1,None,"Bikes"),(2,None,"Components"),(3,None,"Clothing"),(4,None,"Accessories"),
    (5,1,"Mountain Bikes"),(6,1,"Road Bikes"),(7,1,"Touring Bikes"),
    (8,2,"Handlebars"),(9,2,"Bottom Brackets"),(10,2,"Brakes"),(11,2,"Chains"),
    (12,2,"Cranksets"),(13,2,"Derailleurs"),(14,2,"Forks"),(15,2,"Headsets"),
    (16,2,"Mountain Frames"),(17,2,"Pedals"),(18,2,"Road Frames"),(19,2,"Saddles"),
    (20,2,"Touring Frames"),(21,2,"Wheels"),
    (22,3,"Bib-Shorts"),(23,3,"Caps"),(24,3,"Gloves"),(25,3,"Jerseys"),
    (26,3,"Shorts"),(27,3,"Socks"),(28,3,"Tights"),(29,3,"Vests"),
    (30,4,"Bike Racks"),(31,4,"Bike Stands"),(32,4,"Bottles and Cages"),
    (33,4,"Cleaners"),(34,4,"Fenders"),(35,4,"Helmets"),
    (36,4,"Hydration Packs"),(37,4,"Lights"),(38,4,"Locks"),
    (39,4,"Panniers"),(40,4,"Pumps"),(41,4,"Tires and Tubes")]
rows = [[c[0], c[1] or "", c[2], "00000000-0000-0000-0000-000000000000", datetime.now().isoformat()] for c in cats]
write_csv("salesltproductcategory.csv", ["ProductCategoryID","ParentProductCategoryID","Name","rowguid","ModifiedDate"], rows)

# ---------- SalesLTProduct ----------
names = ["Mountain-100","Mountain-200","Road-150","Road-250","Road-350","Touring-1000","Touring-2000",
    "HL Mountain Frame","ML Mountain Frame","LL Mountain Frame","HL Road Frame","ML Road Frame",
    "Sport-100 Helmet","Classic Vest","Short-Sleeve Jersey","Long-Sleeve Jersey","AWC Logo Cap",
    "Mountain Bike Socks","Racing Socks","Half-Finger Gloves","Full-Finger Gloves",
    "Hitch Rack","All-Purpose Bike Stand","Water Bottle","Mountain Bottle Cage","Road Bottle Cage",
    "Patch Kit","Touring Tire Tube","Mountain Tire","Touring Tire","HL Mountain Pedal","ML Road Pedal",
    "Chain","HL Crankset","ML Crankset","HL Bottom Bracket","Front Brakes","Rear Brakes",
    "Headlights","Taillight","Minipump","Fender Set","Mountain-300","Mountain-400","Mountain-500",
    "Road-450","Road-550","Road-650","Road-750","Touring-3000","LL Road Frame","LL Touring Frame",
    "ML Touring Frame","HL Touring Frame"]
rows = []
for i in range(1, len(names)+1):
    cost = round(random.uniform(5,3000),4)
    rows.append([i, names[i-1], f"{names[i-1][:2].upper()}-{random.randint(1000,9999)}",
        random.choice(["Red","Blue","Black","Silver","Yellow","White",""]),
        cost, round(cost*random.uniform(1.2,2.5),4),
        random.choice(["S","M","L","XL","42","48","52",""]),
        round(random.uniform(0.5,25),2) if random.random()>0.3 else "",
        random.choice([c[0] for c in cats if c[1]]), "",
        datetime.now().isoformat(), datetime.now().isoformat(),
        "00000000-0000-0000-0000-000000000000", datetime.now().isoformat()])
write_csv("salesltproduct.csv", ["ProductID","Name","ProductNumber","Color","StandardCost","ListPrice","Size","Weight","ProductCategoryID","ProductModelID","SellStartDate","SellEndDate","rowguid","ModifiedDate"], rows)

# ---------- SalesLTSalesOrderHeader ----------
base_date = datetime(2024, 6, 1)
rows = []
for i in range(1, 1001):
    od = base_date + timedelta(days=random.randint(0,365))
    sub = round(random.uniform(50,15000),4)
    tax = round(sub*0.08,4); freight = round(sub*0.02,4)
    rows.append([71774+i, random.randint(1,8), od.strftime("%Y-%m-%d"),
        (od+timedelta(days=random.randint(7,30))).strftime("%Y-%m-%d"),
        (od+timedelta(days=random.randint(3,14))).strftime("%Y-%m-%d"),
        5, random.choice([True,False]), f"SO{71774+i}", f"PO{random.randint(10000,99999)}",
        f"10-4020-{str(random.randint(1,850)).zfill(6)}", random.randint(1,850),
        random.randint(1,450), random.randint(1,450),
        random.choice(["CARGO TRANSPORT 5","OVERNIGHT J-FAST","XRQ - TRUCK GROUND-"]),
        "", sub, tax, freight, round(sub+tax+freight,4), "",
        "00000000-0000-0000-0000-000000000000", datetime.now().isoformat()])
write_csv("salesltsalesorderheader.csv", ["SalesOrderID","RevisionNumber","OrderDate","DueDate","ShipDate","Status","OnlineOrderFlag","SalesOrderNumber","PurchaseOrderNumber","AccountNumber","CustomerID","ShipToAddressID","BillToAddressID","ShipMethod","CreditCardApprovalCode","SubTotal","TaxAmt","Freight","TotalDue","Comment","rowguid","ModifiedDate"], rows)

# ---------- SalesLTSalesOrderDetail ----------
rows = []; did = 1
for i in range(1, 1001):
    for _ in range(random.randint(1,5)):
        up = round(random.uniform(10,3500),4)
        disc = round(random.choice([0,0,0,0.05,0.10,0.15,0.20]),2)
        qty = random.randint(1,10)
        rows.append([71774+i, did, qty, random.randint(1,len(names)), up, disc, round(qty*up*(1-disc),4),
            "00000000-0000-0000-0000-000000000000", datetime.now().isoformat()])
        did += 1
write_csv("salesltsalesorderdetail.csv", ["SalesOrderID","SalesOrderDetailID","OrderQty","ProductID","UnitPrice","UnitPriceDiscount","LineTotal","rowguid","ModifiedDate"], rows)

print(f"\nAll files generated in: {OUT_DIR}")
