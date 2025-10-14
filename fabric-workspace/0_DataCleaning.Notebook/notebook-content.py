# Fabric notebook source

# METADATA ********************

# META {
# META   "kernel_info": {
# META     "name": "synapse_pyspark"
# META   },
# META   "dependencies": {
# META     "lakehouse": {
# META       "default_lakehouse": "f245663a-76de-4021-a6dd-6a806d27f57b",
# META       "default_lakehouse_name": "SapDataLakehouse",
# META       "default_lakehouse_workspace_id": "4401777b-4041-493e-81bc-efb3c0cc5c44",
# META       "known_lakehouses": [
# META         {
# META           "id": "f245663a-76de-4021-a6dd-6a806d27f57b"
# META         }
# META       ]
# META     }
# META   }
# META }

# CELL ********************

# MAGIC %%sql
# MAGIC -- =====================================================
# MAGIC -- Accounts Payable Fact Table Transformation
# MAGIC -- TWO-STAGE APPROACH
# MAGIC -- =====================================================
# MAGIC -- Stage 1: Data Type Casting (Staging Table)
# MAGIC -- Stage 2: Business Logic Transformation (Final Fact Table)
# MAGIC -- =====================================================
# MAGIC 
# MAGIC -- =====================================================
# MAGIC -- STAGE 1: Data Type Casting Layer
# MAGIC -- =====================================================
# MAGIC -- Purpose: Cast all string columns to proper data types
# MAGIC -- Handles various date formats and null/empty values
# MAGIC -- =====================================================
# MAGIC 
# MAGIC CREATE OR REPLACE TABLE accounts_payable_staging AS
# MAGIC SELECT
# MAGIC     -- Document Keys (Text to keep leading zeros)
# MAGIC     bseg.MANDT AS mandt,
# MAGIC     bseg.BUKRS AS company_code,
# MAGIC     bseg.BELNR AS document_number,
# MAGIC     TRY_CAST(bseg.GJAHR AS INT) AS fiscal_year,
# MAGIC     bseg.BUZEI AS line_item_number,
# MAGIC 
# MAGIC     -- Document Header Information
# MAGIC     bkpf.BLART AS document_type_code,
# MAGIC 
# MAGIC     -- Dates: Use TRY_CAST with multiple fallback formats
# MAGIC     TRY_CAST(
# MAGIC         CASE
# MAGIC             WHEN bkpf.BLDAT IS NULL OR TRIM(bkpf.BLDAT) = '' THEN NULL
# MAGIC             WHEN LENGTH(TRIM(bkpf.BLDAT)) = 8 THEN
# MAGIC                 CONCAT(SUBSTRING(bkpf.BLDAT, 1, 4), '-',
# MAGIC                        SUBSTRING(bkpf.BLDAT, 5, 2), '-',
# MAGIC                        SUBSTRING(bkpf.BLDAT, 7, 2))
# MAGIC             ELSE bkpf.BLDAT
# MAGIC         END AS DATE
# MAGIC     ) AS document_date,
# MAGIC 
# MAGIC     TRY_CAST(
# MAGIC         CASE
# MAGIC             WHEN bkpf.BUDAT IS NULL OR TRIM(bkpf.BUDAT) = '' THEN NULL
# MAGIC             WHEN LENGTH(TRIM(bkpf.BUDAT)) = 8 THEN
# MAGIC                 CONCAT(SUBSTRING(bkpf.BUDAT, 1, 4), '-',
# MAGIC                        SUBSTRING(bkpf.BUDAT, 5, 2), '-',
# MAGIC                        SUBSTRING(bkpf.BUDAT, 7, 2))
# MAGIC             ELSE bkpf.BUDAT
# MAGIC         END AS DATE
# MAGIC     ) AS posting_date,
# MAGIC 
# MAGIC     -- Text fields
# MAGIC     bkpf.WAERS AS currency,
# MAGIC     bkpf.USNAM AS user_name,
# MAGIC     bkpf.BKTXT AS document_header_text,
# MAGIC     bkpf.XBLNR AS reference_document,
# MAGIC     bkpf.TCODE AS transaction_code,
# MAGIC 
# MAGIC     -- Line Item Information
# MAGIC     bseg.SHKZG AS debit_credit_indicator,
# MAGIC     bseg.KOART AS account_type,
# MAGIC     CASE WHEN TRIM(bseg.LIFNR) = '' THEN NULL ELSE bseg.LIFNR END AS vendor_number,
# MAGIC     bseg.HKONT AS gl_account,
# MAGIC 
# MAGIC     -- Amounts: Handle various decimal formats
# MAGIC     TRY_CAST(
# MAGIC         CASE
# MAGIC             WHEN bseg.DMBTR IS NULL OR TRIM(bseg.DMBTR) = '' THEN '0'
# MAGIC             ELSE REPLACE(REPLACE(bseg.DMBTR, ',', ''), ' ', '')
# MAGIC         END AS DECIMAL(15,2)
# MAGIC     ) AS amount_local_currency,
# MAGIC 
# MAGIC     TRY_CAST(
# MAGIC         CASE
# MAGIC             WHEN bseg.WRBTR IS NULL OR TRIM(bseg.WRBTR) = '' THEN '0'
# MAGIC             ELSE REPLACE(REPLACE(bseg.WRBTR, ',', ''), ' ', '')
# MAGIC         END AS DECIMAL(15,2)
# MAGIC     ) AS amount_document_currency,
# MAGIC 
# MAGIC     TRY_CAST(
# MAGIC         CASE
# MAGIC             WHEN bseg.MWSTS IS NULL OR TRIM(bseg.MWSTS) = '' THEN '0'
# MAGIC             ELSE REPLACE(REPLACE(bseg.MWSTS, ',', ''), ' ', '')
# MAGIC         END AS DECIMAL(15,2)
# MAGIC     ) AS tax_amount,
# MAGIC 
# MAGIC     bseg.ZUONR AS assignment_reference,
# MAGIC     bseg.SGTXT AS line_item_text,
# MAGIC 
# MAGIC     -- Payment Terms
# MAGIC     TRY_CAST(
# MAGIC         CASE
# MAGIC             WHEN bseg.ZFBDT IS NULL OR TRIM(bseg.ZFBDT) = '' THEN NULL
# MAGIC             WHEN LENGTH(TRIM(bseg.ZFBDT)) = 8 THEN
# MAGIC                 CONCAT(SUBSTRING(bseg.ZFBDT, 1, 4), '-',
# MAGIC                        SUBSTRING(bseg.ZFBDT, 5, 2), '-',
# MAGIC                        SUBSTRING(bseg.ZFBDT, 7, 2))
# MAGIC             ELSE bseg.ZFBDT
# MAGIC         END AS DATE
# MAGIC     ) AS baseline_payment_date,
# MAGIC 
# MAGIC     TRY_CAST(
# MAGIC         CASE
# MAGIC             WHEN bseg.ZBD1T IS NULL OR TRIM(bseg.ZBD1T) = '' THEN NULL
# MAGIC             ELSE bseg.ZBD1T
# MAGIC         END AS INT
# MAGIC     ) AS cash_discount_days_1,
# MAGIC 
# MAGIC     TRY_CAST(
# MAGIC         CASE
# MAGIC             WHEN bseg.ZBD2T IS NULL OR TRIM(bseg.ZBD2T) = '' THEN NULL
# MAGIC             ELSE bseg.ZBD2T
# MAGIC         END AS INT
# MAGIC     ) AS cash_discount_days_2,
# MAGIC 
# MAGIC     CASE WHEN TRIM(bseg.ZTERM) = '' THEN NULL ELSE bseg.ZTERM END AS payment_terms,
# MAGIC 
# MAGIC     TRY_CAST(
# MAGIC         CASE
# MAGIC             WHEN bseg.SKFBT IS NULL OR TRIM(bseg.SKFBT) = '' THEN '0'
# MAGIC             ELSE REPLACE(REPLACE(bseg.SKFBT, ',', ''), ' ', '')
# MAGIC         END AS DECIMAL(15,2)
# MAGIC     ) AS cash_discount_amount,
# MAGIC 
# MAGIC     -- Vendor Master Data (keep as text, clean only)
# MAGIC     CASE WHEN TRIM(lfa1.NAME1) = '' THEN NULL ELSE lfa1.NAME1 END AS vendor_name,
# MAGIC     CASE WHEN TRIM(lfa1.NAME2) = '' THEN NULL ELSE lfa1.NAME2 END AS vendor_name_2,
# MAGIC     CASE WHEN TRIM(lfa1.ORT01) = '' THEN NULL ELSE lfa1.ORT01 END AS vendor_city,
# MAGIC     CASE WHEN TRIM(lfa1.LAND1) = '' THEN NULL ELSE lfa1.LAND1 END AS vendor_country,
# MAGIC     CASE WHEN TRIM(lfa1.PSTLZ) = '' THEN NULL ELSE lfa1.PSTLZ END AS vendor_postal_code,
# MAGIC     CASE WHEN TRIM(lfa1.STRAS) = '' THEN NULL ELSE lfa1.STRAS END AS vendor_street,
# MAGIC     CASE WHEN TRIM(lfa1.STCD1) = '' THEN NULL ELSE lfa1.STCD1 END AS vendor_tax_number_1,
# MAGIC     CASE WHEN TRIM(lfa1.STCEG) = '' THEN NULL ELSE lfa1.STCEG END AS vendor_vat_number,
# MAGIC     CASE WHEN TRIM(lfa1.KTOKK) = '' THEN NULL ELSE lfa1.KTOKK END AS vendor_account_group,
# MAGIC 
# MAGIC     -- Quality check flag
# MAGIC     CASE WHEN lfa1.LIFNR IS NULL THEN 1 ELSE 0 END AS is_vendor_not_in_master
# MAGIC 
# MAGIC FROM
# MAGIC     bseg
# MAGIC 
# MAGIC INNER JOIN bkpf
# MAGIC     ON bseg.MANDT = bkpf.MANDT
# MAGIC     AND bseg.BUKRS = bkpf.BUKRS
# MAGIC     AND bseg.BELNR = bkpf.BELNR
# MAGIC     AND bseg.GJAHR = bkpf.GJAHR
# MAGIC 
# MAGIC LEFT JOIN lfa1
# MAGIC     ON bseg.MANDT = lfa1.MANDT
# MAGIC     AND bseg.LIFNR = lfa1.LIFNR
# MAGIC 
# MAGIC WHERE
# MAGIC     bseg.KOART IN ('K', 'S');  -- K = Vendor, S = G/L Account

# METADATA ********************

# META {
# META   "language": "sparksql",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# MAGIC %%sql
# MAGIC -- =====================================================
# MAGIC -- STAGE 2: Business Logic Transformation Layer
# MAGIC -- =====================================================
# MAGIC -- Purpose: Apply business rules and calculations
# MAGIC -- Input: Clean, typed data from staging table
# MAGIC -- Output: Final fact table ready for Power BI
# MAGIC -- =====================================================
# MAGIC 
# MAGIC CREATE OR REPLACE TABLE accounts_payable_fact AS
# MAGIC SELECT
# MAGIC     -- Document Keys
# MAGIC     mandt AS MANDT,
# MAGIC     company_code,
# MAGIC     document_number,
# MAGIC     fiscal_year,
# MAGIC     line_item_number,
# MAGIC 
# MAGIC     -- Document Header Information
# MAGIC     document_type_code AS document_type,
# MAGIC     document_date,
# MAGIC     posting_date,
# MAGIC     currency,
# MAGIC     user_name,
# MAGIC     document_header_text,
# MAGIC     reference_document,
# MAGIC     transaction_code,
# MAGIC 
# MAGIC     -- Line Item Information
# MAGIC     debit_credit_indicator,
# MAGIC     account_type,
# MAGIC     vendor_number,
# MAGIC     gl_account,
# MAGIC     amount_local_currency,
# MAGIC     amount_document_currency,
# MAGIC     tax_amount,
# MAGIC     assignment_reference,
# MAGIC     line_item_text,
# MAGIC 
# MAGIC     -- Payment Terms
# MAGIC     baseline_payment_date,
# MAGIC     cash_discount_days_1,
# MAGIC     cash_discount_days_2,
# MAGIC     payment_terms,
# MAGIC     cash_discount_amount,
# MAGIC 
# MAGIC     -- Vendor Master Data
# MAGIC     vendor_name,
# MAGIC     vendor_name_2,
# MAGIC     vendor_city,
# MAGIC     vendor_country,
# MAGIC     vendor_postal_code,
# MAGIC     vendor_street,
# MAGIC     vendor_tax_number_1,
# MAGIC     vendor_vat_number,
# MAGIC     vendor_account_group,
# MAGIC 
# MAGIC     -- Calculated Fields
# MAGIC     CASE
# MAGIC         WHEN debit_credit_indicator = 'S' THEN amount_local_currency
# MAGIC         WHEN debit_credit_indicator = 'H' THEN -amount_local_currency
# MAGIC         ELSE 0
# MAGIC     END AS signed_amount,
# MAGIC 
# MAGIC     CASE
# MAGIC         WHEN account_type = 'K' THEN amount_local_currency
# MAGIC         ELSE 0
# MAGIC     END AS vendor_liability_amount,
# MAGIC 
# MAGIC     -- Document Classification
# MAGIC     CASE
# MAGIC         WHEN document_type_code = 'RE' THEN 'Invoice'
# MAGIC         WHEN document_type_code = 'KZ' THEN 'Payment'
# MAGIC         WHEN document_type_code = 'KG' THEN 'Credit Memo'
# MAGIC         ELSE 'Other'
# MAGIC     END AS document_type_description,
# MAGIC 
# MAGIC     -- Due Date Calculation
# MAGIC     CASE
# MAGIC         WHEN baseline_payment_date IS NOT NULL AND cash_discount_days_1 IS NOT NULL
# MAGIC         THEN DATEADD(day, cash_discount_days_1, baseline_payment_date)
# MAGIC         ELSE NULL
# MAGIC     END AS net_due_date,
# MAGIC 
# MAGIC     -- Cash Discount Due Date
# MAGIC     CASE
# MAGIC         WHEN baseline_payment_date IS NOT NULL AND cash_discount_days_1 IS NOT NULL
# MAGIC         THEN DATEADD(day, cash_discount_days_1, baseline_payment_date)
# MAGIC         ELSE NULL
# MAGIC     END AS cash_discount_due_date,
# MAGIC 
# MAGIC     -- Data Quality Flags
# MAGIC     CASE WHEN vendor_number IS NULL THEN 1 ELSE 0 END AS is_missing_vendor,
# MAGIC     CASE WHEN amount_local_currency = 0 THEN 1 ELSE 0 END AS is_zero_amount,
# MAGIC     is_vendor_not_in_master,
# MAGIC 
# MAGIC     -- Metadata
# MAGIC     CURRENT_TIMESTAMP() AS etl_load_timestamp
# MAGIC 
# MAGIC FROM accounts_payable_staging;
# MAGIC 
# MAGIC 
# MAGIC -- =====================================================
# MAGIC -- Data Quality Summary View
# MAGIC -- =====================================================
# MAGIC CREATE OR REPLACE VIEW ap_data_quality_summary AS
# MAGIC SELECT
# MAGIC     COUNT(*) AS total_line_items,
# MAGIC     SUM(is_missing_vendor) AS missing_vendor_count,
# MAGIC     SUM(is_zero_amount) AS zero_amount_count,
# MAGIC     SUM(is_vendor_not_in_master) AS vendor_not_in_master_count,
# MAGIC     COUNT(DISTINCT vendor_number) AS unique_vendors,
# MAGIC     COUNT(DISTINCT document_number) AS unique_documents,
# MAGIC     SUM(CASE WHEN document_type = 'RE' THEN 1 ELSE 0 END) AS invoice_count,
# MAGIC     SUM(CASE WHEN document_type = 'KZ' THEN 1 ELSE 0 END) AS payment_count,
# MAGIC     MIN(posting_date) AS earliest_posting_date,
# MAGIC     MAX(posting_date) AS latest_posting_date,
# MAGIC     SUM(signed_amount) AS net_vendor_liability
# MAGIC FROM accounts_payable_fact;
# MAGIC 
# MAGIC -- =====================================================
# MAGIC -- Vendor Summary View
# MAGIC -- =====================================================
# MAGIC CREATE OR REPLACE VIEW ap_vendor_summary AS
# MAGIC SELECT
# MAGIC     vendor_number,
# MAGIC     vendor_name,
# MAGIC     vendor_city,
# MAGIC     vendor_country,
# MAGIC     COUNT(DISTINCT document_number) AS document_count,
# MAGIC     SUM(CASE WHEN document_type = 'RE' THEN vendor_liability_amount ELSE 0 END) AS total_invoices,
# MAGIC     SUM(CASE WHEN document_type = 'KZ' THEN vendor_liability_amount ELSE 0 END) AS total_payments,
# MAGIC     SUM(vendor_liability_amount) AS net_open_amount
# MAGIC FROM accounts_payable_fact
# MAGIC WHERE vendor_number IS NOT NULL
# MAGIC GROUP BY
# MAGIC     vendor_number,
# MAGIC     vendor_name,
# MAGIC     vendor_city,
# MAGIC     vendor_country;
# MAGIC 
# MAGIC -- =====================================================
# MAGIC -- Usage Instructions
# MAGIC -- =====================================================
# MAGIC -- 1. Run this entire script in your Lakehouse SQL endpoint
# MAGIC -- 2. Stage 1 creates: accounts_payable_staging (typed data)
# MAGIC -- 3. Stage 2 creates: accounts_payable_fact (business logic)
# MAGIC -- 4. Verify: SELECT * FROM ap_data_quality_summary;
# MAGIC -- 5. Publish 'accounts_payable_fact' to your semantic model
# MAGIC -- =====================================================


# METADATA ********************

# META {
# META   "language": "sparksql",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# MAGIC %%sql
# MAGIC SELECT * FROM ap_data_quality_summary

# METADATA ********************

# META {
# META   "language": "sparksql",
# META   "language_group": "synapse_pyspark"
# META }
