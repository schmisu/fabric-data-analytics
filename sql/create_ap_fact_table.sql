%%sql
-- =====================================================
-- Accounts Payable Fact Table Transformation
-- TWO-STAGE APPROACH
-- =====================================================
-- Stage 1: Data Type Casting (Staging Table)
-- Stage 2: Business Logic Transformation (Final Fact Table)
-- =====================================================

-- =====================================================
-- STAGE 1: Data Type Casting Layer
-- =====================================================
-- Purpose: Cast all string columns to proper data types
-- Handles various date formats and null/empty values
-- =====================================================

CREATE OR REPLACE TABLE accounts_payable_staging AS
SELECT
    -- Document Keys (Text to keep leading zeros)
    bseg.MANDT AS mandt,
    bseg.BUKRS AS company_code,
    bseg.BELNR AS document_number,
    TRY_CAST(bseg.GJAHR AS INT) AS fiscal_year,
    bseg.BUZEI AS line_item_number,

    -- Document Header Information
    bkpf.BLART AS document_type_code,

    -- Dates: Use TRY_CAST with multiple fallback formats
    TRY_CAST(
        CASE
            WHEN bkpf.BLDAT IS NULL OR TRIM(bkpf.BLDAT) = '' THEN NULL
            WHEN LENGTH(TRIM(bkpf.BLDAT)) = 8 THEN
                CONCAT(SUBSTRING(bkpf.BLDAT, 1, 4), '-',
                       SUBSTRING(bkpf.BLDAT, 5, 2), '-',
                       SUBSTRING(bkpf.BLDAT, 7, 2))
            ELSE bkpf.BLDAT
        END AS DATE
    ) AS document_date,

    TRY_CAST(
        CASE
            WHEN bkpf.BUDAT IS NULL OR TRIM(bkpf.BUDAT) = '' THEN NULL
            WHEN LENGTH(TRIM(bkpf.BUDAT)) = 8 THEN
                CONCAT(SUBSTRING(bkpf.BUDAT, 1, 4), '-',
                       SUBSTRING(bkpf.BUDAT, 5, 2), '-',
                       SUBSTRING(bkpf.BUDAT, 7, 2))
            ELSE bkpf.BUDAT
        END AS DATE
    ) AS posting_date,

    -- Text fields
    bkpf.WAERS AS currency,
    bkpf.USNAM AS user_name,
    bkpf.BKTXT AS document_header_text,
    bkpf.XBLNR AS reference_document,
    bkpf.TCODE AS transaction_code,

    -- Line Item Information
    bseg.SHKZG AS debit_credit_indicator,
    bseg.KOART AS account_type,
    CASE WHEN TRIM(bseg.LIFNR) = '' THEN NULL ELSE bseg.LIFNR END AS vendor_number,
    bseg.HKONT AS gl_account,

    -- Amounts: Handle various decimal formats
    TRY_CAST(
        CASE
            WHEN bseg.DMBTR IS NULL OR TRIM(bseg.DMBTR) = '' THEN '0'
            ELSE REPLACE(REPLACE(bseg.DMBTR, ',', ''), ' ', '')
        END AS DECIMAL(15,2)
    ) AS amount_local_currency,

    TRY_CAST(
        CASE
            WHEN bseg.WRBTR IS NULL OR TRIM(bseg.WRBTR) = '' THEN '0'
            ELSE REPLACE(REPLACE(bseg.WRBTR, ',', ''), ' ', '')
        END AS DECIMAL(15,2)
    ) AS amount_document_currency,

    TRY_CAST(
        CASE
            WHEN bseg.MWSTS IS NULL OR TRIM(bseg.MWSTS) = '' THEN '0'
            ELSE REPLACE(REPLACE(bseg.MWSTS, ',', ''), ' ', '')
        END AS DECIMAL(15,2)
    ) AS tax_amount,

    bseg.ZUONR AS assignment_reference,
    bseg.SGTXT AS line_item_text,

    -- Payment Terms
    TRY_CAST(
        CASE
            WHEN bseg.ZFBDT IS NULL OR TRIM(bseg.ZFBDT) = '' THEN NULL
            WHEN LENGTH(TRIM(bseg.ZFBDT)) = 8 THEN
                CONCAT(SUBSTRING(bseg.ZFBDT, 1, 4), '-',
                       SUBSTRING(bseg.ZFBDT, 5, 2), '-',
                       SUBSTRING(bseg.ZFBDT, 7, 2))
            ELSE bseg.ZFBDT
        END AS DATE
    ) AS baseline_payment_date,

    TRY_CAST(
        CASE
            WHEN bseg.ZBD1T IS NULL OR TRIM(bseg.ZBD1T) = '' THEN NULL
            ELSE bseg.ZBD1T
        END AS INT
    ) AS cash_discount_days_1,

    TRY_CAST(
        CASE
            WHEN bseg.ZBD2T IS NULL OR TRIM(bseg.ZBD2T) = '' THEN NULL
            ELSE bseg.ZBD2T
        END AS INT
    ) AS cash_discount_days_2,

    CASE WHEN TRIM(bseg.ZTERM) = '' THEN NULL ELSE bseg.ZTERM END AS payment_terms,

    TRY_CAST(
        CASE
            WHEN bseg.SKFBT IS NULL OR TRIM(bseg.SKFBT) = '' THEN '0'
            ELSE REPLACE(REPLACE(bseg.SKFBT, ',', ''), ' ', '')
        END AS DECIMAL(15,2)
    ) AS cash_discount_amount,

    -- Vendor Master Data (keep as text, clean only)
    CASE WHEN TRIM(lfa1.NAME1) = '' THEN NULL ELSE lfa1.NAME1 END AS vendor_name,
    CASE WHEN TRIM(lfa1.NAME2) = '' THEN NULL ELSE lfa1.NAME2 END AS vendor_name_2,
    CASE WHEN TRIM(lfa1.ORT01) = '' THEN NULL ELSE lfa1.ORT01 END AS vendor_city,
    CASE WHEN TRIM(lfa1.LAND1) = '' THEN NULL ELSE lfa1.LAND1 END AS vendor_country,
    CASE WHEN TRIM(lfa1.PSTLZ) = '' THEN NULL ELSE lfa1.PSTLZ END AS vendor_postal_code,
    CASE WHEN TRIM(lfa1.STRAS) = '' THEN NULL ELSE lfa1.STRAS END AS vendor_street,
    CASE WHEN TRIM(lfa1.STCD1) = '' THEN NULL ELSE lfa1.STCD1 END AS vendor_tax_number_1,
    CASE WHEN TRIM(lfa1.STCEG) = '' THEN NULL ELSE lfa1.STCEG END AS vendor_vat_number,
    CASE WHEN TRIM(lfa1.KTOKK) = '' THEN NULL ELSE lfa1.KTOKK END AS vendor_account_group,

    -- Quality check flag
    CASE WHEN lfa1.LIFNR IS NULL THEN 1 ELSE 0 END AS is_vendor_not_in_master

FROM
    bseg

INNER JOIN bkpf
    ON bseg.MANDT = bkpf.MANDT
    AND bseg.BUKRS = bkpf.BUKRS
    AND bseg.BELNR = bkpf.BELNR
    AND bseg.GJAHR = bkpf.GJAHR

LEFT JOIN lfa1
    ON bseg.MANDT = lfa1.MANDT
    AND bseg.LIFNR = lfa1.LIFNR

WHERE
    bseg.KOART IN ('K', 'S');  -- K = Vendor, S = G/L Account


-- =====================================================
-- STAGE 2: Business Logic Transformation Layer
-- =====================================================
-- Purpose: Apply business rules and calculations
-- Input: Clean, typed data from staging table
-- Output: Final fact table ready for Power BI
-- =====================================================

CREATE OR REPLACE TABLE accounts_payable_fact AS
SELECT
    -- Document Keys
    mandt AS MANDT,
    company_code,
    document_number,
    fiscal_year,
    line_item_number,

    -- Document Header Information
    document_type_code AS document_type,
    document_date,
    posting_date,
    currency,
    user_name,
    document_header_text,
    reference_document,
    transaction_code,

    -- Line Item Information
    debit_credit_indicator,
    account_type,
    vendor_number,
    gl_account,
    amount_local_currency,
    amount_document_currency,
    tax_amount,
    assignment_reference,
    line_item_text,

    -- Payment Terms
    baseline_payment_date,
    cash_discount_days_1,
    cash_discount_days_2,
    payment_terms,
    cash_discount_amount,

    -- Vendor Master Data
    vendor_name,
    vendor_name_2,
    vendor_city,
    vendor_country,
    vendor_postal_code,
    vendor_street,
    vendor_tax_number_1,
    vendor_vat_number,
    vendor_account_group,

    -- Calculated Fields
    CASE
        WHEN debit_credit_indicator = 'S' THEN amount_local_currency
        WHEN debit_credit_indicator = 'H' THEN -amount_local_currency
        ELSE 0
    END AS signed_amount,

    CASE
        WHEN account_type = 'K' THEN amount_local_currency
        ELSE 0
    END AS vendor_liability_amount,

    -- Document Classification
    CASE
        WHEN document_type_code = 'RE' THEN 'Invoice'
        WHEN document_type_code = 'KZ' THEN 'Payment'
        WHEN document_type_code = 'KG' THEN 'Credit Memo'
        ELSE 'Other'
    END AS document_type_description,

    -- Due Date Calculation
    CASE
        WHEN baseline_payment_date IS NOT NULL AND cash_discount_days_1 IS NOT NULL
        THEN DATEADD(day, cash_discount_days_1, baseline_payment_date)
        ELSE NULL
    END AS net_due_date,

    -- Cash Discount Due Date
    CASE
        WHEN baseline_payment_date IS NOT NULL AND cash_discount_days_1 IS NOT NULL
        THEN DATEADD(day, cash_discount_days_1, baseline_payment_date)
        ELSE NULL
    END AS cash_discount_due_date,

    -- Data Quality Flags
    CASE WHEN vendor_number IS NULL THEN 1 ELSE 0 END AS is_missing_vendor,
    CASE WHEN amount_local_currency = 0 THEN 1 ELSE 0 END AS is_zero_amount,
    is_vendor_not_in_master,

    -- Metadata
    CURRENT_TIMESTAMP() AS etl_load_timestamp

FROM accounts_payable_staging;


-- =====================================================
-- Data Quality Summary View
-- =====================================================
CREATE OR REPLACE VIEW ap_data_quality_summary AS
SELECT
    COUNT(*) AS total_line_items,
    SUM(is_missing_vendor) AS missing_vendor_count,
    SUM(is_zero_amount) AS zero_amount_count,
    SUM(is_vendor_not_in_master) AS vendor_not_in_master_count,
    COUNT(DISTINCT vendor_number) AS unique_vendors,
    COUNT(DISTINCT document_number) AS unique_documents,
    SUM(CASE WHEN document_type = 'RE' THEN 1 ELSE 0 END) AS invoice_count,
    SUM(CASE WHEN document_type = 'KZ' THEN 1 ELSE 0 END) AS payment_count,
    MIN(posting_date) AS earliest_posting_date,
    MAX(posting_date) AS latest_posting_date,
    SUM(signed_amount) AS net_vendor_liability
FROM accounts_payable_fact;

-- =====================================================
-- Vendor Summary View
-- =====================================================
CREATE OR REPLACE VIEW ap_vendor_summary AS
SELECT
    vendor_number,
    vendor_name,
    vendor_city,
    vendor_country,
    COUNT(DISTINCT document_number) AS document_count,
    SUM(CASE WHEN document_type = 'RE' THEN vendor_liability_amount ELSE 0 END) AS total_invoices,
    SUM(CASE WHEN document_type = 'KZ' THEN vendor_liability_amount ELSE 0 END) AS total_payments,
    SUM(vendor_liability_amount) AS net_open_amount
FROM accounts_payable_fact
WHERE vendor_number IS NOT NULL
GROUP BY
    vendor_number,
    vendor_name,
    vendor_city,
    vendor_country;

-- =====================================================
-- Usage Instructions
-- =====================================================
-- 1. Run this entire script in your Lakehouse SQL endpoint
-- 2. Stage 1 creates: accounts_payable_staging (typed data)
-- 3. Stage 2 creates: accounts_payable_fact (business logic)
-- 4. Verify: SELECT * FROM ap_data_quality_summary;
-- 5. Publish 'accounts_payable_fact' to your semantic model
-- =====================================================
