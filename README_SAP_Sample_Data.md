# SAP Accounts Payable Sample Data

This repository contains realistic SAP accounts payable sample data for testing and development purposes, featuring German company context with over 1,000+ records across three core SAP tables.

## Data Overview

### Files Generated
- `sap_lfa1_vendor_master.csv` - Vendor master data (50 records)
- `sap_bkpf_document_header.csv` - Accounting document headers (142 records)
- `sap_bseg_line_items.csv` - Accounting document line items (268 records)
- `data_validation_queries.sql` - SQL queries for data validation and analysis

### Data Characteristics
- **Time Period**: 12 months of 2024 (January - December)
- **Currency**: EUR (Euro)
- **Company Context**: German companies with realistic vendor names
- **Document Types**:
  - RE (Invoice documents)
  - KZ (Payment documents)
- **Total Invoice Amount**: Over €3.5 million across all transactions
- **German VAT**: 19% VAT rate applied to all invoices

## Table Structures

### LFA1 - Vendor Master Data
Contains 50 major German companies including:
- **Key Fields**: MANDT, LIFNR (Vendor Number)
- **Vendor Types**: Siemens AG, BASF SE, Volkswagen AG, BMW AG, etc.
- **Address Data**: Complete German addresses with postal codes
- **Tax Information**: German tax numbers and VAT registration

### BKPF - Document Header Data
Contains 142 accounting documents:
- **Key Fields**: MANDT, BUKRS, BELNR, GJAHR
- **Document Types**: Invoice (RE) and Payment (KZ) documents
- **Date Range**: January 2024 - December 2024
- **Users**: Realistic German usernames (MUELLER, SCHMIDT, etc.)

### BSEG - Line Item Data
Contains 268 line items with proper accounting logic:
- **Key Fields**: MANDT, BUKRS, BELNR, GJAHR, BUZEI
- **Account Types**:
  - K (Vendors) - Payable accounts
  - S (G/L Accounts) - Tax and expense accounts
- **Debit/Credit**: Balanced entries with proper SHKZG indicators
- **Payment Terms**: 30-day payment terms with 2% early payment discount

## Data Relationships

The data maintains proper SAP referential integrity:

1. **BKPF ↔ BSEG**: Every line item links to a document header
2. **BSEG ↔ LFA1**: All vendor line items link to vendor master records
3. **Document Balance**: All documents are properly balanced (debits = credits)

## Usage Examples

### Basic Join Query
```sql
SELECT
    h.BELNR as document_number,
    h.BLDAT as document_date,
    v.NAME1 as vendor_name,
    b.DMBTR as amount
FROM sap_bkpf_document_header h
JOIN sap_bseg_line_items b ON h.BELNR = b.BELNR
JOIN sap_lfa1_vendor_master v ON b.LIFNR = v.LIFNR
WHERE b.KOART = 'K';
```

### Monthly AP Summary
```sql
SELECT
    SUBSTR(h.BLDAT, 1, 6) as year_month,
    COUNT(*) as invoice_count,
    SUM(b.DMBTR) as total_amount
FROM sap_bkpf_document_header h
JOIN sap_bseg_line_items b ON h.BELNR = b.BELNR
WHERE h.BLART = 'RE' AND b.KOART = 'K'
GROUP BY SUBSTR(h.BLDAT, 1, 6);
```

## Account Codes Used

- **160000**: Accounts Payable (vendor balances)
- **543210**: Input VAT 19%
- **400000**: Material Expenses
- **440000**: Energy Costs
- **450000**: Telecommunications
- **460000**: Insurance
- **470000**: Cleaning Costs
- **480000**: Office Equipment
- **500000**: Financial Costs
- **520000**: IT Costs
- **630000**: Transportation Costs
- **640000**: Vehicle Costs
- **650000**: Travel Expenses

## Data Validation

Use the provided `data_validation_queries.sql` to verify:
- Document balance validation
- Referential integrity checks
- Record count summaries
- Sample relationship queries

## Business Context

The sample data represents a typical German mid-size company with:
- Manufacturing operations (materials, equipment)
- Service procurement (IT, telecommunications, insurance)
- Fleet management (vehicles, fuel)
- Regular operational expenses (utilities, travel, office supplies)

All vendor names are real German corporations to ensure realistic testing scenarios while maintaining data privacy through the use of public company information only.