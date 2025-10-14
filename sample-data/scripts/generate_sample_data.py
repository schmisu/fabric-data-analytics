#!/usr/bin/env python3
"""
Generate realistic SAP Accounts Payable sample data with variety
- Two years (2023-2024) for YoY analysis
- More vendors, documents, and line items
- Varied payment terms, amounts, and patterns
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

# Set seed for reproducibility
np.random.seed(42)
random.seed(42)

# ============================================================================
# CONFIGURATION
# ============================================================================

NUM_VENDORS = 100  # Increased from 50
NUM_DOCUMENTS_PER_YEAR = 500  # Increased from 142
START_DATE = datetime(2023, 1, 1)
END_DATE = datetime(2024, 12, 31)

# ============================================================================
# VENDOR MASTER DATA (LFA1)
# ============================================================================

# Diverse German companies across industries
VENDOR_NAMES = [
    # Manufacturing (20)
    "Siemens AG", "BASF SE", "Volkswagen AG", "Bosch GmbH", "Bayer AG",
    "Daimler AG", "BMW AG", "ThyssenKrupp AG", "Continental AG", "Schaeffler AG",
    "ZF Friedrichshafen", "Linde AG", "Henkel AG", "Merck KGaA", "Fresenius SE",
    "Heidelberg Cement", "Evonik Industries", "Covestro AG", "KION Group", "Knorr-Bremse",

    # Utilities & Energy (10)
    "E.ON SE", "RWE AG", "EnBW AG", "Innogy SE", "Vattenfall GmbH",
    "50Hertz Transmission", "TenneT TSO", "Stadtwerke München", "EWE AG", "MVV Energie",

    # Logistics & Transport (10)
    "Deutsche Post DHL", "DB Schenker", "Kühne + Nagel", "Dachser SE", "Hellmann Worldwide",
    "Rhenus Logistics", "BLG Logistics", "Fiege Logistik", "Meyer & Meyer", "Mosolf SE",

    # Technology & IT (10)
    "SAP SE", "Software AG", "Deutsche Telekom", "Telefónica Germany", "1&1 AG",
    "TeamViewer AG", "Adesso SE", "Cancom SE", "Bechtle AG", "Dataport",

    # Financial Services (10)
    "Deutsche Bank", "Commerzbank AG", "Allianz SE", "Munich Re", "DZ Bank AG",
    "KfW Bankengruppe", "Talanx AG", "Hannover Rück", "ERGO Group", "R+V Versicherung",

    # Retail & Consumer (10)
    "ALDI Süd", "LIDL Stiftung", "REWE Group", "EDEKA Zentrale", "Metro AG",
    "Kaufland", "dm-drogerie markt", "Rossmann", "OTTO Group", "Zalando SE",

    # Chemicals & Materials (10)
    "Wacker Chemie", "Lanxess AG", "Symrise AG", "Fuchs Petrolub", "K+S AG",
    "Brenntag SE", "Altana AG", "Clariant", "Evonik Degussa", "BASF Coatings",

    # Construction & Real Estate (10)
    "Hochtief AG", "Bilfinger SE", "Strabag SE", "Max Bögl", "Ed. Züblin AG",
    "BAM Deutschland", "Porr AG", "Goldbeck GmbH", "Wolff & Müller", "HABAU Group",

    # Pharma & Healthcare (10)
    "Fresenius Medical Care", "B. Braun Melsungen", "Stada Arzneimittel", "Grünenthal GmbH", "Dr. Reddy's",
    "Sanofi-Aventis", "Boehringer Ingelheim", "Roche Deutschland", "Novartis Pharma", "Pfizer Deutschland",

    # Others (10)
    "TÜV Rheinland", "TÜV SÜD", "Dekra SE", "Bertelsmann SE", "Axel Springer",
    "ProSiebenSat.1", "Freenet AG", "Uniper SE", "Vonovia SE", "Deutsche Wohnen"
]

# German cities
CITIES = [
    "München", "Berlin", "Hamburg", "Frankfurt", "Köln", "Stuttgart", "Düsseldorf",
    "Leipzig", "Dortmund", "Essen", "Bremen", "Dresden", "Hannover", "Nürnberg",
    "Duisburg", "Bochum", "Wuppertal", "Bielefeld", "Bonn", "Münster", "Karlsruhe",
    "Mannheim", "Augsburg", "Wiesbaden", "Gelsenkirchen", "Mönchengladbach",
    "Braunschweig", "Chemnitz", "Kiel", "Aachen", "Halle", "Magdeburg", "Freiburg",
    "Krefeld", "Lübeck", "Oberhausen", "Erfurt", "Mainz", "Rostock", "Kassel"
]

# Vendor account groups (varied)
VENDOR_GROUPS = ["KRED", "LIEF", "SONST", "INTER", "EINM"]

# Payment terms with variety
PAYMENT_TERMS_OPTIONS = [
    ("0001", 30, 2.0, 14),   # 30 days net, 2% discount within 14 days
    ("0002", 60, 3.0, 10),   # 60 days net, 3% discount within 10 days
    ("0003", 14, 0.0, 0),    # 14 days net, no discount
    ("0004", 45, 2.5, 21),   # 45 days net, 2.5% discount within 21 days
    ("0005", 90, 1.5, 30),   # 90 days net, 1.5% discount within 30 days
    ("0006", 30, 0.0, 0),    # 30 days net, no discount
    ("0007", 7, 0.0, 0),     # 7 days (immediate payment)
]

def generate_vendors(num_vendors=100):
    """Generate vendor master data with variety"""
    vendors = []

    for i in range(num_vendors):
        vendor_number = f"{(i+1):010d}"  # 0000000001, 0000000002, etc.

        # Use actual company names, then generate generic ones
        if i < len(VENDOR_NAMES):
            name = VENDOR_NAMES[i]
        else:
            name = f"Firma {chr(65 + (i % 26))} GmbH & Co. KG {i}"

        # Varied payment terms
        payment_terms = random.choice(PAYMENT_TERMS_OPTIONS)

        vendors.append({
            "MANDT": "100",
            "LIFNR": vendor_number,
            "NAME1": name,
            "ORT01": random.choice(CITIES),
            "LAND1": "DE",
            "STCD1": f"DE{random.randint(100000000, 999999999)}",
            "KTOKK": random.choice(VENDOR_GROUPS),
            "ZTERM": payment_terms[0]
        })

    return pd.DataFrame(vendors)

# ============================================================================
# DOCUMENT HEADERS (BKPF)
# ============================================================================

DOCUMENT_TYPES = [
    ("RE", 0.60),  # Invoice (60%)
    ("KZ", 0.35),  # Payment (35%)
    ("KG", 0.05),  # Credit Memo (5%)
]

COMPANY_CODES = ["1000", "2000", "3000"]  # Multiple companies

def generate_documents(num_docs_per_year=500):
    """Generate document headers with seasonal patterns"""
    documents = []
    doc_counter = 1

    for year in [2023, 2024]:
        for i in range(num_docs_per_year):
            # Seasonal pattern: more invoices in Q4, fewer in summer
            month_weights = [8, 8, 9, 9, 7, 6, 6, 7, 9, 10, 11, 12]  # Q4 has more
            month = random.choices(range(1, 13), weights=month_weights)[0]
            day = random.randint(1, 28)  # Avoid month-end issues

            doc_date = datetime(year, month, day)
            posting_date = doc_date + timedelta(days=random.randint(0, 3))

            # Document type with realistic distribution
            doc_type = random.choices(
                [dt[0] for dt in DOCUMENT_TYPES],
                weights=[dt[1] for dt in DOCUMENT_TYPES]
            )[0]

            doc_number = f"{doc_counter:010d}"

            documents.append({
                "MANDT": "100",
                "BUKRS": random.choice(COMPANY_CODES),
                "BELNR": doc_number,
                "GJAHR": str(year),
                "BLART": doc_type,
                "BLDAT": doc_date.strftime("%Y%m%d"),
                "BUDAT": posting_date.strftime("%Y%m%d"),
                "WAERS": "EUR",
                "BKTXT": f"{'Invoice' if doc_type == 'RE' else 'Payment' if doc_type == 'KZ' else 'Credit Memo'} {doc_number}"
            })

            doc_counter += 1

    return pd.DataFrame(documents)

# ============================================================================
# LINE ITEMS (BSEG)
# ============================================================================

GL_ACCOUNTS = {
    "400000": 0.15,  # Raw materials (15%)
    "410000": 0.12,  # Consumables (12%)
    "420000": 0.10,  # Services (10%)
    "430000": 0.08,  # Maintenance (8%)
    "440000": 0.08,  # IT/Software (8%)
    "450000": 0.07,  # Marketing (7%)
    "460000": 0.06,  # Travel (6%)
    "470000": 0.05,  # Utilities (5%)
    "480000": 0.05,  # Rent (5%)
    "490000": 0.04,  # Insurance (4%)
    "500000": 0.04,  # Consulting (4%)
    "510000": 0.03,  # Legal fees (3%)
    "520000": 0.03,  # Training (3%)
    "160000": 0.10,  # Vendor clearing account (10%)
}

def generate_line_items(documents_df, vendors_df):
    """Generate line items with varied amounts and patterns"""
    line_items = []
    line_counter = 1

    for _, doc in documents_df.iterrows():
        doc_type = doc["BLART"]
        num_lines = random.randint(1, 5) if doc_type == "RE" else random.randint(1, 3)

        # Invoice amount varies by GL account type
        if doc_type == "RE":
            # Generate GL lines first
            gl_total = 0
            gl_lines = []

            for line_num in range(num_lines):
                gl_account = random.choices(
                    list(GL_ACCOUNTS.keys()),
                    weights=list(GL_ACCOUNTS.values())
                )[0]

                # Amount varies by account type
                if gl_account in ["400000", "410000"]:  # Materials
                    amount = round(random.uniform(500, 50000), 2)
                elif gl_account in ["420000", "430000", "440000"]:  # Services/IT
                    amount = round(random.uniform(200, 20000), 2)
                elif gl_account in ["480000", "490000"]:  # Rent/Insurance
                    amount = round(random.uniform(1000, 100000), 2)
                else:
                    amount = round(random.uniform(100, 10000), 2)

                gl_total += amount
                gl_lines.append((gl_account, amount))

            # Add GL account lines (Debit)
            for line_num, (gl_account, amount) in enumerate(gl_lines, start=1):
                line_items.append({
                    "MANDT": doc["MANDT"],
                    "BUKRS": doc["BUKRS"],
                    "BELNR": doc["BELNR"],
                    "GJAHR": doc["GJAHR"],
                    "BUZEI": f"{line_num:03d}",
                    "KOART": "S",  # GL account
                    "HKONT": gl_account,
                    "LIFNR": "",
                    "DMBTR": amount,
                    "SHKZG": "S",  # Debit
                    "SGTXT": f"Expense {gl_account}",
                    "ZFBDT": doc["BLDAT"],
                    "ZBD1T": "",
                    "ZBD1P": ""
                })

            # Add vendor line (Credit, balancing entry)
            vendor = vendors_df.sample(1).iloc[0]
            payment_term = next(pt for pt in PAYMENT_TERMS_OPTIONS if pt[0] == vendor["ZTERM"])

            line_items.append({
                "MANDT": doc["MANDT"],
                "BUKRS": doc["BUKRS"],
                "BELNR": doc["BELNR"],
                "GJAHR": doc["GJAHR"],
                "BUZEI": f"{len(gl_lines) + 1:03d}",
                "KOART": "K",  # Vendor
                "HKONT": "160000",  # Vendor clearing
                "LIFNR": vendor["LIFNR"],
                "DMBTR": gl_total,
                "SHKZG": "H",  # Credit
                "SGTXT": f"AP {vendor['NAME1']}",
                "ZFBDT": doc["BLDAT"],
                "ZBD1T": str(payment_term[3]) if payment_term[3] > 0 else "",
                "ZBD1P": str(payment_term[2]) if payment_term[2] > 0 else ""
            })

        elif doc_type == "KZ":  # Payment
            # Bank line (Credit)
            amount = round(random.uniform(1000, 100000), 2)

            line_items.append({
                "MANDT": doc["MANDT"],
                "BUKRS": doc["BUKRS"],
                "BELNR": doc["BELNR"],
                "GJAHR": doc["GJAHR"],
                "BUZEI": "001",
                "KOART": "S",
                "HKONT": "113100",  # Bank account
                "LIFNR": "",
                "DMBTR": amount,
                "SHKZG": "H",  # Credit
                "SGTXT": "Payment",
                "ZFBDT": doc["BLDAT"],
                "ZBD1T": "",
                "ZBD1P": ""
            })

            # Vendor clearing (Debit)
            vendor = vendors_df.sample(1).iloc[0]

            line_items.append({
                "MANDT": doc["MANDT"],
                "BUKRS": doc["BUKRS"],
                "BELNR": doc["BELNR"],
                "GJAHR": doc["GJAHR"],
                "BUZEI": "002",
                "KOART": "K",
                "HKONT": "160000",
                "LIFNR": vendor["LIFNR"],
                "DMBTR": amount,
                "SHKZG": "S",  # Debit
                "SGTXT": f"Payment to {vendor['NAME1']}",
                "ZFBDT": doc["BLDAT"],
                "ZBD1T": "",
                "ZBD1P": ""
            })

        else:  # Credit Memo (KG)
            vendor = vendors_df.sample(1).iloc[0]
            amount = round(random.uniform(100, 10000), 2)

            # Vendor line (Debit)
            line_items.append({
                "MANDT": doc["MANDT"],
                "BUKRS": doc["BUKRS"],
                "BELNR": doc["BELNR"],
                "GJAHR": doc["GJAHR"],
                "BUZEI": "001",
                "KOART": "K",
                "HKONT": "160000",
                "LIFNR": vendor["LIFNR"],
                "DMBTR": amount,
                "SHKZG": "S",
                "SGTXT": f"Credit from {vendor['NAME1']}",
                "ZFBDT": doc["BLDAT"],
                "ZBD1T": "",
                "ZBD1P": ""
            })

            # GL account (Credit)
            gl_account = random.choices(
                list(GL_ACCOUNTS.keys()),
                weights=list(GL_ACCOUNTS.values())
            )[0]

            line_items.append({
                "MANDT": doc["MANDT"],
                "BUKRS": doc["BUKRS"],
                "BELNR": doc["BELNR"],
                "GJAHR": doc["GJAHR"],
                "BUZEI": "002",
                "KOART": "S",
                "HKONT": gl_account,
                "LIFNR": "",
                "DMBTR": amount,
                "SHKZG": "H",
                "SGTXT": "Credit adjustment",
                "ZFBDT": doc["BLDAT"],
                "ZBD1T": "",
                "ZBD1P": ""
            })

    return pd.DataFrame(line_items)

# ============================================================================
# MAIN GENERATION
# ============================================================================

if __name__ == "__main__":
    print("Generating SAP sample data with variety...")
    print(f"Vendors: {NUM_VENDORS}")
    print(f"Documents per year: {NUM_DOCUMENTS_PER_YEAR}")
    print(f"Years: 2023-2024")
    print()

    # Generate vendors
    print("Generating vendor master data...")
    vendors_df = generate_vendors(NUM_VENDORS)

    # Generate documents
    print("Generating document headers...")
    documents_df = generate_documents(NUM_DOCUMENTS_PER_YEAR)

    # Generate line items
    print("Generating line items...")
    line_items_df = generate_line_items(documents_df, vendors_df)

    # Save to CSV
    output_dir = "../"

    print(f"\nSaving files to {output_dir}...")
    vendors_df.to_csv(f"{output_dir}/sap_lfa1_vendor_master.csv", index=False)
    documents_df.to_csv(f"{output_dir}/sap_bkpf_document_header.csv", index=False)
    line_items_df.to_csv(f"{output_dir}/sap_bseg_line_items.csv", index=False)

    # Statistics
    print("\n" + "="*60)
    print("GENERATION COMPLETE")
    print("="*60)
    print(f"\nVendor Master (LFA1):")
    print(f"  - Total vendors: {len(vendors_df)}")
    print(f"  - Cities: {vendors_df['ORT01'].nunique()}")
    print(f"  - Vendor groups: {vendors_df['KTOKK'].nunique()}")
    print(f"  - Payment terms: {vendors_df['ZTERM'].nunique()}")

    print(f"\nDocument Headers (BKPF):")
    print(f"  - Total documents: {len(documents_df)}")
    print(f"  - Years: {sorted(documents_df['GJAHR'].unique())}")
    print(f"  - Company codes: {sorted(documents_df['BUKRS'].unique())}")
    print(f"  - Document types:")
    for doc_type in documents_df['BLART'].unique():
        count = len(documents_df[documents_df['BLART'] == doc_type])
        pct = count / len(documents_df) * 100
        print(f"    - {doc_type}: {count} ({pct:.1f}%)")

    print(f"\nLine Items (BSEG):")
    print(f"  - Total line items: {len(line_items_df)}")
    print(f"  - Account types:")
    for koart in line_items_df['KOART'].unique():
        count = len(line_items_df[line_items_df['KOART'] == koart])
        pct = count / len(line_items_df) * 100
        type_name = "Vendor" if koart == "K" else "GL Account"
        print(f"    - {koart} ({type_name}): {count} ({pct:.1f}%)")

    print(f"\n  - GL Accounts used: {line_items_df[line_items_df['KOART'] == 'S']['HKONT'].nunique()}")
    print(f"  - Vendors used: {line_items_df[line_items_df['KOART'] == 'K']['LIFNR'].nunique()}")

    print(f"\n  - Amount statistics:")
    vendor_amounts = line_items_df[line_items_df['KOART'] == 'K']['DMBTR'].astype(float)
    print(f"    - Min: €{vendor_amounts.min():,.2f}")
    print(f"    - Max: €{vendor_amounts.max():,.2f}")
    print(f"    - Mean: €{vendor_amounts.mean():,.2f}")
    print(f"    - Median: €{vendor_amounts.median():,.2f}")

    print("\n✅ Files created successfully!")
    print(f"   - {output_dir}/sap_lfa1_vendor_master.csv")
    print(f"   - {output_dir}/sap_bkpf_document_header.csv")
    print(f"   - {output_dir}/sap_bseg_line_items.csv")
    print("\nRun your Fabric dataflow to ingest this new data!")
