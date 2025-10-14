# Modern Data Platform Architecture - Portfolio Project

> **Demonstrating end-to-end platform engineering** using Microsoft Fabric's unified analytics stack.
> Built a production-ready data pipeline from ingestion through transformation to self-service analytics.

**Purpose:** Portfolio project showcasing data platform architecture, lakehouse patterns, and analytics engineering best practices.

**Domain:** Financial analytics (accounts payable) chosen for realistic enterprise data complexity and data quality challenges.

⚠️ **Note:** This is a portfolio/learning project built for demonstrating technical capabilities, not for commercial use.

[![Microsoft Fabric](https://img.shields.io/badge/Microsoft%20Fabric-Platform-blue)](https://www.microsoft.com/microsoft-fabric)
[![Lakehouse](https://img.shields.io/badge/Lakehouse-Delta%20Lake-green)](https://delta.io/)
[![Platform Engineering](https://img.shields.io/badge/Platform-Engineering-orange)](https://github.com/schmisu/fabric-data-analytics)

## Overview

This project demonstrates **platform engineering capabilities** through a complete data platform implementation:

**Platform Focus:**
- End-to-end data pipeline architecture
- Reusable transformation frameworks
- Data quality and observability patterns
- Self-service analytics enablement
- Modern lakehouse implementation

**Technical Depth:**
- Two-stage ETL transformation pattern
- Data quality framework with monitoring
- Semantic modeling layer (40+ reusable measures)
- Git-based version control for analytics
- Production-ready documentation

**Business Context:**
The accounts payable domain was selected to showcase enterprise data complexity - multiple data sources, referential integrity, data quality issues, and real-world business logic. The technical patterns demonstrated here apply to any enterprise data platform.

## Why This Project?

After building data platforms professionally for 7+ years, I wanted to demonstrate modern platform engineering using cutting-edge tools.

**Goals:**
- Master Microsoft Fabric's unified analytics platform
- Build a reusable, production-ready data pipeline architecture
- Demonstrate best practices in data quality, testing, and documentation
- Create a reference implementation for lakehouse patterns

**Why Accounts Payable?**
- Realistic enterprise data complexity (multiple sources, relationships, data quality challenges)
- Well-understood domain allows focus on technical architecture excellence
- Showcases both technical depth (SQL, DAX, data modeling) and business value (KPIs, insights)
- Common enterprise use case that demonstrates transferable patterns

**This is a learning/portfolio project**, not production work or client engagement.

## Architecture

```
Data Sources -> Dataflow Gen2 -> Lakehouse -> SQL Notebooks -> Semantic Model -> Power BI
    (CSV)      (Ingestion)     (Delta Lake)  (Transform)     (DAX Layer)    (Self-Service)
```

**Platform Components:**

| Layer | Technology | Purpose | Pattern Demonstrated |
|-------|-----------|---------|---------------------|
| **Ingestion** | Dataflow Gen2 (M) | Extract & Load | Connector integration, schema mapping |
| **Storage** | Lakehouse (Delta) | Unified data lake | ACID transactions, time travel |
| **Transform** | Spark SQL Notebooks | Data processing | Two-stage ETL, data quality framework |
| **Semantic** | Power BI Model (DAX) | Business logic | Metric definitions, reusable calculations |
| **Visualization** | Power BI Reports | Self-service analytics | Dashboard design, drill-through patterns |
| **Orchestration** | Data Pipeline | Scheduling | Dependency management |
| **Version Control** | Git integration | Code management | Infrastructure as code |

See [Architecture Documentation](docs/architecture.md) for detailed component breakdown and [Learnings](docs/learnings.md) for key insights.

## Platform Capabilities Demonstrated

### 1. Data Integration & Connectors
- **CSV ingestion** via Dataflow Gen2 (demonstrates connector pattern)
- Schema mapping and data type handling
- Error handling for malformed data
- Extensible pattern for additional sources (SAP direct, APIs, databases)

### 2. Data Quality Framework
- **Two-stage transformation**: Separation of data quality from business logic
- Quality flags on every record (completeness, validity)
- Data profiling and validation queries
- Quality dashboard ("Page 0") showing issues before analytics
- **Pattern:** Quality-first approach builds stakeholder trust

### 3. Lakehouse Architecture
- **Delta Lake** format for ACID transactions
- Structured data with schema enforcement
- Ready for incremental refresh patterns
- Query performance optimization
- **Pattern:** Modern lakehouse replaces traditional data warehouse

### 4. Transformation Patterns
- **Stage 1 (Staging)**: Data type conversion, date parsing, NULL handling
- **Stage 2 (Fact)**: Business logic, joins, calculations, enrichment
- SQL-based for portability and performance
- Supporting views for data quality and summaries
- **Pattern:** Reusable framework for any domain

### 5. Semantic Modeling Layer
- 40+ pre-built DAX measures organized by category
- Base measures + derived measures pattern
- Time intelligence (YTD, QTD, MTD, YoY)
- Error handling and defensive DAX
- **Pattern:** Self-service analytics through reusable metrics

### 6. Self-Service Analytics
- 6-page Power BI report with drill-through
- Data quality overview (transparency)
- Executive dashboards
- Detailed analysis pages
- **Pattern:** Tiered access - overview to detail

### 7. DevOps & Version Control
- Git integration for Fabric workspace
- Documentation as code
- SQL and DAX scripts version controlled
- **Pattern:** Infrastructure as code for analytics

## Repository Structure

```
fabric-data-analytics/
├── README.md                           # This file (project overview)
├── docs/                               # Platform documentation
│   ├── architecture.md                 # Detailed architecture & design decisions
│   ├── learnings.md                    # Key learnings & challenges
│   ├── powerbi_report_design.md        # Report specifications
│   ├── data_quality_page_design.md     # Data quality dashboard
│   └── fabric-git-setup.md             # Git integration guide
├── sql/                                # Transformation code
│   └── create_ap_fact_table.sql        # Two-stage ETL implementation
├── dax/                                # Semantic layer measures
│   ├── ap_measures.dax                 # Core business logic (40+ measures)
│   └── data_quality_measures.dax       # Data quality metrics
├── sample-data/                        # Data folder (CSV files gitignored)
│   └── README.md                       # Data structure documentation
└── fabric-workspace/                   # Fabric items (via Git integration)
    ├── DataIngestion.Dataflow/         # Dataflow definitions
    ├── SapDataLakehouse.Lakehouse/     # Lakehouse configuration
    ├── 0_DataCleaning.Notebook/        # Transformation notebooks
    ├── Accounts Payable.SemanticModel/ # Semantic model definition
    ├── Accounts Payable.Report/        # Power BI report
    └── Orchestration.DataPipeline/     # Pipeline orchestration
```

## Key Technical Decisions

### 1. Two-Stage SQL Transformation
**Decision:** Separate data quality (staging) from business logic (fact)
**Rationale:** Easier debugging, reusable for different data sources, clear separation of concerns
**Trade-off:** Creates intermediate staging table (acceptable for clarity gained)

### 2. Business Logic in SQL (Not DAX)
**Decision:** Calculate signed amounts, document types, due dates in SQL
**Rationale:** Better performance, reusable across tools, easier testing
**Exception:** Time intelligence stays in DAX (native support, user-friendly)

### 3. Data Quality First Approach
**Decision:** Page 0 shows quality metrics before analytics
**Rationale:** Transparency builds trust, identifies issues early, sets expectations
**Implementation:** Quality flags on every record, completeness percentages, issue counts

### 4. Lakehouse over Data Warehouse
**Decision:** Use Lakehouse (Delta Lake) instead of traditional DW
**Rationale:** Modern architecture, better for analytics, flexible schema, time travel
**Trade-off:** Requires different thinking than traditional star schema

### 5. Git Integration from Day One
**Decision:** Version control all code and configuration
**Rationale:** Professional standard, enables collaboration, tracks changes
**Implementation:** Fabric Git integration, markdown docs, SQL/DAX scripts

## Sample Data & Testing

The `sample-data/` folder contains structure documentation for SAP Accounts Payable data:
- **BKPF**: Document headers (142 documents)
- **BSEG**: Line items (270 items)
- **LFA1**: Vendor master data (50 vendors)

⚠️ **Data files (CSV) are not committed to Git** (best practice). See `sample-data/README.md` for:
- Required data structure
- How to provide your own SAP exports
- Synthetic data generation options

## Getting Started

### Prerequisites
- Microsoft Fabric workspace (Premium capacity or trial)
- Power BI Desktop (latest version)
- Basic knowledge of SQL and DAX

### Quick Start

1. **Clone repository**
   ```bash
   git clone https://github.com/schmisu/fabric-data-analytics.git
   cd fabric-data-analytics
   ```

2. **Provide data**
   - Place SAP export CSV files in `sample-data/` folder
   - Follow structure in `sample-data/README.md`

3. **Set up Fabric workspace**
   - Create new workspace in Fabric
   - Connect to GitHub repo (see `docs/fabric-git-setup.md`)

4. **Run data pipeline**
   - Dataflow ingests CSV to Lakehouse
   - Notebook runs SQL transformations
   - Semantic model connects to fact table

5. **Build reports**
   - Follow specifications in `docs/powerbi_report_design.md`
   - Use pre-built DAX measures from semantic model

See [Architecture Documentation](docs/architecture.md) for detailed setup instructions.

## Project Scope & Stats

**Timeline:** September-October 2024
**Time Investment:** ~40 hours

**Code Statistics:**
- SQL: ~400 lines (transformation logic)
- DAX: ~1,200 lines (40+ measures)
- M (Dataflow): ~150 lines (ingestion)
- Documentation: ~5,000 words

**Platform Patterns Implemented:**
- Two-stage ETL framework
- Data quality monitoring
- Semantic modeling layer
- Self-service analytics
- Git-based version control
- Comprehensive documentation

## Skills Demonstrated

**Platform Engineering:**
- End-to-end data pipeline design
- Architecture decision-making
- Scalability and reusability thinking
- DevOps practices (Git, documentation)

**Data Engineering:**
- SQL transformation patterns (Spark SQL)
- Data quality frameworks
- ETL best practices
- Schema design and modeling

**Analytics Engineering:**
- Semantic layer design (DAX)
- Metric definition and organization
- Self-service enablement
- Report design patterns

**Domain Knowledge:**
- SAP data structures (BKPF, BSEG, LFA1)
- Financial analytics (AP, aging, cash discounts)
- Enterprise data challenges

**Communication:**
- Technical documentation
- Architecture diagrams
- README best practices
- Code comments and organization

## Learnings & Challenges

See [docs/learnings.md](docs/learnings.md) for detailed discussion of:
- What worked well
- Key challenges and solutions
- What I'd do differently
- Future enhancements

**Quick Summary:**
- ✅ Fabric's unified platform simplifies architecture
- ✅ Two-stage SQL transformation improves maintainability
- ✅ Data quality transparency builds stakeholder confidence
- ⚠️ Low-code tools (Dataflow) have limitations for complex logic
- ⚠️ Date format handling from SAP requires robust parsing

## Use Cases for This Repository

### For Recruiters/Hiring Managers:
- Demonstrates **platform engineering thinking**, not just coding
- Shows **end-to-end ownership** from ingestion to visualization
- Proves ability to **document and communicate** technical decisions
- Evidence of **production-ready quality standards**

### For Platform PM Roles:
- Understanding of **data platform architecture**
- **Customer empathy** through hands-on building
- Ability to **identify product gaps and opportunities**
- Knowledge of **developer experience** and user pain points

### For Data Engineers:
- Reference implementation for **lakehouse patterns**
- **Reusable transformation frameworks**
- **Data quality patterns** that can be adapted
- **Best practices** for Fabric development

### For Learning:
- Complete **end-to-end example** to study
- **Decision rationale** documented for each choice
- **Challenges and solutions** explained
- **Code samples** for SQL, DAX, M

## Future Enhancements

**Platform Capabilities:**
- [ ] Incremental refresh pattern (watermark-based)
- [ ] Automated testing framework for SQL transformations
- [ ] CI/CD pipeline for multi-environment deployment
- [ ] Real-time streaming ingestion (Event Streams)
- [ ] Data lineage visualization

**Analytics Features:**
- [ ] Row-level security (multi-company support)
- [ ] Predictive analytics (late payment risk scoring)
- [ ] Anomaly detection on payment patterns
- [ ] Mobile-optimized report layouts
- [ ] Natural language queries (Q&A)

**Data Platform:**
- [ ] Additional data sources (APIs, databases)
- [ ] Medallion architecture (bronze/silver/gold layers)
- [ ] Data catalog integration
- [ ] Cost monitoring and optimization
- [ ] Performance tuning for large-scale data

## Known Limitations

- **Single year data**: Sample data is 2024 only (YoY comparisons return BLANK)
- **Simplified schema**: Production would benefit from normalized star schema with dimension tables
- **Manual refresh**: Automated scheduling requires Fabric Premium capacity
- **Synthetic data**: Sample data is generated, not real transaction data
- **Single source**: Demonstrates CSV ingestion; production would integrate multiple sources

## Contributing & Feedback

This is a portfolio project, but feedback is welcome!

**Ways to engage:**
- Open issues for questions or suggestions
- Fork and adapt for your own use case
- Share feedback on architecture or design choices
- Connect with me on [LinkedIn](https://www.linkedin.com/in/dr-susanne-schmidt/)

## License

This project is open source and available under the [MIT License](LICENSE).

## Contact

**Project by**: Susanne Schmidt
**LinkedIn**: [Dr. Susanne Schmidt](https://www.linkedin.com/in/dr-susanne-schmidt/)
**GitHub**: [@schmisu](https://github.com/schmisu)

---

**Built with Microsoft Fabric** | **Powered by Delta Lake** | **Modern Data Platform**

*Last updated: October 2024*
