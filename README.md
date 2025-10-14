# SAP Accounts Payable Analytics with Microsoft Fabric

> End-to-end analytics solution for SAP AP data, built on Microsoft Fabric with Power BI

[![Microsoft Fabric](https://img.shields.io/badge/Microsoft%20Fabric-Cloud-blue)](https://www.microsoft.com/microsoft-fabric)
[![Power BI](https://img.shields.io/badge/Power%20BI-Dashboards-yellow)](https://powerbi.microsoft.com/)
[![SAP](https://img.shields.io/badge/SAP-ERP-green)](https://www.sap.com/)

## Overview

This project demonstrates a complete **accounts payable analytics solution** using Microsoft Fabric's unified data platform. It showcases modern data engineering practices, from ingestion through transformation to interactive reporting.

**Key Highlights:**
- Full ETL pipeline using Fabric's native tools
- Two-stage SQL transformation with data quality focus
- 40+ pre-built DAX measures for financial analysis
- 6-page Power BI report covering AP analytics
- Template app ready for deployment

## Use Case

Monitor and analyze accounts payable operations:
- **Track** invoice aging and overdue amounts
- **Measure** payment performance and on-time rates
- **Analyze** vendor spend concentration
- **Optimize** cash discount utilization
- **Ensure** data quality and completeness

Perfect for finance teams, AP managers, and data professionals working with SAP data.

## Architecture

```
SAP Tables -> Dataflow Gen2 -> Lakehouse -> SQL Notebook -> Semantic Model -> Power BI Report
```

See [Architecture Documentation](docs/architecture.md) for detailed component breakdown.

### Technology Stack

- **Ingestion**: Dataflow Gen2 (Power Query/M)
- **Storage**: Lakehouse (Delta Lake)
- **Transformation**: Spark SQL Notebooks
- **Modeling**: Power BI Semantic Model (DAX)
- **Visualization**: Power BI Reports
- **Orchestration**: Data Pipelines
- **Platform**: Microsoft Fabric

## Repository Structure

```
fabric-data-analytics/
├── README.md                           # This file
├── docs/                               # Documentation
│   ├── architecture.md                 # Solution architecture
│   ├── powerbi_report_design.md        # Report specifications
│   └── data_quality_page_design.md     # Data quality dashboard
├── sql/                                # SQL transformations
│   └── create_ap_fact_table.sql        # Two-stage ETL script
├── dax/                                # DAX measure libraries
│   ├── ap_measures.dax                 # Core AP analytics measures
│   └── data_quality_measures.dax       # Data quality measures
├── sample-data/                        # Sample data with documentation
│   ├── README.md
│   ├── sap_bseg_line_items.csv         # 270 line items
│   ├── sap_bkpf_document_header.csv    # 142 documents
│   └── sap_lfa1_vendor_master.csv      # 50 vendors
└── fabric-workspace/                   # Fabric items (via Git integration)
    ├── *.Dataflow/                     # Dataflow definitions
    ├── *.Lakehouse/                    # Lakehouse schemas
    ├── *.Notebook/                     # SQL notebooks
    ├── *.SemanticModel/                # Semantic models
    └── *.Report/                       # Power BI reports
```

## Features

### Data Pipeline
- **Automated ingestion** from SAP tables (BKPF, BSEG, LFA1)
- **Two-stage transformation** separating data quality from business logic
- **Delta Lake storage** with ACID transactions
- **Incremental refresh** capability

### Analytics Capabilities
- **Base Metrics**: Invoice amounts, payment amounts, vendor counts
- **Time Intelligence**: YTD, QTD, MTD comparisons
- **Aging Analysis**: DPO, overdue buckets (0-30, 31-60, 61-90, 90+)
- **Payment Performance**: On-time rates, average payment days
- **Cash Discount**: Utilization tracking, potential savings
- **Vendor Analytics**: Rankings, concentration, segmentation
- **Data Quality**: Completeness metrics, issue tracking

### Power BI Report (6 Pages)
1. **Executive Dashboard**: High-level KPIs and trends
2. **Aging & Overdue Analysis**: Payment aging breakdown
3. **Payment Performance**: Payment efficiency metrics
4. **Vendor Analysis**: Spend concentration and rankings
5. **Cash Discount Optimization**: Discount utilization tracking
6. **Drill-Through Detail**: Transaction-level investigation

## Sample Data

The project is designed to work with SAP Accounts Payable data:
- **BKPF**: Document headers
- **BSEG**: Line items
- **LFA1**: Vendor master data

The `sample-data/` folder contains a README with the required data structure and instructions for:
- Using your own SAP exports
- Generating sample data for testing

> **Note**: Data files (CSV) are never committed to Git. You'll need to provide your own data or generate sample data following the structure in `sample-data/README.md`.

## Getting Started

### Prerequisites
- Microsoft Fabric workspace (Premium capacity or trial)
- Power BI Desktop (latest version)
- Basic knowledge of SQL and DAX

### Quick Start

1. **Clone this repository**
   ```bash
   git clone https://github.com/schmisu/fabric-data-analytics.git
   cd fabric-data-analytics
   ```

2. **Create Fabric workspace**
   - Create a new workspace in Fabric
   - Enable as Template App (optional)

3. **Set up Lakehouse**
   - Create Lakehouse named `SapDataLakehouse`
   - Upload sample data via Dataflow Gen2
   - See `docs/architecture.md` for details

4. **Run SQL transformations**
   - Create new Notebook
   - Copy content from `sql/create_ap_fact_table.sql`
   - Execute to create fact table

5. **Build semantic model**
   - Connect to `accounts_payable_fact` table
   - Import DAX measures from `dax/` folder

6. **Create Power BI report**
   - Follow specifications in `docs/powerbi_report_design.md`
   - Use pre-built measures from semantic model

### Connecting Your Fabric Workspace

This repository is designed to work with Fabric's Git integration:

1. In your Fabric workspace -> **Workspace settings** -> **Git integration**
2. Connect to this repository (main branch)
3. Specify folder: `fabric-workspace/`
4. Fabric will commit all workspace items to the repo
5. Pull updates locally to keep documentation in sync

See [Fabric Git Setup Guide](docs/fabric-git-setup.md) for detailed instructions.

## Key Files

| File | Purpose |
|------|---------|
| `sql/create_ap_fact_table.sql` | Two-stage SQL transformation pipeline |
| `dax/ap_measures.dax` | 40+ pre-built DAX measures for AP analytics |
| `dax/data_quality_measures.dax` | Data quality and completeness measures |
| `docs/architecture.md` | Complete architecture documentation |
| `docs/powerbi_report_design.md` | Power BI report specifications (6 pages) |
| `docs/data_quality_page_design.md` | Data quality dashboard design |

## Technical Highlights

### SQL Transformation Approach
- **Stage 1 (Staging)**: Data type conversion, date parsing, NULL handling
- **Stage 2 (Fact)**: Business logic, joins, calculations
- **Benefits**: Clean separation of concerns, easier debugging

### DAX Measure Organization
- **Base measures**: Simple aggregations
- **Derived measures**: Calculations using base measures
- **Time intelligence**: Built-in date functions
- **Best practices**: Variables, error handling, formatting

### Data Quality First
- Page 0 shows data completeness before analytics
- Field-level quality metrics
- Issue identification and recommendations
- Builds stakeholder confidence

## Use Cases

This solution is ideal for:
- **Finance Teams**: Monitor AP operations, aging, and overdue
- **Treasury**: Optimize cash discount utilization
- **Procurement**: Analyze vendor spend and concentration
- **Data Engineers**: Learn Fabric's unified analytics platform
- **Analysts**: Reference for DAX patterns and report design

## Skills Demonstrated

- Microsoft Fabric platform expertise
- Data pipeline design and orchestration
- SQL transformation patterns (Spark SQL)
- DAX measure development (40+ measures)
- Power BI report design and UX
- Data quality frameworks
- Git/version control for analytics
- SAP data structures (BKPF, BSEG, LFA1)

## Future Enhancements

- [ ] Incremental data refresh
- [ ] Row-level security (multi-company)
- [ ] Mobile-optimized layouts
- [ ] Predictive analytics (late payment risk)
- [ ] Automated alerts (overdue thresholds)
- [ ] Additional SAP tables (BSIK, BSAK)
- [ ] Multi-year historical data

## Known Limitations

- **Single year data**: Sample data is 2024 only (YoY comparisons return BLANK)
- **Simplified schema**: Production would benefit from normalized dimensions
- **Manual refresh**: Automated scheduling requires Fabric Premium capacity

## Contributing

This is a portfolio project, but suggestions are welcome! Feel free to:
- Open issues for questions or ideas
- Fork and adapt for your own use case
- Share feedback on architecture or design choices

## License

This project is open source and available under the [MIT License](LICENSE).

## Contact

**Project by**: Susanne Schmidt [LinkedIn](https://www.linkedin.com/in/dr-susanne-schmidt/)
**GitHub**: [@schmisu](https://github.com/schmisu)

---

*Last updated: October 2025*
