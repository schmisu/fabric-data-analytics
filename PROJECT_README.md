# SAP Accounts Payable Analytics - Fabric Template

A complete Microsoft Fabric solution template for SAP accounts payable analytics with German company context.

## Architecture Overview

This template provides an end-to-end analytics solution:

1. **Data Ingestion**: Single dataflow ingests all three SAP tables (BKPF, BSEG, LFA1)
2. **Data Processing**: Lakehouse with Notebooks for data manipulation and transformation
3. **Data Modeling**: Semantic model with proper relationships and measures
4. **Visualization**: Power BI report with comprehensive financial analyses

## Folder Structure

```
fabric-data-analytics/
├── resources/                          # Local development data (not in git)
│   └── sap-sample-data/               # Sample CSV files for development
├── docs/                              # Complete documentation
│   ├── 01-dataflow-setup.md          # Dataflow creation process
│   ├── 02-lakehouse-notebooks.md     # Data transformation process
│   ├── 03-semantic-model.md          # Data modeling process
│   ├── 04-powerbi-report.md          # Report creation process
│   └── git-fabric-integration.md     # Git/Fabric workspace integration
├── fabric-items/                     # Fabric workspace items structure
│   ├── dataflows/                    # Dataflow definitions and M code
│   ├── lakehouses/                   # Lakehouse schemas and configs
│   ├── notebooks/                    # Spark/Python notebooks
│   ├── semantic-models/              # Data model definitions
│   └── reports/                      # Power BI report templates
└── data_validation_queries.sql       # Data validation and analysis queries
```

## Git/Fabric Integration Strategy

Two repository approach:
- **This repo (fabric-data-analytics)**: Development, documentation, sample data
- **Fabric workspace repo**: Auto-synced with Fabric items (dataflows, notebooks, etc.)

## Quick Start

1. Follow `docs/01-dataflow-setup.md` for data ingestion
2. Use `docs/02-lakehouse-notebooks.md` for data processing
3. Build semantic model per `docs/03-semantic-model.md`
4. Create reports following `docs/04-powerbi-report.md`

## Sample Data

- 50 German vendor records (LFA1)
- 142 accounting documents (BKPF)
- 268 line items (BSEG)
- 12 months of 2024 data
- €3.5M+ transaction volume
- Proper SAP relationships and German VAT

Users should replace sample data with their own SAP exports using the same structure.