# Power BI Report Design - Accounts Payable Analytics

## Report Structure Overview

6-page report covering end-to-end AP process monitoring and vendor management.

---

## Page 1: Executive Dashboard

**Purpose:** High-level KPIs for management overview

### Visuals:

1. **KPI Card - Total Invoice Amount**
   - Measure: `[Total Invoice Amount]`
   - Trend: `[Total Invoice Amount PY]`
   - Visual: Card or Multi-row card

2. **KPI Card - Net Payables**
   - Measure: `[Net Payables]`
   - Visual: Card

3. **KPI Card - Days Payable Outstanding**
   - Measure: `[Days Payable Outstanding (DPO)]`
   - Conditional formatting: Use `[DPO Status]`
   - Visual: Card

4. **KPI Card - Overdue Amount**
   - Measure: `[Overdue Amount]`
   - % of total: `[% Overdue]`
   - Conditional formatting: Red if > 100K
   - Visual: Card

5. **Line Chart - Invoice Trend (YoY Comparison)**
   - X-axis: `posting_date` (Month)
   - Y-axis: `[Total Invoice Amount]`, `[Total Invoice Amount PY]`
   - Legend: Current Year vs Prior Year
   - Visual: Line chart

6. **Clustered Column Chart - Monthly Invoice Volume**
   - X-axis: `posting_date` (Month) ####Date Hirarchy not possible <- check date format
   - Y-axis: `[Invoice Count]` ####Only 1 Document per Month <- rerun data generation with. more invoices
   - Data labels: On
   - Visual: Clustered column chart

7. **Donut Chart - Payment Status**
   - Legend: `[Payment Status]` <- Measure as Legend not possible
   - Values: `[Total Invoice Amount]`
   - Visual: Donut chart

8. **Table - Top 5 Vendors by Spend**
   - Columns:
     - `vendor_name`
     - `[Total Invoice Amount]`
     - `[Invoice Count]`
     - `[% of Total Spend]`
   - Sort: `[Total Invoice Amount]` DESC
   - Top N filter: Top 5
   - Visual: Table

### Slicers:
- `posting_date` (Relative date slicer)
- `company_code`
- `vendor_country`

---

## Page 2: Aging & Overdue Analysis

**Purpose:** Deep dive into payment aging and overdue management

### Visuals:

1. **KPI Card - Overdue Amount**
   - Measure: `[Overdue Amount]`
   - Visual: Card with red background

2. **KPI Card - Overdue Invoices**
   - Measure: `[Overdue Invoices]`
   - Visual: Card

3. **KPI Card - % Overdue**
   - Measure: `[% Overdue]`
   - Format: Percentage
   - Visual: Card

4. **Stacked Bar Chart - Aging Buckets**
   - Y-axis: Category (manual labels)
   - X-axis:
     - `[Aging 0-30 Days]`
     - `[Aging 31-60 Days]`
     - `[Aging 61-90 Days]`
     - `[Aging 90+ Days]`
   - Data labels: On
   - Visual: Stacked bar chart or Clustered bar chart
   - Color coding: Green → Yellow → Orange → Red

5. **Table - Overdue Invoices Detail**
   - Columns:
     - `vendor_name`
     - `document_number`
     - `document_date`
     - `net_due_date`
     - `[Total Invoice Amount]`
     - Calculated column: Days Overdue (Today - net_due_date)
   - Filter: `net_due_date` < TODAY
   - Sort: Days Overdue DESC
   - Visual: Table with conditional formatting

6. **Matrix - Aging by Vendor**
   - Rows: `vendor_name`
   - Columns: Aging buckets (0-30, 31-60, 61-90, 90+)
   - Values: `[Total Invoice Amount]`
   - Conditional formatting: Heat map
   - Visual: Matrix

7. **Line Chart - Overdue Trend Over Time**
   - X-axis: `posting_date` (Month)
   - Y-axis: `[Overdue Amount]`
   - Visual: Line chart with area fill

### Slicers:
- `posting_date`
- `vendor_name` (Search enabled)
- `company_code`

---

## Page 3: Payment Performance

**Purpose:** Monitor payment efficiency and compliance

### Visuals:

1. **KPI Card - On-Time Payment Rate**
   - Measure: `[On-Time Payment Rate]`
   - Format: Percentage
   - Visual: Gauge (0-100%)

2. **KPI Card - Average Payment Days**
   - Measure: `[Average Payment Days]`
   - Visual: Card

3. **KPI Card - Total Payment Amount**
   - Measure: `[Total Payment Amount]`
   - Visual: Card

4. **Clustered Column Chart - Payments vs Invoices (Monthly)**
   - X-axis: `posting_date` (Month)
   - Y-axis:
     - `[Total Invoice Amount]`
     - `[Total Payment Amount]`
   - Legend: Invoice vs Payment
   - Visual: Clustered column chart

5. **Scatter Chart - Payment Days vs Invoice Amount**
   - X-axis: `[Average Payment Days]`
   - Y-axis: `[Total Invoice Amount]`
   - Details: `vendor_name`
   - Size: `[Invoice Count]`
   - Visual: Scatter chart

6. **Waterfall Chart - Cash Flow Analysis**
   - Category: `posting_date` (Month)
   - Y-axis:
     - Starting: `[Net Payables]` (previous month)
     - Increase: `[Total Invoice Amount]`
     - Decrease: `[Total Payment Amount]`
   - Visual: Waterfall chart

7. **Table - Payment Performance by Vendor**
   - Columns:
     - `vendor_name`
     - `[Total Payment Amount]`
     - `[Average Payment Days]`
     - `[On-Time Payment Rate]`
   - Sort: `[Total Payment Amount]` DESC
   - Conditional formatting: Green for high on-time rate
   - Visual: Table

### Slicers:
- `posting_date`
- `vendor_name`
- `document_type`

---

## Page 4: Vendor Analysis

**Purpose:** Vendor spend concentration and segmentation

### Visuals:

1. **KPI Card - Vendor Count**
   - Measure: `[Vendor Count]`
   - Visual: Card

2. **KPI Card - Average Invoice Value**
   - Measure: `[Average Invoice Value]`
   - Visual: Card

3. **KPI Card - Vendor Concentration %**
   - Measure: `[Vendor Concentration %]`
   - Visual: Card

4. **Pareto Chart - Top 20 Vendors (80/20 Rule)**
   - X-axis: `vendor_name` (Top 20)
   - Y-axis (Bars): `[Total Invoice Amount]`
   - Y-axis (Line): `[Running Total Invoice Amount]` or cumulative %
   - Visual: Combo chart (Column + Line)
   - Sort: `[Total Invoice Amount]` DESC

5. **Map - Vendor Spend by Country**
   - Location: `vendor_country`
   - Size: `[Total Invoice Amount]`
   - Visual: Map or Filled map

6. **Table - Vendor Master List with Rankings**
   - Columns:
     - `[Vendor Rank by Spend]`
     - `vendor_name`
     - `vendor_city`
     - `vendor_country`
     - `[Total Invoice Amount]`
     - `[Invoice Count]`
     - `[% of Total Spend]`
   - Sort: `[Vendor Rank by Spend]` ASC
   - Visual: Table

7. **Matrix - Spend by Vendor & GL Account**
   - Rows: `vendor_name`
   - Columns: `gl_account` (or cost category)
   - Values: `[Total Invoice Amount]`
   - Visual: Matrix with conditional formatting

8. **Treemap - Vendor Hierarchy by Spend**
   - Group: `vendor_country` → `vendor_name`
   - Values: `[Total Invoice Amount]`
   - Visual: Treemap

### Slicers:
- `posting_date`
- `vendor_country`
- `vendor_account_group`
- Top N vendors (manual entry)

---

## Page 5: Cash Discount Optimization

**Purpose:** Track cash discount opportunities and utilization

### Visuals:

1. **KPI Card - Total Cash Discount Available**
   - Measure: `[Total Cash Discount Available]`
   - Visual: Card

2. **KPI Card - Cash Discount Taken**
   - Measure: `[Cash Discount Taken]`
   - Visual: Card with green background

3. **KPI Card - Cash Discount Utilization %**
   - Measure: `[Cash Discount Utilization %]`
   - Visual: Gauge (0-100%)

4. **KPI Card - Potential Savings**
   - Measure: `[Potential Savings]`
   - Visual: Card with yellow background

5. **Clustered Column Chart - Discount Taken vs Available (Monthly)**
   - X-axis: `posting_date` (Month)
   - Y-axis:
     - `[Total Cash Discount Available]`
     - `[Cash Discount Taken]`
   - Visual: Clustered column chart

6. **Table - Upcoming Discount Opportunities**
   - Columns:
     - `vendor_name`
     - `document_number`
     - `baseline_payment_date`
     - `cash_discount_due_date`
     - `[Total Invoice Amount]`
     - `cash_discount_amount`
   - Filter: `cash_discount_due_date` >= TODAY AND <= TODAY + 7 days
   - Sort: `cash_discount_due_date` ASC
   - Visual: Table with urgency indicators

7. **Table - Cash Discount Performance by Vendor**
   - Columns:
     - `vendor_name`
     - `[Total Cash Discount Available]`
     - `[Cash Discount Taken]`
     - `[Cash Discount Utilization %]`
     - `[Potential Savings]`
   - Sort: `[Potential Savings]` DESC
   - Visual: Table

8. **Donut Chart - Payment Terms Distribution**
   - Legend: `payment_terms`
   - Values: `[Invoice Count]`
   - Visual: Donut chart

### Slicers:
- `posting_date`
- `vendor_name`
- `payment_terms`

---

## Page 6: Drill-Through Detail Page

**Purpose:** Transaction-level detail for investigation

### Configuration:
- Set as **Drill-through page**
- Drill-through fields: `vendor_name`, `document_number`

### Visuals:

1. **Card - Selected Vendor Name**
   - Field: `vendor_name`
   - Visual: Card (large font)

2. **Cards - Vendor Details**
   - `vendor_city`
   - `vendor_country`
   - `vendor_tax_number_1`
   - Visual: Multi-row card

3. **Table - All Transactions for Selected Context**
   - Columns:
     - `document_number`
     - `document_type_description`
     - `posting_date`
     - `document_date`
     - `net_due_date`
     - `amount_local_currency`
     - `debit_credit_indicator`
     - `line_item_text`
     - `gl_account`
   - Sort: `posting_date` DESC
   - Visual: Table with alternating row colors

4. **Clustered Bar Chart - Spend by GL Account**
   - Y-axis: `gl_account`
   - X-axis: `[Total Invoice Amount]`
   - Visual: Clustered bar chart

5. **Line Chart - Transaction Trend**
   - X-axis: `posting_date` (Month)
   - Y-axis: `[Total Invoice Amount]`
   - Visual: Line chart

6. **Slicer - Document Type**
   - Field: `document_type_description`
   - Visual: Slicer (horizontal)

---

## Additional Recommendations

### Cross-Page Features:

1. **Navigation Buttons**
   - Create buttons with actions to navigate between pages
   - Icon-based or text-based navigation bar on every page

2. **Bookmarks**
   - Create bookmarks for common filters (e.g., "Current Month", "YTD", "Overdue Only")
   - Add bookmark navigator for quick access

3. **Tooltips**
   - Create custom tooltip pages for vendor details
   - Apply to vendor-related visuals across all pages

4. **Color Scheme**
   - Primary: Dark blue (#003366) for headers
   - Accent: Orange/Red for overdue/critical items
   - Success: Green for on-time/good performance
   - Neutral: Gray for backgrounds

5. **Filters & Parameters**
   - Page-level vs report-level filters (define hierarchy)
   - Sync slicers across pages where appropriate

### Data Refresh Strategy:
- Schedule daily refresh at 6 AM
- Incremental refresh for large datasets
- Display last refresh time on each page

---

## Visual Priority by Page

### Must-Have Visuals (MVP):
- Page 1: KPI cards, YoY trend line
- Page 2: Aging buckets chart, overdue table
- Page 3: Payment rate gauge, payments vs invoices chart
- Page 4: Pareto chart, vendor ranking table
- Page 5: Discount utilization gauge, opportunities table

### Nice-to-Have (Phase 2):
- Advanced scatter plots
- Custom R/Python visuals
- Decomposition trees
- Key influencers visual

---

## File Structure for Handoff

```
fabric-data-analytics/
├── sql/
│   └── create_ap_fact_table.sql
├── dax/
│   └── ap_measures.dax
├── docs/
│   └── powerbi_report_design.md (this file)
└── powerbi/
    └── AP_Analytics.pbix (your report file)
```

---

## Next Steps

1. Build Page 1 (Executive Dashboard) first as foundation
2. Test drill-through functionality with Page 6
3. Add remaining pages incrementally
4. Apply consistent formatting and theme
5. Create mobile layout for key pages
6. Document insights and recommendations in textboxes
7. Publish to Fabric workspace when complete
