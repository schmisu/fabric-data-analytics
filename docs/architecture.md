# Solution Architecture

## Overview

End-to-end SAP Accounts Payable analytics solution built on Microsoft Fabric, demonstrating modern data platform capabilities for financial reporting and analysis.

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────────┐
│                         DATA SOURCES                                 │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐                          │
│  │  BKPF    │  │  BSEG    │  │  LFA1    │                          │
│  │ Document │  │   Line   │  │ Vendor   │                          │
│  │ Headers  │  │  Items   │  │  Master  │                          │
│  └────┬─────┘  └────┬─────┘  └────┬─────┘                          │
│       │             │             │                                  │
└───────┼─────────────┼─────────────┼──────────────────────────────────┘
        │             │             │
        ▼             ▼             ▼
┌─────────────────────────────────────────────────────────────────────┐
│                    INGESTION LAYER                                   │
│  ┌──────────────────────────────────────────────────────┐           │
│  │         Dataflow Gen2 (Power Query)                  │           │
│  │  • Data type transformations                         │           │
│  │  • Initial data validation                           │           │
│  │  • Load to Lakehouse tables                          │           │
│  └───────────────────────┬──────────────────────────────┘           │
│                          │                                           │
└──────────────────────────┼───────────────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────────────┐
│                    STORAGE LAYER                                     │
│  ┌──────────────────────────────────────────────────────┐           │
│  │         Lakehouse: SapDataLakehouse                  │           │
│  │  Tables:                                             │           │
│  │  • bseg (270 records)                                │           │
│  │  • bkpf (142 records)                                │           │
│  │  • lfa1 (50 records)                                 │           │
│  └───────────────────────┬──────────────────────────────┘           │
│                          │                                           │
└──────────────────────────┼───────────────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────────────┐
│                 TRANSFORMATION LAYER                                 │
│  ┌──────────────────────────────────────────────────────┐           │
│  │         Notebook: SQL Transformation                 │           │
│  │  Stage 1: accounts_payable_staging                   │           │
│  │  • Data type casting                                 │           │
│  │  • Date parsing (YYYYMMDD → DATE)                    │           │
│  │  • NULL handling                                     │           │
│  │                                                      │           │
│  │  Stage 2: accounts_payable_fact                      │           │
│  │  • Join BSEG + BKPF + LFA1                           │           │
│  │  • Business logic (signed amounts)                   │           │
│  │  • Document type classification                      │           │
│  │  • Due date calculations                             │           │
│  │  • Data quality flags                                │           │
│  │                                                      │           │
│  │  Supporting Views:                                   │           │
│  │  • ap_data_quality_summary                           │           │
│  │  • ap_vendor_summary                                 │           │
│  └───────────────────────┬──────────────────────────────┘           │
│                          │                                           │
└──────────────────────────┼───────────────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────────────┐
│                   SEMANTIC LAYER                                     │
│  ┌──────────────────────────────────────────────────────┐           │
│  │         Power BI Semantic Model                      │           │
│  │                                                      │           │
│  │  Data Model:                                         │           │
│  │  • accounts_payable_fact (Star schema)               │           │
│  │                                                      │           │
│  │  DAX Measures (40+):                                 │           │
│  │  • Base metrics (amounts, counts)                    │           │
│  │  • Time intelligence (YTD, QTD, MTD, YoY)            │           │
│  │  • Aging analysis (DPO, overdue buckets)             │           │
│  │  • Payment performance (on-time rate, days)          │           │
│  │  • Cash discount tracking                            │           │
│  │  • Vendor analytics (rankings, concentration)        │           │
│  │  • Data quality metrics                              │           │
│  └───────────────────────┬──────────────────────────────┘           │
│                          │                                           │
└──────────────────────────┼───────────────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────────────┐
│                 PRESENTATION LAYER                                   │
│  ┌──────────────────────────────────────────────────────┐           │
│  │         Power BI Report (6 Pages)                    │           │
│  │  Page 0: Data Quality Overview                       │           │
│  │  Page 1: Executive Dashboard                         │           │
│  │  Page 2: Aging & Overdue Analysis                    │           │
│  │  Page 3: Payment Performance                         │           │
│  │  Page 4: Vendor Analysis                             │           │
│  │  Page 5: Cash Discount Optimization                  │           │
│  │  Page 6: Drill-Through Detail                        │           │
│  └──────────────────────────────────────────────────────┘           │
│                                                                      │
└──────────────────────────────────────────────────────────────────────┘
```

## Component Details

### 1. Data Ingestion (Dataflow Gen2)
- **Technology**: Power Query (M language)
- **Function**: Extract SAP tables and load to Lakehouse
- **Key Features**:
  - Parameterized connections
  - Incremental refresh capability
  - Data quality checks at source

### 2. Data Storage (Lakehouse)
- **Technology**: Delta Lake format
- **Function**: Centralized data lake + SQL analytics
- **Tables**:
  - `bseg`: Line-level transaction items
  - `bkpf`: Document header information
  - `lfa1`: Vendor master data

### 3. Data Transformation (Notebook)
- **Technology**: Spark SQL
- **Function**: Multi-stage transformation pipeline
- **Approach**: Two-stage ETL
  - **Stage 1 (Staging)**: Data quality and type conversion
  - **Stage 2 (Fact)**: Business logic and enrichment
- **File**: `sql/create_ap_fact_table.sql`

### 4. Semantic Modeling (Power BI)
- **Technology**: Tabular model with DAX
- **Function**: Business logic and calculation layer
- **Measures**: 40+ pre-built DAX measures
- **Files**: `dax/ap_measures.dax`, `dax/data_quality_measures.dax`

### 5. Visualization (Power BI Report)
- **Technology**: Power BI Desktop/Service
- **Function**: Interactive dashboards and reports
- **Design**: `docs/powerbi_report_design.md`

## Data Flow

```
SAP Tables (CSV)
  → Dataflow Gen2 (M)
    → Lakehouse Tables (Delta)
      → SQL Transformation (Spark SQL)
        → Fact Table (Delta)
          → Semantic Model (DAX)
            → Power BI Report
```

## Key Design Decisions

### 1. Two-Stage SQL Transformation
**Rationale**: Separate data quality from business logic
- Stage 1 focuses on data types, parsing, NULL handling
- Stage 2 applies business rules and calculations
- **Benefit**: Easier debugging, reusable for different data sources

### 2. Business Logic in SQL (Not DAX)
**Rationale**: Better performance and portability
- Signed amounts calculated in SQL
- Document type descriptions in SQL
- Only time intelligence stays in DAX
- **Benefit**: Faster queries, reusable across tools

### 3. Data Quality First Approach
**Implementation**: Page 0 in report shows quality metrics
- Shows completeness percentages
- Identifies missing data
- Builds trust with stakeholders
- **Benefit**: Transparency and confidence in data

### 4. Star Schema (Simplified)
**Current**: Single fact table with embedded dimensions
- Suitable for current data volume (~400 records)
- Could be normalized for production scale
- **Benefit**: Simple to understand and query

## Technology Stack

| Layer | Technology | Purpose |
|-------|-----------|---------|
| **Ingestion** | Dataflow Gen2 (Power Query) | Extract and load SAP data |
| **Storage** | Lakehouse (Delta Lake) | Unified data storage |
| **Transformation** | Spark SQL | Data processing and business logic |
| **Modeling** | Power BI Semantic Model | Business calculations (DAX) |
| **Visualization** | Power BI Report | Interactive dashboards |
| **Orchestration** | Data Pipeline | Scheduling and automation |
| **Source Control** | Git/GitHub | Version control |
| **Platform** | Microsoft Fabric | Unified analytics platform |

## Scalability Considerations

### Current Implementation (Demo)
- Single fact table: ~400 records
- 2024 data only
- Embedded dimensions
- Manual refresh

### Production Enhancements
- Incremental data loads (delta only)
- Partition by year/month
- Separate dimension tables
- Automated daily refresh
- Row-level security (RLS)
- Historical archive strategy

## Data Model

### Fact Table: `accounts_payable_fact`
- **Grain**: One row per line item (BSEG level)
- **Keys**: document_number + line_item_number
- **Measures**: amounts, dates, indicators
- **Dimensions**: vendor, GL account, document type

### Conformed Dimensions (Embedded)
- Vendor (from LFA1)
- Document Header (from BKPF)
- Time (derived from posting_date)

## Security & Governance

### Access Control
- Workspace-level permissions in Fabric
- Row-level security (RLS) ready for multi-company scenarios
- Sensitive fields can be masked (e.g., tax numbers)

### Data Lineage
- Clear path from source to visualization
- SQL scripts version-controlled
- DAX measures documented

### Compliance
- GDPR considerations: Vendor data handling
- Audit trail: Git commit history
- Data retention: Configurable in Lakehouse

## Performance Optimization

### Current Optimizations
- Delta Lake format (columnar storage)
- Pre-aggregated measures in SQL
- Efficient DAX patterns (avoid row context)

### Future Optimizations
- Aggregation tables in semantic model
- Partitioning by date
- DirectLake mode for real-time queries

## Deployment Strategy

### Development → Production
1. Develop in feature workspace
2. Export as template app
3. Deploy to production workspace
4. Configure refresh schedules
5. Share reports with stakeholders

### CI/CD Potential
- Git integration for version control
- Automated testing of SQL transformations
- Deployment pipelines via Azure DevOps

## Monitoring & Maintenance

### Health Checks
- Data refresh success/failure alerts
- Row count validation
- Data quality score thresholds

### Maintenance Tasks
- Monthly review of data quality metrics
- Quarterly measure optimization
- Annual archiving of old data

---

**Version**: 1.0
**Last Updated**: 2025-10-15
**Author**: [Dr. Susanne Schmidt](https://www.linkedin.com/in/dr-susanne-schmidt/)
