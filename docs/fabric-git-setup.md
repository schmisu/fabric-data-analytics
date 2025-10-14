# Fabric Git Integration Setup Guide

This guide walks you through connecting your Microsoft Fabric workspace to this GitHub repository.

## Prerequisites

- ✅ Microsoft Fabric workspace created
- ✅ Workspace enabled as Template App (optional but recommended)
- ✅ GitHub repository with main branch ready
- ✅ Fabric workspace items manually created:
  - Dataflow Gen2
  - Lakehouse
  - Notebook(s)
  - Semantic Model
  - Power BI Report
  - Pipeline (optional)

## Step 1: Push Local Changes to GitHub

First, push your prepared main branch to GitHub:

```bash
# Make sure you're on main branch
git branch

# Push to GitHub
git push origin main

# Optional: Also push feature branch for history
git push origin feature/sap-sample-data
```

## Step 2: Connect Fabric Workspace to Git

### In Microsoft Fabric:

1. **Open your workspace** in Fabric
2. Click **Workspace settings** (gear icon)
3. Select **Git integration** from the left menu
4. Click **Connect**

### Configure Git Connection:

**Connection Details:**
- **Git provider**: GitHub
- **Organization/Account**: Your GitHub username
- **Repository**: `fabric-data-analytics`
- **Branch**: `main`
- **Folder**: Leave empty (root) or specify a subfolder

**Authentication:**
- You'll be prompted to authenticate with GitHub
- Grant Fabric access to your repository
- Choose the appropriate permissions

## Step 3: Initial Sync (Fabric → Git)

After connecting:

1. Fabric will show **uncommitted changes** for all your workspace items
2. Review the changes - these are your manually created items
3. Add a commit message:
   ```
   Initial sync: Add Fabric workspace items

   - Dataflow: SAP AP data ingestion
   - Lakehouse: SapDataLakehouse
   - Notebook: AP transformation
   - Semantic Model: AP Analytics
   - Report: AP Dashboard
   ```
4. Click **Commit**

Fabric will create folders like:
```
YourDataflow.DataFlow/
YourLakehouse.Lakehouse/
YourNotebook.Notebook/
YourSemanticModel.SemanticModel/
YourReport.Report/
```

## Step 4: Pull to Local Repository

After Fabric commits, pull the changes locally:

```bash
git pull origin main
```

You should now see Fabric-generated folders alongside your documentation.

## Step 5: Verify Final Structure

Your repository should now look like:

```
fabric-data-analytics/
├── README.md                           # Your documentation
├── docs/                               # Your guides
├── sql/                                # Your SQL code
├── dax/                                # Your DAX measures
├── sample-data/                        # Your sample data
│
└── [Fabric Items - Auto-generated]
    ├── SapDataIngestion.DataFlow/
    ├── SapDataLakehouse.Lakehouse/
    ├── APTransformation.Notebook/
    ├── APAnalytics.SemanticModel/
    └── APDashboard.Report/
```

## Step 6: Update README (Optional)

After syncing, you may want to update your README to reference actual Fabric item names:

```bash
# Edit README.md to add actual item names
# Commit and push
git add README.md
git commit -m "Update README with actual Fabric item names"
git push origin main
```

## How Git Integration Works

### Workspace → Git (Commit)
When you make changes in Fabric:
1. Changes appear as "uncommitted" in workspace
2. You review and commit from Fabric UI
3. Fabric pushes to your GitHub branch

### Git → Workspace (Update)
When you make changes in Git:
1. Changes appear as "updates available" in workspace
2. You review and pull from Fabric UI
3. Fabric updates your workspace items

## Best Practices

### ✅ DO:
- Use Git integration for **final/production** deployments
- Commit meaningful changes with good messages
- Keep documentation in sync with Fabric items
- Use branches for major changes (if needed)

### ❌ DON'T:
- Don't use Git integration for active development (too slow)
- Don't manually edit Fabric-generated files (will be overwritten)
- Don't commit directly to main via Git (use Fabric UI)

## Workflow for Future Changes

### Making Changes:

1. **Develop in Fabric** (make changes to dataflow, notebook, etc.)
2. **Test thoroughly** in workspace
3. **Commit via Fabric UI** with meaningful message
4. **Pull locally** to keep documentation in sync
5. **Update documentation** if needed (in Git)
6. **Push documentation updates** to GitHub

### Documentation-Only Changes:

1. **Edit locally** (README, docs, SQL, DAX)
2. **Commit and push** to GitHub
3. **Update from Fabric UI** (optional, if you want to pull)

## Troubleshooting

### Issue: "No changes to commit" in Fabric
**Solution**: Make sure you've actually changed something in a Fabric item

### Issue: Conflicts when pulling from Git
**Solution**: Resolve conflicts in GitHub first, or use Fabric's conflict resolution UI

### Issue: Fabric items not syncing
**Solution**: Check that Git integration is still connected (Workspace Settings → Git integration)

### Issue: Can't push from local Git
**Solution**: Fabric owns the workspace items. Only commit documentation changes locally.

## Template App Deployment

If your workspace is enabled as a Template App:

1. **Prepare workspace** with sample data and tested items
2. **Git sync** ensures version control
3. **Create template app** via Fabric UI (separate process)
4. **Package and publish** to AppSource or private distribution

## Security Considerations

### Public Repository:
- ✅ Documentation, SQL, DAX (safe to share)
- ✅ Sample data (synthetic/anonymized)
- ❌ Connection strings or credentials (never commit!)
- ❌ Real business data

### Private Repository:
- More flexibility, but still avoid credentials
- Use environment variables or Fabric parameters

## Next Steps

After Git integration is complete:

1. ✅ Update your LinkedIn/resume with GitHub link
2. ✅ Add project to portfolio with README screenshots
3. ✅ Optional: Record a demo video walkthrough
4. ✅ Optional: Write a blog post about the architecture

---

## Quick Reference Commands

```bash
# Check current branch
git branch

# Check status
git status

# Pull latest from GitHub
git pull origin main

# Push documentation changes
git add docs/
git commit -m "Update documentation"
git push origin main

# View commit history
git log --oneline --graph

# Check what Fabric committed
git log --author="Azure DevOps"
```

---

**Last Updated**: October 2025
**Questions?** Check Fabric Git integration docs at Microsoft Learn
