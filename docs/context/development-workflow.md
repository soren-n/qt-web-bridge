# Development Workflow and Tools

## Development Environment Setup

### Prerequisites
- **Python**: 3.11+ (recommended: 3.12)
- **Qt Implementation**: PySide6, PyQt6, PySide2, or PyQt5
- **Git**: For version control
- **IDE**: VS Code, PyCharm, or similar with Python support

### Project Setup
```bash
# Clone repository
git clone <repository-url>
cd qt-webview-bridge

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Install development dependencies
pip install -e ".[dev]"

# Install examples dependencies (optional)
pip install -e ".[examples]"
```

### Development Dependencies
```toml
[project.optional-dependencies]
dev = [
    "pytest>=7.0",          # Testing framework
    "pytest-qt>=4.0",       # Qt testing support  
    "black>=22.0",          # Code formatting (being replaced by ruff)
    "ruff>=0.1.0",          # Linting, formatting, import sorting
    "mypy>=1.0",            # Type checking
    "PySide6>=6.0",         # Qt implementation for development
]
```

## Development Tools Configuration

### Ruff Configuration (`pyproject.toml`)
```toml
[tool.ruff]
line-length = 88
target-version = "py311"

[tool.ruff.lint]
select = [
    "E",   # pycodestyle errors
    "W",   # pycodestyle warnings  
    "F",   # pyflakes
    "I",   # isort
    "B",   # flake8-bugbear
    "C4",  # flake8-comprehensions
    "UP",  # pyupgrade
]
ignore = [
    "E501",  # line too long (handled by formatter)
]

[tool.ruff.lint.per-file-ignores]
"tests/*" = ["B011"]  # allow assert False in tests
```

### MyPy Configuration (`pyproject.toml`)
```toml
[tool.mypy]
python_version = "3.11"
warn_return_any = true
warn_unused_configs = true
disallow_untyped_defs = true
check_untyped_defs = true

[[tool.mypy.overrides]]
module = "qtpy.*"
ignore_missing_imports = true
```

### Pytest Configuration (`pyproject.toml`)
```toml
[tool.pytest.ini_options]
testpaths = ["tests"]
addopts = "-v --tb=short"
qt_api = "pyside6"
```

## Development Workflow

### Daily Development Cycle
1. **Activate Environment**: `source venv/bin/activate` (or Windows equivalent)
2. **Pull Latest Changes**: `git pull origin main`
3. **Run Tests**: `pytest` (ensure clean baseline)
4. **Develop Features**: Edit code, add tests
5. **Format and Lint**: `ruff check . && ruff format .`
6. **Type Check**: `mypy src/`
7. **Test Changes**: `pytest`
8. **Commit**: Follow commit message conventions

### Code Quality Checklist
Before committing any code, ensure:
- [ ] `ruff check .` passes without errors
- [ ] `ruff format .` applied (or code is properly formatted)  
- [ ] `mypy src/` passes type checking
- [ ] `pytest` passes all tests
- [ ] New features have corresponding tests
- [ ] Documentation updated if public API changes

### Automated Quality Checks
```bash
# Run all quality checks in sequence
check_quality() {
    echo "Running ruff check..."
    ruff check . || exit 1
    
    echo "Running ruff format check..."
    ruff format --check . || exit 1
    
    echo "Running mypy..."
    mypy src/ || exit 1
    
    echo "Running pytest..."
    pytest || exit 1
    
    echo "All checks passed!"
}
```

## Testing Strategy

### Test Organization
```
tests/
├── __init__.py
├── test_webview.py        # BridgedWebView functionality
├── test_bridge.py         # Bridge communication
├── test_utils.py          # Utility functions
├── test_panel.py          # WebViewPanel wrapper
└── test_integration.py    # Full integration tests
```

### Testing Patterns

#### Widget Testing with pytest-qt
```python
import pytest
from qtpy.QtWidgets import QApplication
from qt_webview_bridge import BridgedWebView

@pytest.fixture
def app():
    """Create QApplication for tests."""
    return QApplication.instance() or QApplication([])

def test_webview_creation(qtbot, app):
    """Test WebView widget creation."""
    webview = BridgedWebView()
    qtbot.addWidget(webview)
    
    assert webview is not None
    assert webview.web_view is not None
```

#### Bridge Testing
```python
def test_bridge_json_communication():
    """Test JSON serialization in bridges."""
    bridge = DataBridge()
    
    # Test data setting
    items = [{"id": "1", "name": "Test Item"}]
    bridge.set_items(items)
    
    # Test retrieval
    result = bridge.get_all_items()
    parsed = json.loads(result)
    
    assert len(parsed) == 1
    assert parsed[0]["name"] == "Test Item"
```

#### Integration Testing
```python
def test_full_webview_bridge_integration(qtbot, app):
    """Test complete WebView + Bridge integration."""
    webview = BridgedWebView()
    bridge = DataBridge()
    
    qtbot.addWidget(webview)
    webview.register_bridge_object("data", bridge)
    
    # Test bridge registration
    assert webview.get_bridge_object("data") is bridge
```

### Test Execution
```bash
# Run all tests
pytest

# Run specific test file
pytest tests/test_webview.py

# Run with coverage
pytest --cov=src/qt_webview_bridge

# Run with verbose output
pytest -v

# Run specific test
pytest tests/test_bridge.py::test_data_bridge_functionality
```

## Examples and Documentation

### Running Examples
```bash
# Simple WebView demo
python examples/simple_webview_example.py

# Bridge communication demo
python examples/bridge_communication_example.py
```

### Development Scripts
```bash
# Set up git hooks (one-time setup)
python scripts/setup-hooks.py

# Test git hooks are working
python scripts/test-hooks.py
```

### Example Development
When creating new examples:
1. **Self-contained**: Examples should work with just `pip install qt-webview-bridge[examples]`
2. **Documented**: Clear docstrings and inline comments
3. **Educational**: Show best practices and common patterns
4. **Visual**: Provide immediate visual feedback when run

### Documentation Updates
- **README.md**: Keep usage examples current
- **Docstrings**: Update for any API changes
- **Context Docs**: Update architecture docs for significant changes
- **Changelog**: Document all user-visible changes

## Release Process

### Version Management
- **Semantic Versioning**: MAJOR.MINOR.PATCH (e.g., 0.1.0)
- **Development Versions**: Use `.dev0` suffix during development
- **Release Candidates**: Use `.rc1` suffix for pre-releases

### Release Checklist
1. [ ] All tests passing
2. [ ] Documentation updated
3. [ ] Version bumped in `pyproject.toml` and `__init__.py`
4. [ ] CHANGELOG.md updated
5. [ ] Examples tested on target platforms
6. [ ] Git tag created
7. [ ] PyPI package built and uploaded

### Build Process
```bash
# Install build tools
pip install build twine

# Build package
python -m build

# Check package
twine check dist/*

# Upload to PyPI (production)
twine upload dist/*

# Upload to TestPyPI (staging)
twine upload --repository testpypi dist/*
```

## IDE Configuration

### VS Code Settings (`.vscode/settings.json`)
```json
{
    "python.linting.enabled": false,
    "python.formatting.provider": "none",
    "python.analysis.typeCheckingMode": "basic",
    "[python]": {
        "editor.defaultFormatter": "charliermarsh.ruff",
        "editor.codeActionsOnSave": {
            "source.organizeImports": true
        },
        "editor.formatOnSave": true
    },
    "ruff.lint.args": ["--config=pyproject.toml"],
    "ruff.format.args": ["--config=pyproject.toml"]
}
```

### PyCharm Configuration
1. **Code Style**: Set line length to 88 characters
2. **Imports**: Configure to match ruff's isort settings
3. **Type Checking**: Enable MyPy plugin
4. **Testing**: Set pytest as default test runner

## Debugging Strategies

### WebView Debugging
```python
# Enable development tools (Qt 5.6+)
webview.enable_dev_tools(True)  # F12 to open dev tools

# JavaScript console logging
webview.execute_javascript("console.log('Debug message')")

# Bridge communication debugging
def debug_bridge_calls():
    bridge = webview.get_bridge_object("data")
    bridge.error_occurred.connect(lambda msg: print(f"Bridge Error: {msg}"))
```

### Qt Application Debugging
```python
# Enable Qt logging
import os
os.environ['QT_LOGGING_RULES'] = 'qt.webengine.debug=true'

# Widget inspection
from qtpy.QtWidgets import QApplication
QApplication.instance().aboutQt()  # Show Qt version info
```

### Common Issues and Solutions

#### Styling Conflicts
```python
from qt_webview_bridge.utils import detect_qt_styling_conflicts

# Check for conflicts before creating WebView
conflicts = detect_qt_styling_conflicts(parent_widget)
for conflict in conflicts:
    print(f"Warning: {conflict}")
```

#### Content Loading Issues
```python
from qt_webview_bridge.utils import validate_web_content_path

# Validate content path
is_valid, issues = validate_web_content_path("./web-dist")
if not is_valid:
    for issue in issues:
        print(f"Content Issue: {issue}")
```

#### Bridge Communication Problems
```python
# Test bridge connectivity
def test_bridge_connection():
    webview.execute_javascript("""
        if (typeof qt !== 'undefined') {
            console.log('Qt WebChannel available');
        } else {
            console.error('Qt WebChannel not available');
        }
    """)
```

## Performance Profiling

### Python Performance
```bash
# Profile Python code
python -m cProfile -s cumulative examples/bridge_communication_example.py

# Memory profiling
pip install memory-profiler
python -m memory_profiler examples/simple_webview_example.py
```

### WebView Performance
- Use browser dev tools (F12) for JavaScript profiling
- Monitor Qt WebEngine process memory usage
- Profile bridge communication overhead

## Continuous Integration

### GitHub Actions Example (if using GitHub)
```yaml
name: CI
on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: [3.9, 3.10, 3.11, 3.12]
    
    steps:
    - uses: actions/checkout@v3
    - name: Set up Python ${{ matrix.python-version }}
      uses: actions/setup-python@v4
      with:
        python-version: ${{ matrix.python-version }}
    
    - name: Install dependencies
      run: |
        pip install -e ".[dev]"
        
    - name: Run ruff
      run: ruff check .
      
    - name: Run mypy
      run: mypy src/
      
    - name: Run tests
      run: pytest
```

This development workflow ensures code quality, maintainability, and reliable releases while providing a smooth developer experience.