# Git Hooks Setup Guide

This project uses pre-commit hooks to automatically run code quality checks before each commit.

**Requirements**: Python 3.11+

## Quick Setup

1. **Install development dependencies:**
   ```bash
   pip install -e ".[dev]"
   ```

2. **Run the setup script:**
   ```bash
   python scripts/setup-hooks.py
   ```

3. **Test the hooks:**
   ```bash
   python scripts/test-hooks.py
   ```

## What Gets Checked

The pre-commit hooks will automatically run these checks before each commit:

### Ruff (Linting & Formatting)
- **Linting**: Checks for code style issues, unused imports, etc.
- **Formatting**: Automatically formats code to consistent style
- **Import Sorting**: Organizes imports in the standard order

### MyPy (Type Checking)  
- Run manually with `mypy src/` (not in pre-commit due to Qt import issues)
- Validates type annotations and ensures type safety

### File Quality Checks
- Removes trailing whitespace
- Ensures files end with newline
- Validates YAML, TOML, and JSON syntax
- Checks for merge conflicts and debug statements
- Prevents large files from being committed

### Pytest (Optional)
- Test suite runs only when explicitly triggered
- Use: `pre-commit run pytest --hook-stage manual`

## Hook Behavior

### Automatic Fixes
Some hooks will automatically fix issues:
- Ruff formatting
- Trailing whitespace removal
- Missing final newlines

When this happens:
1. The commit will be stopped
2. Files will be modified with fixes
3. You need to stage the changes and commit again

### Failed Checks
If hooks find unfixable issues:
1. The commit will be prevented
2. Error messages will show what needs fixing
3. Fix the issues manually and commit again

## Manual Commands

```bash
# Run all hooks on all files
pre-commit run --all-files

# Run specific hooks
pre-commit run ruff           # Only linting/formatting
pre-commit run mypy           # Only type checking
pre-commit run trailing-whitespace  # Only whitespace

# Run tests manually
pre-commit run pytest --hook-stage manual

# Skip hooks for emergency commits (not recommended)
git commit --no-verify -m "emergency fix"

# Update hook versions
pre-commit autoupdate
```

## Configuration Files

- **`.pre-commit-config.yaml`**: Hook configuration and versions
- **`pyproject.toml`**: Tool settings (ruff, mypy, pytest)
- **`setup-hooks.py`**: Automated setup script
- **`test-hooks.py`**: Hook testing script

## Troubleshooting

### "pre-commit command not found"
```bash
pip install pre-commit>=3.0.0
```

### MyPy import errors
Make sure QtPy is available in your environment:
```bash
pip install qtpy>=2.0.0
```

### Hooks are too slow
You can disable specific hooks by editing `.pre-commit-config.yaml` or skip them:
```bash
SKIP=mypy git commit -m "skip mypy for this commit"
```

### Clear hook cache
If hooks behave unexpectedly:
```bash
pre-commit clean
pre-commit install --install-hooks
```

## Customization

### Adding New Hooks
Edit `.pre-commit-config.yaml` to add new repositories or hooks.

### Modifying Tool Settings
Edit `pyproject.toml` to change ruff, mypy, or pytest configuration.

### Disabling Hooks
To disable a hook, comment it out in `.pre-commit-config.yaml` or remove it entirely.

## Best Practices

1. **Run hooks locally** before pushing to catch issues early
2. **Keep hooks updated** with `pre-commit autoupdate`
3. **Fix issues promptly** rather than committing with `--no-verify`
4. **Test changes** with `python test-hooks.py` after modifying configuration

The hooks help maintain code quality and consistency across the project, making collaboration easier and reducing bugs in production.