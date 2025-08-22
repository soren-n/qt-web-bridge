# PyPI Trusted Publishing Setup

This document outlines the steps to configure PyPI Trusted Publishing for secure, tokenless deployment.

## Prerequisites

1. **GitHub Repository**: Ensure your repository is public or part of GitHub Pro/Team
2. **PyPI Account**: Create accounts on both [PyPI](https://pypi.org) and [TestPyPI](https://test.pypi.org)

## Step 1: Configure Trusted Publishing on PyPI

### For TestPyPI (Development Testing)
1. Go to [TestPyPI Trusted Publishers](https://test.pypi.org/manage/account/publishing/)
2. Add a new trusted publisher with these settings:
   - **PyPI Project Name**: `soren-n-qt-web-bridge`
   - **Owner**: `soren-n`
   - **Repository name**: `qt-web-bridge`
   - **Workflow filename**: `publish.yml`
   - **Environment name**: `testpypi`

### For Production PyPI
1. Go to [PyPI Trusted Publishers](https://pypi.org/manage/account/publishing/)
2. Add a new trusted publisher with these settings:
   - **PyPI Project Name**: `soren-n-qt-web-bridge`
   - **Owner**: `soren-n`
   - **Repository name**: `qt-web-bridge`
   - **Workflow filename**: `publish.yml`
   - **Environment name**: `pypi`

## Step 2: Configure GitHub Environments

### Create TestPyPI Environment
1. Go to your GitHub repository → Settings → Environments
2. Click "New environment"
3. Name: `testpypi`
4. Add environment protection rules:
   - ☑️ Required reviewers: Add yourself
   - ☑️ Restrict pushes to protected branches

### Create PyPI Environment
1. Create another environment named: `pypi`
2. Add environment protection rules:
   - ☑️ Required reviewers: Add yourself (mandatory for production)
   - ☑️ Restrict pushes to protected branches
   - ☑️ Deployment branches: Only protected branches

## Step 3: Update Project Configuration

Update your `pyproject.toml` with correct repository URLs:

```toml
[project.urls]
Homepage = "https://github.com/soren-n/qt-web-bridge"
Repository = "https://github.com/soren-n/qt-web-bridge.git"
Issues = "https://github.com/soren-n/qt-web-bridge/issues"
```

## Step 4: Test the Publishing Pipeline

### Test with a Pre-release Version
1. Update version in `pyproject.toml` to `0.1.0a1` (alpha release)
2. Create and push a tag:
   ```bash
   git tag v0.1.0a1
   git push origin v0.1.0a1
   ```
3. Monitor the GitHub Actions workflow
4. Verify package appears on TestPyPI first
5. Approve the PyPI deployment when ready

### Production Release Process
1. Update version in `pyproject.toml` to stable version (e.g., `0.1.0`)
2. Create and push a tag:
   ```bash
   git tag v0.1.0
   git push origin v0.1.0
   ```
3. Approve the TestPyPI deployment
4. Approve the PyPI deployment after TestPyPI success

## Security Benefits

- ✅ **No Long-lived Tokens**: OIDC tokens expire in 15 minutes
- ✅ **Repository-Specific**: Tokens only work for your specific repo
- ✅ **Environment Controls**: Manual approval required for production
- ✅ **Audit Trail**: All deployments tracked in GitHub Actions
- ✅ **Automatic Attestations**: PEP 740 attestations generated automatically

## Troubleshooting

### Common Issues
1. **"Trusted publishing not configured"**: Verify PyPI trusted publisher settings match exactly
2. **"Environment protection rules"**: Ensure environments are configured in GitHub
3. **"Workflow not found"**: Check workflow filename matches exactly in PyPI config

### Verification Commands
```bash
# Check if package uploaded successfully
pip install --index-url https://test.pypi.org/simple/ soren-n-qt-web-bridge

# Install from production PyPI
pip install soren-n-qt-web-bridge
```

## Next Steps

1. Set up branch protection rules for `main` branch
2. Configure tag protection rules for `v*` pattern
3. Consider setting up GitHub security advisories
4. Review and update the security policy