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
    TRY_CAST(
        CASE
            WHEN bkpf.KURSF IS NULL OR TRIM(bkpf.KURSF) = '' THEN '1.00000'
            ELSE bkpf.KURSF
        END AS DECIMAL(9,5)
    ) AS exchange_rate,
    bkpf.USNAM AS user_name,
    bkpf.BKTXT AS document_header_text,
    bkpf.XBLNR AS reference_document,
    bkpf.TCODE AS transaction_code,

    -- Entry date
    TRY_CAST(
        CASE
            WHEN bkpf.CPUDT IS NULL OR TRIM(bkpf.CPUDT) = '' THEN NULL
            WHEN LENGTH(TRIM(bkpf.CPUDT)) = 8 THEN
                CONCAT(SUBSTRING(bkpf.CPUDT, 1, 4), '-',
                       SUBSTRING(bkpf.CPUDT, 5, 2), '-',
                       SUBSTRING(bkpf.CPUDT, 7, 2))
            ELSE bkpf.CPUDT
        END AS DATE
    ) AS entry_date,

    -- Status fields
    CASE WHEN TRIM(bkpf.BSTAT) = '' THEN NULL ELSE bkpf.BSTAT END AS document_status,
    CASE WHEN TRIM(bkpf.STBLG) = '' THEN NULL ELSE bkpf.STBLG END AS reversal_document,
    CASE WHEN TRIM(bkpf.STJAH) = '' THEN NULL ELSE bkpf.STJAH END AS reversal_fiscal_year,

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

    CASE WHEN TRIM(bseg.PSWSL) = '' THEN NULL ELSE bseg.PSWSL END AS document_currency_key,

    TRY_CAST(
        CASE
            WHEN bseg.MWSTS IS NULL OR TRIM(bseg.MWSTS) = '' THEN '0'
            ELSE REPLACE(REPLACE(bseg.MWSTS, ',', ''), ' ', '')
        END AS DECIMAL(15,2)
    ) AS tax_amount,

    CASE WHEN TRIM(bseg.KOSTL) = '' THEN NULL ELSE bseg.KOSTL END AS cost_center,
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
            WHEN bseg.ZBD1P IS NULL OR TRIM(bseg.ZBD1P) = '' THEN NULL
            ELSE bseg.ZBD1P
        END AS DECIMAL(5,3)
    ) AS cash_discount_percent_1,

    TRY_CAST(
        CASE
            WHEN bseg.ZBD2T IS NULL OR TRIM(bseg.ZBD2T) = '' THEN NULL
            ELSE bseg.ZBD2T
        END AS INT
    ) AS cash_discount_days_2,

    TRY_CAST(
        CASE
            WHEN bseg.ZBD3T IS NULL OR TRIM(bseg.ZBD3T) = '' THEN NULL
            ELSE bseg.ZBD3T
        END AS INT
    ) AS net_payment_terms_days,

    CASE WHEN TRIM(bseg.ZTERM) = '' THEN NULL ELSE bseg.ZTERM END AS payment_terms_code,

    TRY_CAST(
        CASE
            WHEN bseg.SKFBT IS NULL OR TRIM(bseg.SKFBT) = '' THEN '0'
            ELSE REPLACE(REPLACE(bseg.SKFBT, ',', ''), ' ', '')
        END AS DECIMAL(15,2)
    ) AS cash_discount_base_amount,

    -- Vendor Master Data (keep as text, clean only)
    CASE WHEN TRIM(lfa1.NAME1) = '' THEN NULL ELSE lfa1.NAME1 END AS vendor_name,
    CASE WHEN TRIM(lfa1.NAME2) = '' THEN NULL ELSE lfa1.NAME2 END AS vendor_name_2,
    CASE WHEN TRIM(lfa1.SORTL) = '' THEN NULL ELSE lfa1.SORTL END AS vendor_sort_field,
    CASE WHEN TRIM(lfa1.ORT01) = '' THEN NULL ELSE lfa1.ORT01 END AS vendor_city,
    CASE WHEN TRIM(lfa1.LAND1) = '' THEN NULL ELSE lfa1.LAND1 END AS vendor_country,
    CASE WHEN TRIM(lfa1.REGIO) = '' THEN NULL ELSE lfa1.REGIO END AS vendor_region,
    CASE WHEN TRIM(lfa1.PSTLZ) = '' THEN NULL ELSE lfa1.PSTLZ END AS vendor_postal_code,
    CASE WHEN TRIM(lfa1.STRAS) = '' THEN NULL ELSE lfa1.STRAS END AS vendor_street,
    CASE WHEN TRIM(lfa1.STCD1) = '' THEN NULL ELSE lfa1.STCD1 END AS vendor_tax_number_1,
    CASE WHEN TRIM(lfa1.STCD2) = '' THEN NULL ELSE lfa1.STCD2 END AS vendor_tax_number_2,
    CASE WHEN TRIM(lfa1.STCEG) = '' THEN NULL ELSE lfa1.STCEG END AS vendor_vat_number,
    CASE WHEN TRIM(lfa1.KTOKK) = '' THEN NULL ELSE lfa1.KTOKK END AS vendor_account_group,
    CASE WHEN TRIM(lfa1.BRSCH) = '' THEN NULL ELSE lfa1.BRSCH END AS vendor_industry,
    CASE WHEN TRIM(lfa1.LOEVM) = '' THEN NULL ELSE lfa1.LOEVM END AS vendor_deletion_flag,
    CASE WHEN TRIM(lfa1.SPERR) = '' THEN NULL ELSE lfa1.SPERR END AS vendor_posting_block,

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
    entry_date,
    currency,
    exchange_rate,
    user_name,
    document_header_text,
    reference_document,
    transaction_code,
    document_status,
    reversal_document,
    reversal_fiscal_year,

    -- Line Item Information
    debit_credit_indicator,
    account_type,
    vendor_number,
    gl_account,
    cost_center,
    amount_local_currency,
    amount_document_currency,
    document_currency_key,
    tax_amount,
    assignment_reference,
    line_item_text,

    -- Payment Terms
    baseline_payment_date,
    cash_discount_days_1,
    cash_discount_percent_1,
    cash_discount_days_2,
    net_payment_terms_days,
    payment_terms_code,
    cash_discount_base_amount,

    -- Vendor Master Data
    vendor_name,
    vendor_name_2,
    vendor_sort_field,
    vendor_city,
    vendor_country,
    vendor_region,
    vendor_postal_code,
    vendor_street,
    vendor_tax_number_1,
    vendor_tax_number_2,
    vendor_vat_number,
    vendor_account_group,
    vendor_industry,
    vendor_deletion_flag,
    vendor_posting_block,

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
        WHEN baseline_payment_date IS NOT NULL AND net_payment_terms_days IS NOT NULL
        THEN DATEADD(day, net_payment_terms_days, baseline_payment_date)
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

    -- Cash Discount Amount Calculation
    CASE
        WHEN cash_discount_percent_1 IS NOT NULL AND cash_discount_base_amount > 0
        THEN ROUND(cash_discount_base_amount * cash_discount_percent_1 / 100, 2)
        ELSE 0
    END AS calculated_discount_amount,

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
