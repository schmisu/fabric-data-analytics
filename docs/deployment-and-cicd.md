# Deployment Strategies & CI/CD Patterns

This document demonstrates understanding of deployment automation and CI/CD patterns for data platforms, tailored for portfolio/demonstration purposes.

> **Portfolio Context:** This project uses a simplified deployment approach suitable for demonstration. Production implementations would extend these patterns with automated testing, approval gates, and monitoring.

---

## Current Setup: Git Feature Branch Workflow

This portfolio project uses a **feature branch workflow** for development:

### Git Branch Strategy

```
main branch (stable, production-ready)
    ├── feature/sap-authentic-structure (current enhancement)
    └── future features...
```

**Workflow:**
1. **Main branch** = Stable, working solution (protected)
2. **Feature branches** = Active development (isolated changes)
3. **Testing** = Validate in Fabric workspace before merging
4. **Merge** = Only merge to main after successful testing

**Why This Approach:**
- ✅ Demonstrates professional Git workflow for job applications
- ✅ Main branch always contains working code
- ✅ Can show feature development in isolation
- ✅ Single workspace sufficient for portfolio (cost-effective)

### Template App vs Multi-Environment

**Template App Workspace Configuration:**

This workspace is configured as a **Template App**, which enables:
- Packaging the entire solution for distribution
- Parameterized configurations for different environments
- Easy deployment to new workspaces
- Version control through Git integration

**Important Distinction:**
- **Template App** ≠ Dev/Prod separation
- **Template App** = Distribution mechanism for deploying to other organizations
- **Multi-Environment** = Separate workspaces (Dev/Test/Prod) for deployment pipeline

### What is a Template App?

A Template App in Fabric allows you to:
1. **Package** your workspace items (dataflows, notebooks, semantic models, reports, pipelines)
2. **Parameterize** connection strings and environment-specific settings
3. **Distribute** the packaged solution to other workspaces or organizations
4. **Update** deployed instances when you publish new versions

**Use Cases:**
- Multi-tenant SaaS platforms
- Deploying to multiple regions/environments
- Customer installations
- Internal templates for standardization

---

## Deployment Pattern Overview

### Lightweight CI/CD for Portfolio Projects

For demonstration purposes, this project uses a **simplified deployment pattern**:

```
Local Development
    ↓
Git Repository (GitHub)
    ↓
Fabric Workspace (Manual Sync)
    ↓
Template App (Optional Distribution)
```

**Key Features Demonstrated:**
1. **Version Control:** All code (SQL, DAX, M) in Git
2. **Parameterization:** Environment-agnostic dataflows
3. **Orchestration:** Pipeline automates end-to-end refresh
4. **Documentation:** Clear setup and deployment instructions

---

## Parameterization Strategy

### Dataflow Parameters

**Purpose:** Make solution environment-independent

**Example Parameters:**
- `SharePointSite`: URL of SharePoint site
- `FolderPath`: Path to CSV files
- `Environment`: "dev" or "prod"

**Configuration:**
```m
// Dataflow parameter definition
SharePointSite = "https://company.sharepoint.com/sites/dev" meta [IsParameterQuery=true, Type="Text"]

// Usage in query
Source = SharePoint.Files(SharePointSite, [ApiVersion = 15])
```

**Pipeline Integration:**
- ✅ Enable "Make parameters available to pipeline" in Dataflow settings
- Pipeline can override parameters for different environments
- Same dataflow code works in dev/test/prod

### Why Parameterization Matters

**For Platform Engineering:**
- Demonstrates environment-agnostic design thinking
- Shows understanding of configuration management
- Enables true CI/CD (same code, different configs)

**For Job Applications:**
- Proves you understand production deployment challenges
- Shows ability to design reusable, scalable solutions
- Demonstrates professional software engineering practices

---

## Production-Grade CI/CD (Conceptual)

While this portfolio uses manual Git sync, here's what a **production CI/CD pipeline** would look like:

### Multi-Environment Setup

```
┌─────────────────┐
│  Developer      │
│  Local Changes  │
└────────┬────────┘
         │
         ▼
    ┌────────┐
    │  Git   │ ← Feature branch
    │ Commit │
    └───┬────┘
        │
        ▼
┌───────────────────┐
│  Pull Request     │ ← Code review
│  + Automated Tests│
└────────┬──────────┘
         │
         ▼ (Merge to main)
┌──────────────────────┐
│  Dev Workspace       │ ← Auto-deploy
│  Fabric APIs         │
│  - Dataflow refresh  │
│  - Run pipeline      │
│  - Test semantic model│
└───────┬──────────────┘
        │
        ▼ (Manual approval)
┌──────────────────────┐
│  Test Workspace      │ ← Staged deployment
│  QA Validation       │
└───────┬──────────────┘
        │
        ▼ (Release gate)
┌──────────────────────┐
│  Prod Workspace      │ ← Production
│  Monitored refresh   │
└──────────────────────┘
```

### Automation Tools

**Option 1: Azure DevOps**
```yaml
# azure-pipelines.yml
trigger:
  branches:
    include:
      - main

pool:
  vmImage: 'ubuntu-latest'

stages:
  - stage: Deploy_Dev
    jobs:
      - job: Fabric_Deployment
        steps:
          - task: AzureCLI@2
            inputs:
              script: |
                # Authenticate with Fabric
                az login --service-principal

                # Update Fabric workspace items via REST API
                curl -X POST https://api.fabric.microsoft.com/v1/workspaces/... \
                     -H "Authorization: Bearer $TOKEN" \
                     -d @dataflow-definition.json

                # Trigger pipeline refresh
                curl -X POST https://api.fabric.microsoft.com/v1/pipelines/.../run

  - stage: Run_Tests
    dependsOn: Deploy_Dev
    jobs:
      - job: Data_Quality_Tests
        steps:
          - script: |
              python tests/test_data_quality.py

  - stage: Deploy_Prod
    dependsOn: Run_Tests
    condition: and(succeeded(), eq(variables['Build.SourceBranch'], 'refs/heads/main'))
    jobs:
      - deployment: Production
        environment: 'Prod'
        strategy:
          runOnce:
            deploy:
              steps:
                - # Prod deployment steps
```

**Option 2: GitHub Actions**
```yaml
# .github/workflows/deploy.yml
name: Deploy to Fabric

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  deploy-dev:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Deploy to Dev Workspace
        env:
          FABRIC_TOKEN: ${{ secrets.FABRIC_TOKEN }}
        run: |
          # Use Fabric REST APIs to update workspace
          python scripts/deploy_to_fabric.py --env dev

      - name: Run Pipeline
        run: |
          python scripts/trigger_pipeline.py --workspace dev

  test:
    needs: deploy-dev
    runs-on: ubuntu-latest
    steps:
      - name: Run Data Quality Tests
        run: |
          pytest tests/

  deploy-prod:
    needs: test
    if: github.ref == 'refs/heads/main'
    runs-on: ubuntu-latest
    environment: production
    steps:
      - name: Deploy to Production
        run: |
          python scripts/deploy_to_fabric.py --env prod
```

---

## Testing Strategy (Production)

### Automated Tests

**Data Quality Tests:**
```python
# tests/test_data_quality.py
import pandas as pd
from fabric_client import FabricClient

def test_no_duplicate_documents():
    """Ensure no duplicate document numbers in fact table"""
    client = FabricClient()
    df = client.query_lakehouse("SELECT document_number, COUNT(*) as cnt FROM accounts_payable_fact GROUP BY document_number HAVING cnt > 1")
    assert len(df) == 0, "Duplicate documents found"

def test_document_balance():
    """Verify debits equal credits for each document"""
    df = client.query_lakehouse("""
        SELECT document_number, ABS(SUM(signed_amount)) as balance
        FROM accounts_payable_fact
        GROUP BY document_number
        HAVING ABS(SUM(signed_amount)) > 0.01
    """)
    assert len(df) == 0, f"Unbalanced documents found: {df}"

def test_date_completeness():
    """Check posting_date is populated for all records"""
    df = client.query_lakehouse("SELECT COUNT(*) FROM accounts_payable_fact WHERE posting_date IS NULL")
    assert df.iloc[0,0] == 0, "Missing posting dates found"
```

**Semantic Model Tests:**
```python
# tests/test_semantic_model.py
def test_measure_calculations():
    """Verify DAX measures return expected values"""
    client = FabricClient()

    # Test Total Invoice Amount
    result = client.execute_dax("EVALUATE {[Total Invoice Amount]}")
    assert result > 0, "Total Invoice Amount should be positive"

    # Test YoY Growth (with 2023-2024 data)
    result = client.execute_dax("EVALUATE {[YoY Growth %]}")
    assert result is not None, "YoY Growth should return a value"
```

---

## Deployment Checklist

### For This Portfolio Project

**Current Automated:**
- ✅ Git version control (manual sync)
- ✅ Parameterized dataflows
- ✅ Orchestrated pipeline (Dataflow → Notebook → Semantic Model Refresh)
- ✅ Documentation as code

**What Would Be Added for Production:**
- [ ] Automated deployment via CI/CD tool
- [ ] Multi-environment workspaces (Dev/Test/Prod)
- [ ] Automated testing (data quality, measure validation)
- [ ] Approval gates for production
- [ ] Rollback procedures
- [ ] Monitoring and alerting

### Template App Distribution (Optional)

**If distributing as Template App:**

1. **Prepare Workspace**
   - Ensure all items are parameterized
   - Test with different parameter values
   - Document parameter requirements

2. **Create Template App**
   - Fabric Portal → Workspace → "Create Template App"
   - Configure parameters (SharePointSite, Environment, etc.)
   - Set version number

3. **Test Installation**
   - Install to test workspace
   - Verify parameters can be overridden
   - Check all items deploy correctly

4. **Publish**
   - Submit to AppSource (if public)
   - Or share install link privately

---

## Platform Engineering Perspective

### Why This Matters for Job Applications

**Demonstrates:**
1. **DevOps Mindset:** Understanding of deployment automation
2. **Environment Management:** Ability to design for dev/test/prod
3. **Configuration Management:** Parameterization vs hard-coding
4. **Quality Assurance:** Testing strategies for data platforms
5. **Production Readiness:** Thinking beyond "it works on my machine"

### Conversation Points for Interviews

**For Platform PM Roles:**
> "While this portfolio uses manual Git sync for simplicity, I've designed it with CI/CD in mind - parameterized dataflows, orchestrated pipeline, and version-controlled code. In production, I'd extend this with Azure DevOps or GitHub Actions to automate deployment across dev/test/prod environments, plus automated data quality tests."

**For Data Platform Roles:**
> "The orchestration pipeline demonstrates end-to-end automation: dataflow ingestion → SQL transformation → semantic model refresh. Parameters make it environment-agnostic. This pattern scales to production with automated testing and multi-environment deployment pipelines."

**For Fabric PM Roles:**
> "I've experienced Fabric's Git integration and Template App features hands-on. The parameter exposure issue I solved (dataflow settings → enable pipeline access) is a great example of product UX that could be improved - why shouldn't this be default behavior?"

---

## Quick Reference: Fabric Git Integration

### Current Workflow

**Push Changes:**
1. Make changes in Fabric workspace (notebooks, dataflows, etc.)
2. Workspace shows "uncommitted changes"
3. Click "Source control" → "Commit"
4. Enter commit message
5. Changes pushed to GitHub

**Pull Changes:**
1. Make changes in Git (documentation, SQL scripts)
2. Push to GitHub
3. Workspace shows "updates available"
4. Click "Source control" → "Update"
5. Fabric pulls changes

### Limitations (As of Oct 2024)

- ⚠️ Cannot push from local Git to Fabric (one-way from workspace)
- ⚠️ Sync delays make active development slow
- ⚠️ Must commit from Fabric UI manually
- ✅ Great for final deployments and version history

**Recommendation:** Use for deployment checkpoints, not active development.

---

## Future Enhancements

**For Full Production Implementation:**

1. **Automated Deployment Pipeline**
   - GitHub Actions or Azure DevOps
   - Fabric REST API integration
   - Environment-specific configs

2. **Testing Framework**
   - Python-based data quality tests
   - DAX measure validation
   - End-to-end pipeline tests

3. **Monitoring & Alerting**
   - Pipeline success/failure notifications
   - Data quality threshold alerts
   - Performance degradation detection

4. **Multi-Workspace Strategy**
   - Separate Dev/Test/Prod workspaces
   - Promotion process with approvals
   - Rollback procedures

5. **Documentation Automation**
   - Auto-generate data dictionary
   - Measure documentation from DAX comments
   - Deployment runbooks

---

## Summary

**This Portfolio Demonstrates:**
- ✅ Understanding of deployment patterns
- ✅ Parameterization for environment flexibility
- ✅ Orchestration automation
- ✅ Version control best practices
- ✅ Template App readiness (workspace configured)

**Production Extensions:**
- CI/CD automation (Azure DevOps/GitHub Actions)
- Automated testing framework
- Multi-environment promotion
- Monitoring and alerting

**Key Takeaway:** Even in a portfolio context, demonstrating deployment thinking shows platform engineering maturity and readiness for production challenges.

---

**Version:** 1.0
**Last Updated:** October 2024
**Author:** Susanne Schmidt
**Purpose:** Portfolio demonstration of CI/CD understanding
