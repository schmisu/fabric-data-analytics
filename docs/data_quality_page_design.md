# Power BI Report Design - Data Quality Overview Page

## Purpose
Pre-flight check page to validate data completeness and identify issues before analysis. This page should be **Page 1** (before Executive Dashboard) to ensure data quality is verified first.

---

## Page Layout: Data Quality Overview

### Section 1: Overall Health Score (Top)

**Visual 1: Data Quality Score Card**
- Type: Card
- Measure: `[Data Quality Score]`
- Format: Percentage
- Conditional formatting:
  - Green: > 95%
  - Yellow: 90-95%
  - Red: < 90%

**Visual 2: Total Records Card**
- Type: Card
- Field: `COUNT(accounts_payable_fact[document_number])`
- Label: "Total Line Items"

**Visual 3: Date Range Card**
- Type: Multi-row card
- Fields:
  - `MIN(accounts_payable_fact[posting_date])` → "Earliest Date"
  - `MAX(accounts_payable_fact[posting_date])` → "Latest Date"

---

### Section 2: Critical Data Issues (Middle)

**Visual 4: Data Quality Issues Table**
- Type: Table
- Columns:
  - Issue Type (manual text)
  - Count (measure)
  - % of Total (measure)
  - Status (visual indicator)

**Manual rows to create:**
```
Issue Type                    | Count Measure                  | % of Total
------------------------------|--------------------------------|------------------
Missing Vendor                | [Missing Vendor Count]         | [Missing Vendor %]
Zero Amount Invoices          | [Zero Amount Count]            | [Zero Amount %]
Vendor Not in Master          | [Vendor Not in Master Count]   | [Vendor Not in Master %]
Missing Posting Date          | [Missing Posting Date Count]   | [Missing Posting Date %]
Missing Document Type         | [Missing Document Type Count]  | [Missing Document Type %]
Invalid Payment Terms         | [Invalid Payment Terms Count]  | [Invalid Payment Terms %]
```

**Visual 5: Issue Severity Gauge**
- Type: Gauge
- Measure: `[Critical Issues %]`
- Min: 0%
- Max: 20%
- Target: 5%
- Color zones:
  - 0-5%: Green (Good)
  - 5-10%: Yellow (Warning)
  - 10-20%: Red (Critical)

---

### Section 3: Field Completeness (Middle-Right)

**Visual 6: Field Completeness Matrix**
- Type: Matrix or Clustered Bar Chart
- Y-axis: Field names (manual list)
- X-axis: `[Field Completeness %]`

**Fields to check:**
- posting_date
- document_date
- vendor_number
- amount_local_currency
- baseline_payment_date
- payment_terms
- vendor_name

**Visual 7: Completeness Heatmap (optional)**
- Type: Matrix
- Rows: Month (posting_date)
- Columns: Field names
- Values: Completeness %
- Conditional formatting: Green (100%) to Red (< 80%)

---

### Section 4: Data Distribution (Bottom)

**Visual 8: Record Count by Month**
- Type: Column Chart
- X-axis: `posting_date` (Month)
- Y-axis: `COUNT(accounts_payable_fact[document_number])`
- Purpose: Identify gaps or anomalies in data load

**Visual 9: Document Type Distribution**
- Type: Donut Chart
- Legend: `document_type_description`
- Values: `COUNT(accounts_payable_fact[document_number])`
- Purpose: Ensure mix of Invoices, Payments, etc.

**Visual 10: Vendor Coverage**
- Type: Card
- Measure: `[Vendor Coverage Rate]`
- Format: Percentage
- Definition: % of line items with valid vendor match

---

### Section 5: Actionable Recommendations (Bottom)

**Visual 11: Issues to Fix Table**
- Type: Table with drill-down
- Columns:
  - Priority (High/Medium/Low)
  - Issue Description
  - Affected Records
  - Recommended Action

**Example rows:**
| Priority | Issue | Affected Records | Recommended Action |
|----------|-------|------------------|-------------------|
| High | Missing vendor numbers | [Missing Vendor Count] | Review and populate LIFNR in BSEG |
| High | Vendor not in master | [Vendor Not in Master Count] | Add vendors to LFA1 table |
| Medium | Zero amount invoices | [Zero Amount Count] | Verify if legitimate or data error |
| Low | Missing payment terms | [Invalid Payment Terms Count] | Populate ZTERM in BSEG |

---

## Required DAX Measures for Data Quality Page

### Basic Quality Metrics

```dax
Missing Vendor Count =
CALCULATE(
    COUNTROWS(accounts_payable_fact),
    accounts_payable_fact[is_missing_vendor] = 1
)

Missing Vendor % =
DIVIDE([Missing Vendor Count], COUNTROWS(accounts_payable_fact), 0)

Zero Amount Count =
CALCULATE(
    COUNTROWS(accounts_payable_fact),
    accounts_payable_fact[is_zero_amount] = 1
)

Zero Amount % =
DIVIDE([Zero Amount Count], COUNTROWS(accounts_payable_fact), 0)

Vendor Not in Master Count =
CALCULATE(
    COUNTROWS(accounts_payable_fact),
    accounts_payable_fact[is_vendor_not_in_master] = 1
)

Vendor Not in Master % =
DIVIDE([Vendor Not in Master Count], COUNTROWS(accounts_payable_fact), 0)

Missing Posting Date Count =
CALCULATE(
    COUNTROWS(accounts_payable_fact),
    ISBLANK(accounts_payable_fact[posting_date])
)

Missing Posting Date % =
DIVIDE([Missing Posting Date Count], COUNTROWS(accounts_payable_fact), 0)

Missing Document Type Count =
CALCULATE(
    COUNTROWS(accounts_payable_fact),
    ISBLANK(accounts_payable_fact[document_type])
)

Missing Document Type % =
DIVIDE([Missing Document Type Count], COUNTROWS(accounts_payable_fact), 0)

Invalid Payment Terms Count =
CALCULATE(
    COUNTROWS(accounts_payable_fact),
    ISBLANK(accounts_payable_fact[payment_terms]),
    accounts_payable_fact[account_type] = "K"  -- Only check for vendor line items
)

Invalid Payment Terms % =
DIVIDE([Invalid Payment Terms Count], COUNTROWS(accounts_payable_fact), 0)
```

### Overall Quality Score

```dax
Total Quality Issues =
[Missing Vendor Count] +
[Zero Amount Count] +
[Vendor Not in Master Count] +
[Missing Posting Date Count] +
[Missing Document Type Count]

Data Quality Score =
VAR TotalRecords = COUNTROWS(accounts_payable_fact)
VAR IssueCount = [Total Quality Issues]
RETURN
    DIVIDE(TotalRecords - IssueCount, TotalRecords, 1)

Critical Issues % =
DIVIDE([Total Quality Issues], COUNTROWS(accounts_payable_fact), 0)
```

### Field Completeness Measures

```dax
Posting Date Completeness % =
VAR TotalRecords = COUNTROWS(accounts_payable_fact)
VAR RecordsWithValue = CALCULATE(
    COUNTROWS(accounts_payable_fact),
    NOT(ISBLANK(accounts_payable_fact[posting_date]))
)
RETURN
    DIVIDE(RecordsWithValue, TotalRecords, 0)

Vendor Number Completeness % =
VAR TotalRecords = COUNTROWS(accounts_payable_fact)
VAR RecordsWithValue = CALCULATE(
    COUNTROWS(accounts_payable_fact),
    NOT(ISBLANK(accounts_payable_fact[vendor_number]))
)
RETURN
    DIVIDE(RecordsWithValue, TotalRecords, 0)

Payment Terms Completeness % =
VAR TotalRecords = CALCULATE(
    COUNTROWS(accounts_payable_fact),
    accounts_payable_fact[account_type] = "K"
)
VAR RecordsWithValue = CALCULATE(
    COUNTROWS(accounts_payable_fact),
    NOT(ISBLANK(accounts_payable_fact[payment_terms])),
    accounts_payable_fact[account_type] = "K"
)
RETURN
    DIVIDE(RecordsWithValue, TotalRecords, 0)

Baseline Date Completeness % =
VAR TotalRecords = CALCULATE(
    COUNTROWS(accounts_payable_fact),
    accounts_payable_fact[account_type] = "K"
)
VAR RecordsWithValue = CALCULATE(
    COUNTROWS(accounts_payable_fact),
    NOT(ISBLANK(accounts_payable_fact[baseline_payment_date])),
    accounts_payable_fact[account_type] = "K"
)
RETURN
    DIVIDE(RecordsWithValue, TotalRecords, 0)

Vendor Name Completeness % =
VAR TotalRecords = COUNTROWS(accounts_payable_fact)
VAR RecordsWithValue = CALCULATE(
    COUNTROWS(accounts_payable_fact),
    NOT(ISBLANK(accounts_payable_fact[vendor_name]))
)
RETURN
    DIVIDE(RecordsWithValue, TotalRecords, 0)
```

### Coverage Metrics

```dax
Vendor Coverage Rate =
VAR TotalVendorLines = CALCULATE(
    COUNTROWS(accounts_payable_fact),
    accounts_payable_fact[account_type] = "K"
)
VAR MatchedVendorLines = CALCULATE(
    COUNTROWS(accounts_payable_fact),
    accounts_payable_fact[account_type] = "K",
    accounts_payable_fact[is_vendor_not_in_master] = 0
)
RETURN
    DIVIDE(MatchedVendorLines, TotalVendorLines, 0)
```

---

## Minimum Requirements for Analysis to Work

### Critical (Must Fix - Blocks Analysis)

1. **Posting Date**
   - Requirement: 100% populated
   - Why: Required for time intelligence (YTD, MTD, trends)
   - Fix: Re-run data ingestion, ensure BUDAT field is captured

2. **Document Type**
   - Requirement: 100% populated
   - Why: Distinguishes invoices from payments
   - Fix: Verify BLART field in BKPF table

3. **Amount Fields**
   - Requirement: Non-null for vendor line items (account_type = 'K')
   - Why: Core financial metrics depend on amounts
   - Fix: Check DMBTR field in BSEG, investigate zero amounts

### High Priority (Limits Analysis)

4. **Vendor Number**
   - Requirement: 100% for vendor line items (account_type = 'K')
   - Why: Vendor analysis impossible without vendor ID
   - Fix: Populate LIFNR in BSEG for all vendor postings

5. **Vendor Master Match**
   - Requirement: > 95% match rate
   - Why: Vendor names, details needed for reporting
   - Fix: Add missing vendors to LFA1 table

### Medium Priority (Reduces Analysis Quality)

6. **Payment Terms (baseline_payment_date, payment_terms)**
   - Requirement: > 80% for invoices
   - Why: Aging, overdue, discount calculations fail
   - Fix: Populate ZFBDT and ZTERM in BSEG

7. **Document Date**
   - Requirement: > 90%
   - Why: Alternate date field for analysis
   - Fix: Check BLDAT in BKPF

### Low Priority (Nice to Have)

8. **Line Item Text**
   - Requirement: > 50%
   - Why: Provides context for drill-down
   - Fix: Populate SGTXT in BSEG

9. **Assignment Reference**
   - Requirement: Optional
   - Why: Helps link related documents
   - Fix: Populate ZUONR when available

---

## Action Plan Based on Quality Score

### If Data Quality Score < 80%
**Status:** ❌ Critical - Do Not Proceed
1. Review all critical requirements
2. Fix data ingestion process
3. Re-load data
4. Re-run quality checks

### If Data Quality Score 80-90%
**Status:** ⚠️ Warning - Limited Analysis
1. Identify specific issues
2. Create filtered views excluding bad data
3. Document limitations in report
4. Plan data remediation

### If Data Quality Score 90-95%
**Status:** ✅ Good - Minor Issues
1. Note issues in documentation
2. Proceed with analysis
3. Plan fixes for next iteration

### If Data Quality Score > 95%
**Status:** ✅✅ Excellent
1. Proceed with full analysis
2. All measures will work correctly

---

## Visual Layout Suggestion

```
┌─────────────────────────────────────────────────────────────┐
│  DATA QUALITY OVERVIEW                                      │
├─────────────────────────────────────────────────────────────┤
│  [Quality Score]  [Total Records]  [Date Range]             │
│      95%              426         Jan-Dec 2024               │
├─────────────────────────────────────────────────────────────┤
│  Data Quality Issues            │  Field Completeness       │
│  ┌────────────────────────────┐ │  ┌──────────────────────┐ │
│  │ Issue Type     │ Count │ % │ │  │ posting_date   100%  │ │
│  │ Missing Vendor │   12  │2% │ │  │ vendor_number   98%  │ │
│  │ Zero Amount    │    8  │2% │ │  │ payment_terms   85%  │ │
│  └────────────────────────────┘ │  └──────────────────────┘ │
│                                  │                           │
│  [Issue Severity Gauge: 4%]     │                           │
├─────────────────────────────────────────────────────────────┤
│  Record Distribution                                        │
│  ┌──────────────────────────────────────────────────────┐   │
│  │ [Column Chart: Records by Month]                     │   │
│  └──────────────────────────────────────────────────────┘   │
│                                                             │
│  ┌────────────────────┐  ┌────────────────────────────────┐│
│  │ [Donut: Doc Types] │  │ [Issues to Fix Table]          ││
│  └────────────────────┘  └────────────────────────────────┘│
└─────────────────────────────────────────────────────────────┘
```

