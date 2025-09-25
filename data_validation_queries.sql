-- SAP Accounts Payable Data Validation Queries
-- These queries validate the relationships between BKPF, BSEG, and LFA1 tables

-- 1. Check if all BSEG records have matching BKPF headers
SELECT
    'Missing BKPF for BSEG' as validation_check,
    COUNT(*) as issue_count
FROM sap_bseg_line_items b
LEFT JOIN sap_bkpf_document_header h
    ON b.MANDT = h.MANDT
    AND b.BUKRS = h.BUKRS
    AND b.BELNR = h.BELNR
    AND b.GJAHR = h.GJAHR
WHERE h.BELNR IS NULL;

-- 2. Check if all vendor line items (KOART = 'K') have matching LFA1 records
SELECT
    'Missing LFA1 for vendor BSEG' as validation_check,
    COUNT(*) as issue_count
FROM sap_bseg_line_items b
LEFT JOIN sap_lfa1_vendor_master v
    ON b.MANDT = v.MANDT
    AND b.LIFNR = v.LIFNR
WHERE b.KOART = 'K' AND v.LIFNR IS NULL;

-- 3. Verify document balance (debit = credit for each document)
SELECT
    'Document balance check' as validation_check,
    COUNT(*) as unbalanced_documents
FROM (
    SELECT
        MANDT, BUKRS, BELNR, GJAHR,
        SUM(CASE WHEN SHKZG = 'S' THEN DMBTR ELSE -DMBTR END) as balance
    FROM sap_bseg_line_items
    GROUP BY MANDT, BUKRS, BELNR, GJAHR
    HAVING ABS(SUM(CASE WHEN SHKZG = 'S' THEN DMBTR ELSE -DMBTR END)) > 0.01
) unbalanced;

-- 4. Count records by table
SELECT 'LFA1 Vendor Records' as table_name, COUNT(*) as record_count FROM sap_lfa1_vendor_master
UNION ALL
SELECT 'BKPF Header Records' as table_name, COUNT(*) as record_count FROM sap_bkpf_document_header
UNION ALL
SELECT 'BSEG Line Items' as table_name, COUNT(*) as record_count FROM sap_bseg_line_items;

-- 5. Sample join query to demonstrate relationships
SELECT
    h.BELNR as document_number,
    h.BLDAT as document_date,
    h.BKTXT as header_text,
    b.BUZEI as line_item,
    b.SHKZG as debit_credit,
    b.DMBTR as amount,
    v.NAME1 as vendor_name,
    v.ORT01 as vendor_city
FROM sap_bkpf_document_header h
JOIN sap_bseg_line_items b
    ON h.MANDT = b.MANDT
    AND h.BUKRS = b.BUKRS
    AND h.BELNR = b.BELNR
    AND h.GJAHR = b.GJAHR
LEFT JOIN sap_lfa1_vendor_master v
    ON b.MANDT = v.MANDT
    AND b.LIFNR = v.LIFNR
WHERE b.KOART = 'K'  -- Vendor line items only
ORDER BY h.BLDAT, h.BELNR, b.BUZEI
LIMIT 10;

-- 6. Monthly AP summary
SELECT
    SUBSTR(h.BLDAT, 1, 6) as year_month,
    COUNT(DISTINCT h.BELNR) as invoice_count,
    SUM(CASE WHEN b.SHKZG = 'H' AND b.KOART = 'K' THEN b.DMBTR ELSE 0 END) as total_payable_amount,
    COUNT(DISTINCT b.LIFNR) as unique_vendors
FROM sap_bkpf_document_header h
JOIN sap_bseg_line_items b
    ON h.MANDT = b.MANDT
    AND h.BUKRS = b.BUKRS
    AND h.BELNR = b.BELNR
    AND h.GJAHR = b.GJAHR
WHERE h.BLART = 'RE'  -- Invoice documents only
GROUP BY SUBSTR(h.BLDAT, 1, 6)
ORDER BY year_month;