# Key Learnings & Challenges

This document captures the key insights, challenges, and lessons learned from building this data platform.

## What Worked Well

### 1. Fabric's Unified Platform
**Observation:** Having Dataflow, Lakehouse, Notebooks, Semantic Model, and Reports in one platform significantly simplified architecture.

**Benefits:**
- No data movement between tools
- Single security model
- Integrated monitoring
- Simplified deployment

**Impact:** Reduced complexity compared to multi-tool stacks (e.g., Airbyte + Snowflake + dbt + Power BI)

### 2. Two-Stage SQL Transformation Pattern
**Decision:** Separate staging (data quality) from fact (business logic)

**Why It Worked:**
- **Debugging:** Easy to isolate whether issues are data quality or business logic
- **Reusability:** Staging layer can feed multiple fact tables
- **Clarity:** Team members immediately understand the flow
- **Testing:** Can test each stage independently

**Pattern Applied:**
```sql
-- Stage 1: Data quality focused
CREATE OR REPLACE TABLE accounts_payable_staging AS
SELECT
    TRY_CAST(...) AS clean_field,
    CASE WHEN field IS NULL THEN 'MISSING' ELSE 'OK' END AS quality_flag
FROM raw_data;

-- Stage 2: Business logic focused
CREATE OR REPLACE TABLE accounts_payable_fact AS
SELECT
    *,
    CASE WHEN debit_credit = 'H' THEN -amount ELSE amount END AS signed_amount
FROM accounts_payable_staging;
```

### 3. Data Quality Transparency
**Decision:** Build "Page 0" data quality dashboard before analytics pages

**Results:**
- Stakeholders trust the data more
- Issues identified early (before wrong decisions made)
- Clear communication about data limitations
- Users appreciate honesty over hidden problems

**Key Metrics Shown:**
- Field completeness percentages
- Missing data counts
- Data quality score (0-100%)
- Issue summary table

### 4. Git Integration from Day One
**Decision:** Version control all code and documentation

**Benefits:**
- Track changes to SQL, DAX, and documentation
- Collaborate with others (potential)
- Rollback capability
- Professional standard

**Fabric Git Integration:**
- Works well for exporting workspace items
- Some limitations for active development (sync delays)
- Best used for final deployments

## Key Challenges & Solutions

### Challenge 1: SAP Date Format Handling
**Problem:** SAP stores dates as YYYYMMDD strings (e.g., "20240115"), but some records had inconsistent formats or empty strings.

**Initial Approach (Failed):**
```sql
CAST(posting_date AS DATE)  -- Fails on malformed dates
```

**Solution:**
```sql
TRY_CAST(
    CONCAT(
        SUBSTRING(posting_date, 1, 4), '-',
        SUBSTRING(posting_date, 5, 2), '-',
        SUBSTRING(posting_date, 7, 2)
    ) AS DATE
) AS posting_date_clean
```

**Learning:** Always use TRY_CAST for user-provided data. Build robust parsers that handle edge cases gracefully.

---

### Challenge 2: Dataflow vs Notebooks - When to Use What?
**Problem:** Fabric offers both low-code (Dataflow Gen2/Power Query) and code (Notebooks/SQL). Which to use when?

**Discovery:**
- **Dataflow strengths:** Simple transformations, GUI for non-coders, built-in connectors
- **Dataflow limitations:** Complex joins difficult, limited control flow, debugging is hard

**Solution Reached:**
- **Use Dataflow for:** Ingestion, simple type conversions, schema mapping
- **Use Notebooks for:** Complex transformations, multi-stage ETL, business logic

**Pattern:**
```
Dataflow Gen2: CSV → Lakehouse (raw)
Notebook (SQL): Lakehouse (raw) → Lakehouse (staging) → Lakehouse (fact)
```

**Learning:** Use low-code tools for their strength (connectivity), but don't force complex logic into them.

---

### Challenge 3: Single-Year Data Limitation
**Problem:** Sample data only covers 2024. Year-over-year (YoY) DAX measures return BLANK.

**Impact:**
- YoY Growth measures show no results
- Cannot demonstrate full time intelligence capabilities
- Limited storytelling for trends

**Considered Solutions:**
1. Generate synthetic 2023 data (time-consuming)
2. Use Month-over-Month (MoM) instead of YoY
3. Document as known limitation

**Chosen Approach:** Document as limitation, focus on other measures.

**Learning:** For portfolio projects, prioritize breadth over perfection. Document limitations honestly.

---

### Challenge 4: Data Quality Flag Placement
**Problem:** Should data quality flags be in staging table or fact table?

**Decision:** Include quality flags in BOTH:
- **Staging:** Flags for each field (completeness, validity)
- **Fact:** Overall quality score per record

**Rationale:**
- Staging flags help debugging transformations
- Fact flags enable filtering in reports (e.g., "show only high-quality records")

**Implementation:**
```sql
-- Staging: Field-level flags
has_vendor_flag,
has_payment_terms_flag,

-- Fact: Aggregate quality
CASE
    WHEN has_vendor AND has_payment_terms THEN 'HIGH'
    WHEN has_vendor THEN 'MEDIUM'
    ELSE 'LOW'
END AS data_quality_level
```

**Learning:** Data quality should be queryable at every stage.

---

### Challenge 5: Empty vs NULL Handling
**Problem:** SAP exports sometimes have empty strings ("") instead of NULL for missing values.

**Impact:** Queries like `WHERE field IS NULL` don't catch empty strings.

**Solution:**
```sql
NULLIF(TRIM(field), '') AS field_clean
```

**Learning:** Always normalize NULL representation in staging layer. Empty strings should become NULLs.

---

### Challenge 6: Pipeline Parameters with Dataflow Gen2
**Problem:** Dataflow Gen2 with parameters runs successfully when executed independently, but fails when called from a Data Pipeline.

**Root Cause:** Dataflow parameters are not automatically exposed to the pipeline by default.

**Symptoms:**
- Dataflow works fine in isolation
- Pipeline fails with parameter-related errors
- Parameters use default values instead of pipeline-provided values

**Solution:**
In Dataflow Gen2 settings:
1. Go to **Dataflow settings** → **Options**
2. Under **Parameters** section
3. ✅ **Check the box** "Make parameters available to pipeline"
4. Save and retry pipeline

**Alternative Approach:**
Explicitly pass parameters in pipeline activity:
```json
{
  "type": "DataflowActivity",
  "parameters": {
    "ParameterName": "@pipeline().parameters.PipelinePar ameter"
  }
}
```

**Learning:** Dataflow parameters are workspace-scoped by default. Must explicitly enable pipeline access for orchestration scenarios.

**Impact:** This enables flexible, environment-specific configurations (dev/test/prod SharePoint sites, different file paths, etc.).

---

## What I'd Do Differently

### 1. Incremental Refresh from the Start
**Current:** Full refresh every time (all data reprocessed)

**Better Approach:**
```sql
-- Add watermark column
last_modified_timestamp,

-- Query only new/changed records
WHERE last_modified_timestamp > (SELECT MAX(last_processed) FROM watermark_table)
```

**Benefit:** Faster refreshes, lower compute costs, scales better.

---

### 2. Automated Testing for SQL Transformations
**Current:** Manual testing by querying results

**Better Approach:**
```sql
-- Unit tests for transformations
CREATE OR REPLACE TABLE test_results AS
SELECT
    'Document Balance Test' AS test_name,
    CASE
        WHEN COUNT(*) = 0 THEN 'PASS'
        ELSE 'FAIL'
    END AS result
FROM (
    SELECT document_number
    FROM accounts_payable_fact
    GROUP BY document_number
    HAVING ABS(SUM(signed_amount)) > 0.01  -- Debit != Credit
);
```

**Benefit:** Catch issues early, regression testing, continuous validation.

---

### 3. Star Schema with Dimension Tables
**Current:** Flat fact table with embedded dimensions

**Better Approach:**
```
Fact_Transactions
    ├── DimVendor
    ├── DimDate
    ├── DimCompany
    └── DimGLAccount
```

**Benefits:**
- Reduced redundancy
- Easier to update dimension attributes
- Better query performance (smaller fact table)
- Reusable dimensions across fact tables

**Trade-off:** More complex, suitable for production scale.

---

### 4. CI/CD Pipeline for Multi-Environment
**Current:** Single workspace (development + production)

**Better Approach:**
```
Dev Workspace → Test Workspace → Prod Workspace
     ↓               ↓                ↓
   Dev Git      Test Git         Prod Git
```

**Benefits:**
- Test changes before production
- Rollback capability
- Safer deployments

**Tool:** Azure DevOps or GitHub Actions with Fabric APIs

---

## Technical Insights

### Fabric-Specific Learnings

**1. Git Integration Works, But...**
- ✅ Great for exporting workspace definitions
- ✅ Version control for notebooks, DAX, pipelines
- ⚠️ Sync delays make active development slow
- ⚠️ Must manually commit from Fabric UI (can't push from local)

**Recommendation:** Use Git for final deployments, not daily development.

**2. Dataflow Gen2 Power and Limits**
- ✅ Excellent for connectivity (many built-in connectors)
- ✅ GUI makes it accessible to non-coders
- ✅ Automatic schema detection
- ⚠️ Complex transformations get messy quickly
- ⚠️ Debugging is difficult (no step-through)
- ⚠️ Performance tuning limited

**Recommendation:** Use Dataflow for simple ingestion, Notebooks for transformations.

**3. Lakehouse is Powerful**
- ✅ Delta Lake ACID transactions
- ✅ Time travel (query historical versions)
- ✅ Unified batch and streaming
- ✅ Open format (not vendor lock-in)
- ⚠️ Requires understanding of partitioning for performance
- ⚠️ Different mental model than traditional data warehouse

**Recommendation:** Invest time learning Delta Lake patterns.

---

## Platform Engineering Insights

### 1. Data Quality is a Feature, Not a Burden
Early investment in data quality framework paid dividends:
- Faster issue identification
- Better stakeholder trust
- Reduced "bad data" complaints
- Clear communication of limitations

### 2. Documentation is Code
Spending time on README, architecture docs, and code comments:
- Helps future self understand decisions
- Enables collaboration
- Demonstrates professionalism
- Makes project more valuable

### 3. Two-Stage Pattern is Reusable
The staging → fact pattern works for any domain:
- E-commerce: Orders, Customers, Products
- HR: Employees, Attendance, Performance
- Manufacturing: Machines, Production, Quality

**Key:** Separate data quality concerns from business logic.

### 4. Self-Service Requires Structure
Enabling self-service analytics needs:
- **Clear semantic layer** (DAX measures with business-friendly names)
- **Data quality transparency** (users need to know data limitations)
- **Documentation** (measure definitions, calculation logic)
- **Governance** (who can see what data)

---

## Future Enhancements (Lessons Applied)

Based on these learnings, future work would include:

### Short-Term (High ROI)
1. **Incremental refresh** - Watermark-based pattern
2. **Automated tests** - SQL-based validation queries
3. **Performance tuning** - Partitioning, indexing, caching

### Medium-Term (Scale)
4. **Star schema normalization** - Dimension tables
5. **Multi-environment** - Dev/Test/Prod pipeline
6. **Monitoring dashboard** - Refresh status, errors, performance

### Long-Term (Advanced)
7. **Real-time streaming** - Event Streams for live data
8. **Predictive analytics** - ML models for forecasting
9. **Data catalog** - Metadata management, lineage

---

## Closing Thoughts

**Key Takeaway:** Building a data platform end-to-end, even on a small scale, reveals insights no amount of reading can provide.

**Challenges Faced:**
- Date format handling → Robust parsing needed
- Tool selection (Dataflow vs Notebook) → Right tool for right job
- Data quality → Transparency builds trust
- Single-year limitation → Perfect is enemy of good

**Skills Developed:**
- Fabric platform expertise
- ETL pattern design
- Data quality frameworks
- SQL and DAX proficiency
- Documentation and communication

**What I'd Tell My Past Self:**
1. Start with data quality framework (don't add it later)
2. Use notebooks for complex logic (don't fight Dataflow limitations)
3. Document decisions as you go (don't wait until the end)
4. Accept imperfection (single-year data is fine for portfolio)

---

**Version:** 1.0
**Last Updated:** October 2024
**Author:** Susanne Schmidt
