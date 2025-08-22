# Read the Docs Setup Instructions

This document provides step-by-step instructions for setting up Qt Web Bridge documentation on Read the Docs.

## Prerequisites

1. **GitHub Repository**: Ensure your repository is available at `https://github.com/soren-n/qt-web-bridge`
2. **Read the Docs Account**: Create an account at [readthedocs.org](https://readthedocs.org)

## Step 1: Connect GitHub Account

1. Go to [Read the Docs](https://readthedocs.org/) and sign in
2. Click your username in the top-right corner → **Settings**
3. Go to **Connected Services** → **GitHub**
4. Click **Connect to GitHub** and authorize Read the Docs

## Step 2: Import Project

1. From your dashboard, click **Import a Project**
2. Find `soren-n/qt-web-bridge` in the list (may need to refresh repositories)
3. Click **+** to import the project
4. Configure the project:
   - **Name**: `qt-web-bridge`
   - **Repository URL**: `https://github.com/soren-n/qt-web-bridge`
   - **Description**: Clean Qt WebView widgets for hosting modern web UIs without styling conflicts
   - **Project Homepage**: `https://github.com/soren-n/qt-web-bridge`
   - **Language**: English
   - **Programming Language**: Python
   - **Repository Type**: Git

## Step 3: Configure Project Settings

### Basic Settings
1. Go to **Admin** → **Settings**
2. Set **Documentation Type**: Sphinx Html
3. Set **Default Version**: `latest`
4. Enable **Build pull requests for this project**

### Advanced Settings  
1. Go to **Admin** → **Advanced Settings**
2. Set **Python Interpreter**: CPython 3.x
3. Enable **Use system packages**
4. Set **Python Configuration File**: (leave empty to use `.readthedocs.yaml`)

## Step 4: Environment Variables (Optional)

If needed, you can set environment variables in **Admin** → **Environment Variables**:
- No special environment variables are required for this project

## Step 5: Build Documentation

1. Go to **Builds** tab
2. Click **Build Version: latest**
3. Monitor the build process - it should complete successfully

## Step 6: Configure Domain (Optional)

The documentation will be available at:
- **Primary URL**: `https://qt-web-bridge.readthedocs.io/`
- **Alternative**: `https://qt-web-bridge.readthedocs.io/en/latest/`

To use a custom domain:
1. Go to **Admin** → **Domains**
2. Add your custom domain
3. Configure DNS CNAME record

## Step 7: Webhooks (Automatic)

Read the Docs automatically configures webhooks for GitHub repositories. Verify:
1. Go to your GitHub repository → **Settings** → **Webhooks**
2. You should see a webhook for `https://readthedocs.org/api/v2/webhook/...`

## Build Configuration

The project uses `.readthedocs.yaml` configuration file with:

### Build Environment
- **OS**: Ubuntu 24.04
- **Python**: 3.12
- **Tools**: uv for dependency management

### Documentation
- **Format**: Sphinx with Furo theme
- **API Documentation**: Auto-generated with sphinx-autoapi
- **Output Formats**: HTML, PDF, ePub

### Dependencies
Defined in `docs/requirements.txt`:
- sphinx>=8.2.3
- furo (modern theme)
- sphinx-autoapi (auto API docs)
- myst-parser (Markdown support)
- Various Sphinx extensions

## Troubleshooting

### Common Build Issues

**"No module named 'qt_web_bridge'"**
- Ensure the project is installed with `pip install -e .` in the build
- Check that `src/qt_web_bridge` is properly structured

**"linkify not installed"**
- Ensure `linkify-it-py` is in docs/requirements.txt
- This dependency is required for MyST parser

**Build timeout**
- Documentation builds should complete in 2-3 minutes
- Contact Read the Docs support if builds consistently timeout

### Build Logs
Access build logs via:
1. **Builds** tab in Read the Docs dashboard
2. Click on any build to see detailed logs
3. Check both **Raw Log** and **HTML** tabs

### Local Testing
Test documentation builds locally:
```bash
cd docs/
pip install -r requirements.txt
sphinx-build -b html . _build/html
```

## Maintenance

### Updating Documentation
- Documentation rebuilds automatically on git pushes to main branch
- Manual builds can be triggered from Read the Docs dashboard
- Pull request builds preview changes before merging

### Version Management
- `latest` version tracks the main branch
- Tagged releases create versioned documentation
- Configure version settings in **Admin** → **Versions**

### Monitoring
- Enable email notifications in **Admin** → **Notifications**
- Monitor build status and reader analytics in dashboard

## Support Resources

- [Read the Docs Documentation](https://docs.readthedocs.io/)
- [Sphinx Documentation](https://www.sphinx-doc.org/)
- [GitHub Issues](https://github.com/soren-n/qt-web-bridge/issues) for project-specific problems