# SAP Table Reference - Accounts Payable

This document describes the SAP tables used in this project with their authentic field structures.

**Sources:**
- [BKPF - Accounting Document Header](https://leanx.eu/en/sap/table/bkpf.html)
- [BSEG - Accounting Document Segment (Line Items)](https://leanx.eu/en/sap/table/bseg.html)
- [LFA1 - Vendor Master (General Section)](https://leanx.eu/en/sap/table/lfa1.html)

---

## BKPF - Accounting Document Header

**Description:** Stores header lines for accounting documents in SAP Financial Accounting

**Purpose in this project:** Document-level information (date, type, currency, user) for AP transactions

### Key Fields

| Field | Description | Type | Length | Key |
|-------|-------------|------|--------|-----|
| MANDT | Client | CLNT | 3 | ✓ |
| BUKRS | Company Code | CHAR | 4 | ✓ |
| BELNR | Accounting Document Number | CHAR | 10 | ✓ |
| GJAHR | Fiscal Year | NUMC | 4 | ✓ |

### Important Fields for AP Analytics

| Field | Description | Type | Length | Notes |
|-------|-------------|------|--------|-------|
| BLART | Document Type | CHAR | 2 | RE=Invoice, KZ=Payment, KG=Credit Memo |
| BLDAT | Document Date | DATS | 8 | Date on the document |
| BUDAT | Posting Date | DATS | 8 | Date posted to accounting |
| CPUDT | Entry Date | DATS | 8 | Date document was entered |
| WAERS | Currency Key | CUKY | 5 | Usually EUR, USD, etc. |
| KURSF | Exchange Rate | DEC | 9(5) | For foreign currency |
| USNAM | User Name | CHAR | 12 | Who created the document |
| TCODE | Transaction Code | CHAR | 20 | SAP transaction used (FB60, F-53, etc.) |
| BKTXT | Document Header Text | CHAR | 25 | Description |
| XBLNR | Reference Document Number | CHAR | 16 | External reference (invoice #) |
| BSTAT | Document Status | CHAR | 1 | Blank=normal, D=deleted |
| STBLG | Reverse Document Number | CHAR | 10 | If reversed |
| STJAH | Reverse Fiscal Year | NUMC | 4 | Year of reversal |

### Typical Document Types (BLART)

| Code | Description | Usage |
|------|-------------|-------|
| RE | Invoice | Vendor invoices |
| KR | Credit Memo | Vendor credit notes |
| KZ | Payment | Outgoing payments |
| KG | Credit Memo | General credit memo |
| SA | G/L Account Document | Manual journal entries |

### Date Fields Explained

- **BLDAT (Document Date):** Date on the physical invoice/document
- **BUDAT (Posting Date):** When it was posted to the general ledger
- **CPUDT (Entry Date):** When it was entered into SAP system

**Typical Pattern:** BLDAT (invoice date) → CPUDT (entered in SAP) → BUDAT (posted to GL)

---

## BSEG - Accounting Document Segment (Line Items)

**Description:** Stores line items for accounting documents (300+ fields)

**Purpose in this project:** Individual transaction lines linking vendors, GL accounts, and amounts

### Key Fields

| Field | Description | Type | Length | Key |
|-------|-------------|------|--------|-----|
| MANDT | Client | CLNT | 3 | ✓ |
| BUKRS | Company Code | CHAR | 4 | ✓ |
| BELNR | Accounting Document Number | CHAR | 10 | ✓ |
| GJAHR | Fiscal Year | NUMC | 4 | ✓ |
| BUZEI | Line Item Number | NUMC | 3 | ✓ |

### Critical Fields for AP Analytics

| Field | Description | Type | Length | Notes |
|-------|-------------|------|--------|-------|
| KOART | Account Type | CHAR | 1 | K=Vendor, D=Customer, S=GL, A=Asset, M=Material |
| SHKZG | Debit/Credit Indicator | CHAR | 1 | S=Debit, H=Credit |
| DMBTR | Amount in Local Currency | CURR | 13(2) | Main amount field |
| WRBTR | Amount in Document Currency | CURR | 13(2) | If foreign currency |
| PSWSL | Document Currency | CUKY | 5 | Currency of WRBTR |

### Account-Specific Fields

**For Vendor Lines (KOART = 'K'):**

| Field | Description | Type | Length | Notes |
|-------|-------------|------|--------|-------|
| LIFNR | Vendor Account Number | CHAR | 10 | Links to LFA1 |
| ZTERM | Payment Terms | CHAR | 4 | Links to payment terms master |
| ZFBDT | Baseline Date for Due Date Calculation | DATS | 8 | Start date for payment terms |
| ZBD1T | Cash Discount Days 1 | DEC | 3 | Days for first discount |
| ZBD1P | Cash Discount Percentage 1 | DEC | 5(3) | % discount if paid early |
| ZBD2T | Cash Discount Days 2 | DEC | 3 | Days for second discount tier |
| ZBD2P | Cash Discount Percentage 2 | DEC | 5(3) | Second discount % |
| ZBD3T | Net Payment Terms | DEC | 3 | Days until due (no discount) |
| SKFBT | Amount Eligible for Cash Discount | CURR | 13(2) | Base for discount calc |

**For GL Account Lines (KOART = 'S'):**

| Field | Description | Type | Length | Notes |
|-------|-------------|------|--------|-------|
| HKONT | General Ledger Account | CHAR | 10 | Expense/asset account |
| KOSTL | Cost Center | CHAR | 10 | For cost allocation |
| AUFNR | Order Number | CHAR | 12 | Internal order |
| PRCTR | Profit Center | CHAR | 10 | For profit center accounting |

### Text and Reference Fields

| Field | Description | Type | Length |
|-------|-------------|------|--------|
| SGTXT | Item Text | CHAR | 50 |
| ZUONR | Assignment | CHAR | 18 |
| XREF1 | Reference Key 1 | CHAR | 12 |
| XREF2 | Reference Key 2 | CHAR | 12 |

### Tax Fields

| Field | Description | Type | Length |
|-------|-------------|------|--------|
| MWSKZ | Tax Code | CHAR | 2 |
| MWSTS | Tax Amount in Local Currency | CURR | 13(2) |
| TXJCD | Tax Jurisdiction | CHAR | 15 |

---

## LFA1 - Vendor Master (General Section)

**Description:** Vendor master data (general information, not company-code specific)

**Purpose in this project:** Vendor names, addresses, and basic attributes

### Key Field

| Field | Description | Type | Length | Key |
|-------|-------------|------|--------|-----|
| MANDT | Client | CLNT | 3 | ✓ |
| LIFNR | Vendor Account Number | CHAR | 10 | ✓ |

### Basic Vendor Information

| Field | Description | Type | Length | Notes |
|-------|-------------|------|--------|-------|
| NAME1 | Vendor Name 1 | CHAR | 35 | Primary name |
| NAME2 | Vendor Name 2 | CHAR | 35 | Additional name |
| NAME3 | Vendor Name 3 | CHAR | 35 | Additional name |
| NAME4 | Vendor Name 4 | CHAR | 35 | Additional name |
| SORTL | Sort Field | CHAR | 10 | For alphabetical sorting |
| STRAS | Street and House Number | CHAR | 35 | Address |
| ORT01 | City | CHAR | 35 | City |
| ORT02 | District | CHAR | 35 | District/Region |
| PSTLZ | Postal Code | CHAR | 10 | ZIP code |
| LAND1 | Country Key | CHAR | 3 | DE, US, FR, etc. |
| REGIO | Region | CHAR | 3 | State/Province |

### Contact Information

| Field | Description | Type | Length |
|-------|-------------|------|--------|
| TELF1 | Telephone 1 | CHAR | 16 |
| TELF2 | Telephone 2 | CHAR | 16 |
| TELFX | Fax Number | CHAR | 31 |
| SMTP_ADDR | Email Address | CHAR | 241 |

### Tax and Legal Information

| Field | Description | Type | Length | Notes |
|-------|-------------|------|--------|-------|
| STCD1 | Tax Number 1 | CHAR | 16 | VAT registration number |
| STCD2 | Tax Number 2 | CHAR | 11 | Additional tax ID |
| STCD3 | Tax Number 3 | CHAR | 18 | Tax number 3 |
| STCD4 | Tax Number 4 | CHAR | 18 | Tax number 4 |
| STKZA | Recipient of Goods Statistics | CHAR | 1 | Statistical indicator |
| STKZU | Liable for VAT | CHAR | 1 | VAT liability flag |

### Administrative Fields

| Field | Description | Type | Length | Notes |
|-------|-------------|------|--------|-------|
| KTOKK | Vendor Account Group | CHAR | 4 | KRED, LIEF, etc. |
| ANRED | Title | CHAR | 15 | Mr., Ms., Company, etc. |
| BAHNS | Train Station | CHAR | 25 | Nearest train station |
| BAHNE | International Location Number 1 | CHAR | 10 | ILN |
| KONZS | Group Key | CHAR | 10 | Corporate group |
| KUNNR | Customer Number | CHAR | 10 | If also a customer |
| LOEVM | Central Deletion Flag | CHAR | 1 | X=flagged for deletion |
| SPERR | Central Posting Block | CHAR | 1 | Block for all transactions |
| SPERM | Purchasing Block | CHAR | 1 | Block for purchasing |
| XCPDK | One-Time Account | CHAR | 1 | X=one-time vendor |

### Industry and Classification

| Field | Description | Type | Length |
|-------|-------------|------|--------|
| BRSCH | Industry Key | CHAR | 4 |
| LTSGA | Vendor Quality Management Active | CHAR | 1 |

### Creation/Change Tracking

| Field | Description | Type | Length |
|-------|-------------|------|--------|
| ERDAT | Date Created | DATS | 8 |
| ERNAM | Name of Person Created | CHAR | 12 |
| LNRZA | Vendor Sub-Range | CHAR | 2 |

---

## Table Relationships

### Primary Relationship: BKPF ←→ BSEG

**Join Condition:**
```sql
BKPF.MANDT = BSEG.MANDT
AND BKPF.BUKRS = BSEG.BUKRS
AND BKPF.BELNR = BSEG.BELNR
AND BKPF.GJAHR = BSEG.GJAHR
```

**Cardinality:** 1 BKPF : N BSEG (one header, many line items)

### Vendor Lookup: BSEG → LFA1

**Join Condition:**
```sql
BSEG.MANDT = LFA1.MANDT
AND BSEG.LIFNR = LFA1.LIFNR
WHERE BSEG.KOART = 'K'  -- Only for vendor line items
```

**Cardinality:** N BSEG : 1 LFA1 (many transactions per vendor)

---

## Fields Used in This Project

### Minimum Required Fields

**BKPF (Document Header):**
- MANDT, BUKRS, BELNR, GJAHR *(keys)*
- BLART *(document type)*
- BLDAT *(document date)*
- BUDAT *(posting date)*
- WAERS *(currency)*

**BSEG (Line Items):**
- MANDT, BUKRS, BELNR, GJAHR, BUZEI *(keys)*
- KOART *(account type: K or S)*
- SHKZG *(debit/credit)*
- DMBTR *(amount)*
- LIFNR *(vendor number, for KOART='K')*
- HKONT *(GL account, for KOART='S')*
- ZFBDT *(baseline date)*
- ZBD1T, ZBD1P *(cash discount terms)*

**LFA1 (Vendor Master):**
- MANDT, LIFNR *(keys)*
- NAME1 *(vendor name)*
- ORT01 *(city)*
- LAND1 *(country)*
- STCD1 *(tax number)*
- KTOKK *(account group)*

### Optional/Enhanced Fields

For more realistic data, consider adding:
- **BKPF:** BKTXT, XBLNR, USNAM, TCODE, CPUDT
- **BSEG:** SGTXT, KOSTL, ZTERM, ZUONR
- **LFA1:** STRAS, PSTLZ, REGIO, BRSCH

---

## SAP Standard Patterns

### Invoice Document Pattern

**BKPF:**
- BLART = 'RE' (Invoice)
- BLDAT = Invoice date
- BUDAT = Posting date (usually same or later)

**BSEG Lines:**
1. **GL Account Lines (KOART = 'S'):** Expense accounts (Debit, SHKZG = 'S')
2. **Vendor Line (KOART = 'K'):** Vendor clearing account (Credit, SHKZG = 'H')

**Balance Rule:** Sum of debits = Sum of credits for each document

### Payment Document Pattern

**BKPF:**
- BLART = 'KZ' (Payment)

**BSEG Lines:**
1. **Vendor Line (KOART = 'K'):** Clears vendor payable (Debit, SHKZG = 'S')
2. **Bank Line (KOART = 'S'):** Bank account (Credit, SHKZG = 'H')

### Credit Memo Pattern

**BKPF:**
- BLART = 'KG' or 'KR'

**BSEG Lines:**
1. **Vendor Line (KOART = 'K'):** Reduces payable (Debit, SHKZG = 'S')
2. **GL Account Line (KOART = 'S'):** Reduces expense (Credit, SHKZG = 'H')

---

## Data Generation Guidelines

### Realistic Data Patterns

1. **Vendor Number Format:**
   - 10 characters, zero-padded
   - Example: 0000100001, 0000100002

2. **Document Number:**
   - 10 characters, numeric
   - Typically sequential within fiscal year
   - Example: 5100000001, 5100000002

3. **Date Formats:**
   - YYYYMMDD (8 digits)
   - Example: 20240115 = January 15, 2024

4. **Amount Distribution:**
   - Small invoices: €100 - €1,000
   - Medium: €1,000 - €10,000
   - Large: €10,000 - €100,000+
   - Follow realistic business patterns

5. **Currency:**
   - Mostly EUR for German companies
   - Occasional USD, GBP for international vendors

6. **Payment Terms:**
   - Standard: 30 days net, 2% discount within 14 days
   - Variations: 14, 30, 45, 60, 90 days
   - Cash discount: 1-3%

---

## References

- **LeanX SAP Tables:** https://leanx.eu/en/sap/
- **SAP Help:** https://help.sap.com/
- **SAP Table Documentation:** Standard SAP documentation

---

**Version:** 1.0
**Last Updated:** October 2024
**Purpose:** Reference for data generation and transformation logic
