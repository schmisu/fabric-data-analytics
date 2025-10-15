#!/usr/bin/env python3
"""
Generate realistic SAP Accounts Payable sample data following authentic SAP table structure
Based on SAP tables: BKPF, BSEG, LFA1
Reference: sample-data/SAP_TABLE_REFERENCE.md

- Two years (2023-2024) for YoY analysis
- Realistic SAP field structures
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

NUM_VENDORS = 100
NUM_DOCUMENTS_PER_YEAR = 500
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

# German cities with streets and postal codes
CITIES_DATA = [
    ("München", "80331", "BY"), ("Berlin", "10115", "BE"), ("Hamburg", "20095", "HH"),
    ("Frankfurt", "60311", "HE"), ("Köln", "50667", "NW"), ("Stuttgart", "70173", "BW"),
    ("Düsseldorf", "40210", "NW"), ("Leipzig", "04109", "SN"), ("Dortmund", "44135", "NW"),
    ("Essen", "45127", "NW"), ("Bremen", "28195", "HB"), ("Dresden", "01067", "SN"),
    ("Hannover", "30159", "NI"), ("Nürnberg", "90402", "BY"), ("Bochum", "44787", "NW"),
]

STREETS = [
    "Hauptstraße", "Bahnhofstraße", "Marktplatz", "Kirchstraße", "Gartenstraße",
    "Schulstraße", "Bergstraße", "Am Markt", "Lindenstraße", "Dorfstraße"
]

# Industry codes
INDUSTRIES = ["0001", "0002", "0003", "0004", "0005", "0006", "0007", "0008"]

# Vendor account groups
VENDOR_GROUPS = ["KRED", "LIEF", "SONST", "INTER", "EINM"]

# Payment terms (ZTERM code, net days, discount %, discount days)
PAYMENT_TERMS_OPTIONS = [
    ("0001", 30, 2.0, 14),   # 30 days net, 2% within 14
    ("0002", 60, 3.0, 10),   # 60 days net, 3% within 10
    ("0003", 14, 0.0, 0),    # 14 days net, no discount
    ("0004", 45, 2.5, 21),   # 45 days net, 2.5% within 21
    ("0005", 90, 1.5, 30),   # 90 days net, 1.5% within 30
    ("0006", 30, 0.0, 0),    # 30 days net, no discount
    ("0007", 7, 0.0, 0),     # 7 days immediate
]

def generate_vendors(num_vendors=100):
    """Generate LFA1 vendor master data with realistic SAP fields"""
    vendors = []

    for i in range(num_vendors):
        vendor_number = f"{(i+1):010d}"  # 0000000001, etc.

        # Use company names or generate generic
        if i < len(VENDOR_NAMES):
            name = VENDOR_NAMES[i]
        else:
            name = f"Firma {chr(65 + (i % 26))} GmbH & Co. KG {i}"

        # Select city data
        city_data = random.choice(CITIES_DATA)
        city, postal_code, region = city_data

        # Generate street address
        street = f"{random.choice(STREETS)} {random.randint(1, 150)}"

        # Payment terms
        payment_term = random.choice(PAYMENT_TERMS_OPTIONS)

        vendors.append({
            # Key fields
            "MANDT": "100",
            "LIFNR": vendor_number,

            # Name fields
            "NAME1": name[:35],  # Max 35 chars in SAP
            "NAME2": "",
            "SORTL": name[:10].upper(),

            # Address fields
            "STRAS": street[:35],
            "ORT01": city,
            "PSTLZ": postal_code,
            "LAND1": "DE",
            "REGIO": region,

            # Tax and legal
            "STCD1": f"DE{random.randint(100000000, 999999999)}",  # VAT registration
            "STCD2": f"{random.randint(1000000000, 9999999999)}",
            "STCEG": f"DE{random.randint(100000000, 999999999)}",  # EU VAT number

            # Administrative
            "KTOKK": random.choice(VENDOR_GROUPS),
            "BRSCH": random.choice(INDUSTRIES),
            "LOEVM": "",  # Not flagged for deletion
            "SPERR": "",  # Not blocked

            # Contact (minimal for this project)
            "TELF1": "",
            "SMTP_ADDR": "",
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

COMPANY_CODES = ["1000", "2000", "3000"]

# SAP transaction codes for different document types
TCODE_MAP = {
    "RE": ["FB60", "MIRO"],  # Vendor invoice
    "KZ": ["F-53", "F110"],  # Payment
    "KG": ["FB65"],          # Credit memo
}

def generate_documents(num_docs_per_year=500):
    """Generate BKPF document headers with realistic SAP fields"""
    documents = []
    doc_counter = 5100000001  # SAP style document numbering

    for year in [2023, 2024]:
        for i in range(num_docs_per_year):
            # Seasonal pattern: more in Q4
            month_weights = [8, 8, 9, 9, 7, 6, 6, 7, 9, 10, 11, 12]
            month = random.choices(range(1, 13), weights=month_weights)[0]
            day = random.randint(1, 28)

            # Document date (on invoice)
            doc_date = datetime(year, month, day)

            # Entry date (when entered in SAP) - usually same day or 1-2 days later
            entry_date = doc_date + timedelta(days=random.randint(0, 2))

            # Posting date (when posted to GL) - usually same as entry or next day
            posting_date = entry_date + timedelta(days=random.randint(0, 1))

            # Document type
            doc_type = random.choices(
                [dt[0] for dt in DOCUMENT_TYPES],
                weights=[dt[1] for dt in DOCUMENT_TYPES]
            )[0]

            doc_number = f"{doc_counter:010d}"

            # Transaction code based on doc type
            tcode = random.choice(TCODE_MAP[doc_type])

            # Header text based on type
            type_desc = {"RE": "Invoice", "KZ": "Payment", "KG": "Credit Memo"}[doc_type]

            documents.append({
                # Key fields
                "MANDT": "100",
                "BUKRS": random.choice(COMPANY_CODES),
                "BELNR": doc_number,
                "GJAHR": str(year),

                # Document type and dates
                "BLART": doc_type,
                "BLDAT": doc_date.strftime("%Y%m%d"),
                "BUDAT": posting_date.strftime("%Y%m%d"),
                "CPUDT": entry_date.strftime("%Y%m%d"),

                # Currency and exchange
                "WAERS": "EUR",
                "KURSF": "1.00000",  # Exchange rate (1.0 for EUR)

                # User and system
                "USNAM": f"USER{random.randint(1, 20):02d}",
                "TCODE": tcode,

                # Text fields
                "BKTXT": f"{type_desc} {doc_number}"[:25],
                "XBLNR": f"EXT{random.randint(100000, 999999)}"[:16] if doc_type == "RE" else "",

                # Status fields
                "BSTAT": "",  # Normal (not deleted)
                "STBLG": "",  # Not reversed
                "STJAH": "",
            })

            doc_counter += 1

    return pd.DataFrame(documents)

# ============================================================================
# LINE ITEMS (BSEG)
# ============================================================================

GL_ACCOUNTS = {
    # Expense accounts (weighted by frequency)
    "400000": 0.15,  # Raw materials
    "410000": 0.12,  # Consumables
    "420000": 0.10,  # Services
    "430000": 0.08,  # Maintenance
    "440000": 0.08,  # IT/Software
    "450000": 0.07,  # Marketing
    "460000": 0.06,  # Travel
    "470000": 0.05,  # Utilities
    "480000": 0.05,  # Rent
    "490000": 0.04,  # Insurance
    "500000": 0.04,  # Consulting
    "510000": 0.03,  # Legal
    "520000": 0.03,  # Training
    "160000": 0.10,  # Vendor clearing (AP account)
}

# Cost centers
COST_CENTERS = ["1000", "2000", "3000", "4000", "5000"]

def generate_line_items(documents_df, vendors_df):
    """Generate BSEG line items with realistic SAP fields"""
    line_items = []

    for _, doc in documents_df.iterrows():
        doc_type = doc["BLART"]
        num_lines = random.randint(1, 5) if doc_type == "RE" else random.randint(1, 3)

        if doc_type == "RE":  # Invoice
            # Generate GL expense lines (Debit)
            gl_total = 0
            gl_lines = []

            for line_num in range(num_lines):
                gl_account = random.choices(
                    list(GL_ACCOUNTS.keys()),
                    weights=list(GL_ACCOUNTS.values())
                )[0]

                # Amount varies by account
                if gl_account in ["400000", "410000"]:  # Materials
                    amount = round(random.uniform(500, 50000), 2)
                elif gl_account in ["420000", "430000", "440000"]:  # Services
                    amount = round(random.uniform(200, 20000), 2)
                elif gl_account in ["480000", "490000"]:  # Rent/Insurance
                    amount = round(random.uniform(1000, 100000), 2)
                else:
                    amount = round(random.uniform(100, 10000), 2)

                gl_total += amount
                gl_lines.append((gl_account, amount))

            # Add GL lines
            for line_num, (gl_account, amount) in enumerate(gl_lines, start=1):
                # Calculate tax (19% German VAT for some accounts)
                tax_amount = 0
                if gl_account in ["420000", "440000", "450000"]:  # Services, IT, Marketing
                    tax_amount = round(amount * 0.19, 2)

                line_items.append({
                    # Key fields
                    "MANDT": doc["MANDT"],
                    "BUKRS": doc["BUKRS"],
                    "BELNR": doc["BELNR"],
                    "GJAHR": doc["GJAHR"],
                    "BUZEI": f"{line_num:03d}",

                    # Account type and details
                    "KOART": "S",  # GL account
                    "SHKZG": "S",  # Debit
                    "DMBTR": f"{amount:.2f}",
                    "WRBTR": f"{amount:.2f}",
                    "PSWSL": "EUR",
                    "MWSTS": f"{tax_amount:.2f}",  # Tax amount

                    # GL-specific
                    "HKONT": gl_account,
                    "KOSTL": random.choice(COST_CENTERS),

                    # Vendor fields (empty for GL lines)
                    "LIFNR": "",
                    "ZFBDT": "",
                    "ZBD1T": "",
                    "ZBD1P": "",
                    "ZBD2T": "",  # Second discount tier
                    "ZBD3T": "",
                    "ZTERM": "",  # Payment terms
                    "SKFBT": "",  # Cash discount base amount

                    # Text
                    "SGTXT": f"Expense {gl_account}"[:50],
                    "ZUONR": "",
                })

            # Add vendor line (Credit, balances the document)
            vendor = vendors_df.sample(1).iloc[0]

            # Get payment terms from vendor
            vendor_payment_term = vendor["KTOKK"]  # Account group
            # Find actual payment terms
            payment_term = random.choice(PAYMENT_TERMS_OPTIONS)
            zterm_code = payment_term[0]
            net_days = payment_term[1]
            disc_pct = payment_term[2]
            disc_days = payment_term[3]

            # Calculate cash discount base amount
            skfbt_amount = gl_total  # Base amount eligible for discount

            line_items.append({
                # Key fields
                "MANDT": doc["MANDT"],
                "BUKRS": doc["BUKRS"],
                "BELNR": doc["BELNR"],
                "GJAHR": doc["GJAHR"],
                "BUZEI": f"{len(gl_lines) + 1:03d}",

                # Account type and details
                "KOART": "K",  # Vendor
                "SHKZG": "H",  # Credit
                "DMBTR": f"{gl_total:.2f}",
                "WRBTR": f"{gl_total:.2f}",
                "PSWSL": "EUR",
                "MWSTS": "0.00",  # No tax on vendor line

                # Vendor-specific payment terms
                "LIFNR": vendor["LIFNR"],
                "ZFBDT": doc["BLDAT"],  # Baseline date
                "ZBD1T": str(disc_days) if disc_days > 0 else "",
                "ZBD1P": f"{disc_pct:.3f}" if disc_pct > 0 else "",
                "ZBD2T": "",  # No second discount tier for simplicity
                "ZBD3T": str(net_days),
                "ZTERM": zterm_code,
                "SKFBT": f"{skfbt_amount:.2f}" if disc_pct > 0 else "",

                # GL fields (vendor clearing account)
                "HKONT": "160000",
                "KOSTL": "",

                # Text
                "SGTXT": f"AP {vendor['NAME1'][:30]}"[:50],
                "ZUONR": vendor["LIFNR"],
            })

        elif doc_type == "KZ":  # Payment
            amount = round(random.uniform(1000, 100000), 2)

            # Bank line (Credit)
            line_items.append({
                "MANDT": doc["MANDT"],
                "BUKRS": doc["BUKRS"],
                "BELNR": doc["BELNR"],
                "GJAHR": doc["GJAHR"],
                "BUZEI": "001",
                "KOART": "S",
                "SHKZG": "H",  # Credit
                "DMBTR": f"{amount:.2f}",
                "WRBTR": f"{amount:.2f}",
                "PSWSL": "EUR",
                "MWSTS": "0.00",
                "HKONT": "113100",  # Bank
                "KOSTL": "",
                "LIFNR": "",
                "ZFBDT": "",
                "ZBD1T": "",
                "ZBD1P": "",
                "ZBD2T": "",
                "ZBD3T": "",
                "ZTERM": "",
                "SKFBT": "",
                "SGTXT": "Payment",
                "ZUONR": "",
            })

            # Vendor line (Debit, clears AP)
            vendor = vendors_df.sample(1).iloc[0]
            line_items.append({
                "MANDT": doc["MANDT"],
                "BUKRS": doc["BUKRS"],
                "BELNR": doc["BELNR"],
                "GJAHR": doc["GJAHR"],
                "BUZEI": "002",
                "KOART": "K",
                "SHKZG": "S",  # Debit
                "DMBTR": f"{amount:.2f}",
                "WRBTR": f"{amount:.2f}",
                "PSWSL": "EUR",
                "MWSTS": "0.00",
                "HKONT": "160000",
                "KOSTL": "",
                "LIFNR": vendor["LIFNR"],
                "ZFBDT": "",
                "ZBD1T": "",
                "ZBD1P": "",
                "ZBD2T": "",
                "ZBD3T": "",
                "ZTERM": "",
                "SKFBT": "",
                "SGTXT": f"Payment to {vendor['NAME1'][:30]}"[:50],
                "ZUONR": vendor["LIFNR"],
            })

        else:  # Credit Memo (KG)
            vendor = vendors_df.sample(1).iloc[0]
            amount = round(random.uniform(100, 10000), 2)

            # Vendor line (Debit, reduces AP)
            line_items.append({
                "MANDT": doc["MANDT"],
                "BUKRS": doc["BUKRS"],
                "BELNR": doc["BELNR"],
                "GJAHR": doc["GJAHR"],
                "BUZEI": "001",
                "KOART": "K",
                "SHKZG": "S",
                "DMBTR": f"{amount:.2f}",
                "WRBTR": f"{amount:.2f}",
                "PSWSL": "EUR",
                "MWSTS": "0.00",
                "HKONT": "160000",
                "KOSTL": "",
                "LIFNR": vendor["LIFNR"],
                "ZFBDT": "",
                "ZBD1T": "",
                "ZBD1P": "",
                "ZBD2T": "",
                "ZBD3T": "",
                "ZTERM": "",
                "SKFBT": "",
                "SGTXT": f"Credit from {vendor['NAME1'][:30]}"[:50],
                "ZUONR": vendor["LIFNR"],
            })

            # GL line (Credit, reduces expense)
            gl_account = random.choice(list(GL_ACCOUNTS.keys()))
            line_items.append({
                "MANDT": doc["MANDT"],
                "BUKRS": doc["BUKRS"],
                "BELNR": doc["BELNR"],
                "GJAHR": doc["GJAHR"],
                "BUZEI": "002",
                "KOART": "S",
                "SHKZG": "H",
                "DMBTR": f"{amount:.2f}",
                "WRBTR": f"{amount:.2f}",
                "PSWSL": "EUR",
                "MWSTS": "0.00",
                "HKONT": gl_account,
                "KOSTL": random.choice(COST_CENTERS),
                "LIFNR": "",
                "ZFBDT": "",
                "ZBD1T": "",
                "ZBD1P": "",
                "ZBD2T": "",
                "ZBD3T": "",
                "ZTERM": "",
                "SKFBT": "",
                "SGTXT": "Credit adjustment",
                "ZUONR": "",
            })

    return pd.DataFrame(line_items)

# ============================================================================
# MAIN GENERATION
# ============================================================================

if __name__ == "__main__":
    print("="*70)
    print("SAP Accounts Payable Sample Data Generator")
    print("Following authentic SAP table structures (BKPF, BSEG, LFA1)")
    print("="*70)
    print(f"\nConfiguration:")
    print(f"  - Vendors: {NUM_VENDORS}")
    print(f"  - Documents per year: {NUM_DOCUMENTS_PER_YEAR}")
    print(f"  - Years: 2023-2024")
    print()

    # Generate data
    print("Step 1/3: Generating vendor master data (LFA1)...")
    vendors_df = generate_vendors(NUM_VENDORS)

    print("Step 2/3: Generating document headers (BKPF)...")
    documents_df = generate_documents(NUM_DOCUMENTS_PER_YEAR)

    print("Step 3/3: Generating line items (BSEG)...")
    line_items_df = generate_line_items(documents_df, vendors_df)

    # Save to CSV
    output_dir = "../"

    print(f"\nSaving files to {output_dir}...")
    vendors_df.to_csv(f"{output_dir}/sap_lfa1_vendor_master.csv", index=False)
    documents_df.to_csv(f"{output_dir}/sap_bkpf_document_header.csv", index=False)
    line_items_df.to_csv(f"{output_dir}/sap_bseg_line_items.csv", index=False)

    # Statistics
    print("\n" + "="*70)
    print("GENERATION COMPLETE")
    print("="*70)

    print(f"\nLFA1 - Vendor Master:")
    print(f"  Total vendors: {len(vendors_df)}")
    print(f"  Cities: {vendors_df['ORT01'].nunique()}")
    print(f"  Vendor groups: {vendors_df['KTOKK'].nunique()}")
    print(f"  Fields: {len(vendors_df.columns)}")

    print(f"\nBKPF - Document Headers:")
    print(f"  Total documents: {len(documents_df)}")
    print(f"  Years: {sorted(documents_df['GJAHR'].unique())}")
    print(f"  Company codes: {sorted(documents_df['BUKRS'].unique())}")
    print(f"  Document types:")
    for doc_type in sorted(documents_df['BLART'].unique()):
        count = len(documents_df[documents_df['BLART'] == doc_type])
        pct = count / len(documents_df) * 100
        type_name = {"RE": "Invoice", "KZ": "Payment", "KG": "Credit Memo"}[doc_type]
        print(f"    {doc_type} ({type_name}): {count:4d} ({pct:4.1f}%)")
    print(f"  Fields: {len(documents_df.columns)}")

    print(f"\nBSEG - Line Items:")
    print(f"  Total line items: {len(line_items_df)}")
    print(f"  Account types:")
    for koart in sorted(line_items_df['KOART'].unique()):
        count = len(line_items_df[line_items_df['KOART'] == koart])
        pct = count / len(line_items_df) * 100
        type_name = "Vendor" if koart == "K" else "GL Account"
        print(f"    {koart} ({type_name}): {count:4d} ({pct:4.1f}%)")
    print(f"  GL Accounts: {line_items_df[line_items_df['KOART'] == 'S']['HKONT'].nunique()}")
    print(f"  Vendors used: {line_items_df[line_items_df['KOART'] == 'K']['LIFNR'].nunique()}")
    print(f"  Fields: {len(line_items_df.columns)}")

    print(f"\nAmount Statistics (Vendor Lines):")
    vendor_amounts = line_items_df[line_items_df['KOART'] == 'K']['DMBTR'].astype(float)
    print(f"  Min:    EUR {vendor_amounts.min():>12,.2f}")
    print(f"  Max:    EUR {vendor_amounts.max():>12,.2f}")
    print(f"  Mean:   EUR {vendor_amounts.mean():>12,.2f}")
    print(f"  Median: EUR {vendor_amounts.median():>12,.2f}")

    print("\n" + "="*70)
    print("✅ Files created successfully!")
    print("="*70)
    print(f"  {output_dir}sap_lfa1_vendor_master.csv")
    print(f"  {output_dir}sap_bkpf_document_header.csv")
    print(f"  {output_dir}sap_bseg_line_items.csv")
    print("\nNext: Run your Fabric dataflow to ingest this data!")
    print("="*70)
