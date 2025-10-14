# SAP Sample Data

This folder contains realistic German company sample data for the Accounts Payable analytics solution.

## Files

### sap_bkpf_document_header.csv
**SAP Table**: BKPF (Accounting Document Header)
- **Records**: 142 documents
- **Date Range**: January - December 2024
- **Document Types**: RE (Invoice), KZ (Payment)

**Key Fields**:
- `BUKRS`: Company code (e.g., 1000 = Main Company)
- `BELNR`: Accounting document number
- `GJAHR`: Fiscal year
- `BLART`: Document type
- `BLDAT`: Document date
- `BUDAT`: Posting date
- `WAERS`: Currency (EUR)

### sap_bseg_line_items.csv
**SAP Table**: BSEG (Accounting Document Line Items)
- **Records**: 270 line items
- **Account Types**: K (Vendor), S (G/L Account)

**Key Fields**:
- `BUKRS`, `BELNR`, `GJAHR`: Link to header (BKPF)
- `BUZEI`: Line item number
- `KOART`: Account type (K = Vendor, S = GL)
- `LIFNR`: Vendor number (for type K)
- `HKONT`: G/L account number (for type S)
- `DMBTR`: Amount in local currency
- `SHKZG`: Debit/Credit indicator (S = Debit, H = Credit)
- `ZFBDT`: Baseline date for payment terms
- `ZBD1T`: Cash discount days
- `ZBD1P`: Cash discount percentage

### sap_lfa1_vendor_master.csv
**SAP Table**: LFA1 (Vendor Master Data)
- **Records**: 50 German vendors
- **Industries**: Manufacturing, Utilities, Logistics, Services

**Key Fields**:
- `LIFNR`: Vendor number (10-digit, e.g., 0000100001)
- `NAME1`: Vendor name (e.g., Siemens AG, BASF SE)
- `ORT01`: City
- `LAND1`: Country code (DE = Germany)
- `STCD1`: Tax number
- `KTOKK`: Vendor account group
- `ZTERM`: Payment terms

## Data Characteristics

### Realistic German Vendors
Sample includes well-known German companies:
- **Manufacturing**: Siemens, BASF, Volkswagen, Bosch
- **Utilities**: E.ON, RWE
- **Logistics**: Deutsche Post DHL, DB Schenker
- **Technology**: SAP, Deutsche Telekom
- **Financial**: Deutsche Bank, Allianz

### Transaction Patterns
- **Total Transaction Volume**: €3.5M+ (2024)
- **Average Invoice**: ~€25,000
- **Payment Terms**: Typically 30 days net with 2% cash discount
- **VAT**: 19% standard German VAT included
- **Posting Frequency**: Realistic monthly distribution

### Data Quality
- **Completeness**: 100% for vendor line items (type K)
- **GL Lines**: Type S lines intentionally have no vendor (expected)
- **Date Formats**: YYYYMMDD (SAP standard)
- **Currency**: All amounts in EUR

## Usage in Project

1. **Ingestion**: Load via Dataflow Gen2 to Lakehouse tables
2. **Transformation**: Process with SQL notebook (`sql/create_ap_fact_table.sql`)
3. **Analytics**: Power BI semantic model and reports

## Replacing with Your Data

To use your own SAP data:

1. **Export from SAP** (SE16/SE16N or custom program):
   ```sql
   SELECT * FROM BKPF
   WHERE BUKRS = '1000'
     AND GJAHR = '2024'
     AND BLART IN ('RE', 'KZ')
   ```

2. **Maintain CSV structure**:
   - Keep same column names
   - Use YYYYMMDD date format
   - Ensure proper encoding (UTF-8)

3. **Upload to Fabric**:
   - Use Dataflow Gen2 to load CSVs
   - Point to your file location
   - Follow same transformation steps

## Notes

- Data is for **demonstration purposes** only
- Vendor names are real companies, but transaction data is synthetic
- Payment terms follow standard German business practices
- Cash discount patterns typical for manufacturing sector

---

**Sample Data Version**: 1.0
**Generated**: September 2024
**Last Updated**: October 2025
