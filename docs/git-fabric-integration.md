# Git/Fabric Workspace Integration Guide

## Overview

Microsoft Fabric supports Git integration for source control of workspace items. Here are your options for integrating this development repo with Fabric workspaces.

## Integration Options

### Option 1: Two-Repository Approach (Recommended)

**Development Repo (This One)**: `fabric-data-analytics`
- Documentation and guides
- Sample data and validation scripts
- Development notes and templates
- Manual export/import artifacts

**Fabric Workspace Repo**: Auto-created by Fabric
- Dataflows (M code and JSON definitions)
- Notebooks (Python/Spark code)
- Semantic models (model.bim files)
- Reports (Power BI report definitions)

**Workflow:**
1. Develop and document in this repo
2. Create items manually in Fabric workspace
3. Connect Fabric workspace to a NEW Git repo
4. Fabric automatically syncs workspace items to the new repo
5. Keep this repo for documentation and development reference

### Option 2: Single Repository Approach

Connect this existing repo directly to Fabric workspace:
- Fabric items would be added to `fabric-items/` folder
- All development and production code in one place
- More complex to manage mixed content

## Recommended Setup Process

### Phase 1: Development (Current)
1. Complete dataflow setup and document in this repo
2. Build lakehouse, notebooks, semantic model manually
3. Create Power BI reports
4. Document everything in `docs/` folder

### Phase 2: Fabric Git Integration
1. Create new empty repo: `fabric-data-analytics-workspace`
2. In Fabric workspace settings, connect to the new repo
3. Fabric auto-syncs all workspace items to new repo
4. Keep this repo for documentation and templates
5. Use the Fabric-synced repo for production deployments

## Fabric Git Integration Features

When you connect a Fabric workspace to Git:
- **Auto-sync**: Fabric items automatically sync to Git
- **Version control**: Track changes to dataflows, notebooks, etc.
- **Branch support**: Create branches for different environments
- **Deployment**: Deploy from Git to different workspaces
- **Collaboration**: Multiple developers can work on same workspace

## File Structure in Fabric Git Repo

Fabric automatically creates this structure:
```
fabric-workspace-repo/
├── Dataflows/
│   └── SAP_AP_Ingestion.DataFlow/
│       ├── dataflow.json
│       └── queries/
├── Lakehouses/
│   └── SAP_Analytics.Lakehouse/
├── Notebooks/
│   └── SAP_Data_Processing.Notebook/
├── SemanticModels/
│   └── SAP_AP_Model.SemanticModel/
└── Reports/
    └── SAP_AP_Dashboard.Report/
```

## Next Steps

1. Finish development in this repo first
2. Once everything works, decide on integration approach
3. Set up Fabric Git connection for production use
4. Keep this repo as the "template" and documentation source