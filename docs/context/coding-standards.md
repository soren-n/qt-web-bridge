# Coding Standards and Conventions

## Project Overview
**Qt Web Bridge** (PyPI: `soren-n-qt-web-bridge`, import: `qt_web_bridge`) is a Python package that provides clean Qt WebView widgets for hosting modern web UIs without styling conflicts. The codebase emphasizes minimal dependencies, clean APIs, and zero Qt styling interference.

## Repository Information
- **Repository**: https://github.com/soren-n/qt-web-bridge
- **Documentation**: https://qt-web-bridge.readthedocs.io/
- **Package**: soren-n-qt-web-bridge (PyPI)
- **Import**: qt_web_bridge (Python)

## Python Code Standards

### Style Guidelines
- **Line Length**: 88 characters (configured in ruff)
- **Python Version**: Minimum 3.11, targeting 3.11-3.12  
- **Formatter**: Ruff (replaces Black, isort, flake8, pyupgrade)
- **Type Checking**: MyPy with strict typing enabled
- **Pre-commit**: Automated quality enforcement via git hooks

### Import Organization
```python
# Standard library imports
import json
from pathlib import Path
from typing import Any

# Third-party imports  
from qtpy.QtCore import QObject, Signal, Slot
from qtpy.QtWidgets import QWidget, QVBoxLayout

# Local imports
from .bridge import WebViewBridge
from .webview import BridgedWebView
```

### Naming Conventions
- **Classes**: PascalCase (`BridgedWebView`, `DataBridge`)
- **Functions/Methods**: snake_case (`set_web_content`, `load_content`)
- **Constants**: UPPER_SNAKE_CASE (`__version__`, `__all__`)
- **Private Members**: Leading underscore (`_setup_ui`, `_bridge_objects`)

### Documentation Standards

#### Docstring Format
Use Google-style docstrings with full type information:

```python
def register_bridge_object(self, name: str, obj: QObject) -> None:
    """
    Register a Python object to be accessible from JavaScript.

    Args:
        name: JavaScript object name
        obj: Python QObject with @Slot methods for JS to call
    """
```

#### File Header Documentation
Each module should have a comprehensive docstring explaining:
- Purpose and functionality
- Key features and design decisions
- Usage examples
- Integration patterns

Example:
```python
"""
Clean WebView widget for hosting TypeScript UIs with zero Qt styling conflicts.

This component provides a minimal WebView that:
1. Never applies Qt stylesheets that could conflict with host applications
2. Provides clean Python-JavaScript communication via WebChannel
3. Handles development vs production web content loading
4. Is fully reusable across different projects and contexts
"""
```

### Type Annotations
- **Required**: All public methods and functions must have type hints
- **Parameters**: Use union syntax `str | None` (Python 3.11+ style)
- **Return Types**: Always specify, use `None` for procedures
- **Collections**: Use `list[Type]`, `dict[Key, Value]` syntax

```python
def set_items(self, items: list[dict[str, Any]]) -> None:
    """Set items and notify frontend."""
```

### Error Handling
- **Defensive Programming**: Validate inputs and handle edge cases gracefully
- **Logging vs Exceptions**: Use print statements for user feedback, exceptions for programming errors
- **Error Signals**: Emit Qt signals for errors that the UI can handle

```python
def _safe_json_loads(self, json_str: str) -> dict[str, Any]:
    """Safely deserialize JSON string to Python object."""
    try:
        return json.loads(json_str)
    except (TypeError, ValueError) as e:
        self._emit_error(f"JSON parsing error: {e}")
        return {}
```

## Architecture Patterns

### Qt Integration Patterns
1. **Zero Styling**: Never apply custom stylesheets that could conflict
2. **Minimal Layouts**: Use zero-margin layouts for transparency
3. **Signal-Slot Communication**: Leverage Qt's event system for loose coupling

### Bridge Pattern Implementation
- **Base Classes**: Inherit from `WebViewBridge` for common functionality
- **JSON Communication**: Always use JSON for Python-JavaScript data exchange
- **Error Isolation**: Handle bridge errors without crashing the UI

### Project Structure
```
qt-web-bridge/
├── src/qt_web_bridge/        # Source code package
│   ├── __init__.py          # Public API exports
│   ├── webview.py          # Core WebView widget
│   ├── bridge.py           # Bridge base classes and implementations  
│   ├── panel.py            # Optional panel wrapper
│   ├── utils.py            # Utility functions
│   └── temp/               # Temporary files for development
├── tests/                   # Test suite
├── examples/                # Example applications
├── scripts/                 # Development and setup scripts
├── docs/                    # Documentation
│   ├── conf.py             # Sphinx configuration
│   ├── requirements.txt    # Documentation dependencies
│   ├── guides/             # User guides
│   ├── examples/           # Example documentation
│   ├── context/            # Development context docs
│   └── _build/             # Generated documentation
├── .github/                 # GitHub Actions workflows
│   └── workflows/
│       ├── ci.yml          # Continuous Integration
│       └── publish.yml     # PyPI publishing
├── pyproject.toml          # Python project configuration
├── uv.lock                 # Locked dependencies (uv)
├── .readthedocs.yaml       # Read the Docs configuration
├── README.md               # Main documentation
├── LICENSE                 # License file
├── .gitignore             # Git ignore rules
└── .pre-commit-config.yaml # Pre-commit configuration
```

### Root Directory Guidelines
Keep the project root clean and focused:
- **Essential files only**: pyproject.toml, README.md, LICENSE, .gitignore
- **Configuration files**: .pre-commit-config.yaml and similar tool configs
- **Organized directories**: src/, tests/, examples/, docs/, scripts/
- **No loose scripts**: Move utilities to scripts/ directory
- **No redundant docs**: Consolidate documentation in docs/

## Quality Assurance

### Testing Standards
- **Framework**: pytest with pytest-qt for Qt testing
- **Coverage**: Aim for comprehensive test coverage of public APIs
- **Test Structure**: One test file per source module

### Code Quality Tools
```toml
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
```

### Modern Development Workflow

#### Using uv (Recommended)
```bash
# Setup and quality checks
uv sync                      # Install dependencies
uv run ruff check .          # Linting
uv run ruff format .         # Formatting
uv run mypy src/             # Type checking
uv run pytest               # Testing
```

#### Traditional Workflow
```bash
# Quality checks
ruff check .                 # Linting  
ruff format .                # Formatting
mypy src/                    # Type checking
pytest                       # Testing
```

### Automated Quality Assurance
- **Pre-commit Hooks**: Automatic quality checks on git commit
- **GitHub Actions**: CI/CD pipeline with matrix testing
- **Dependabot**: Automated dependency updates
- **Read the Docs**: Automatic documentation building

## API Design Principles

### Public API Guidelines
1. **Minimal Surface**: Keep public APIs as small and focused as possible
2. **Consistent Naming**: Use consistent prefixes (`set_`, `get_`, `load_`)
3. **Chainable Methods**: Where possible, return `self` for method chaining
4. **Backward Compatibility**: Maintain API stability across minor versions

### Signal Design
- **Descriptive Names**: `content_loaded`, `bridge_ready`, `error_occurred`
- **Consistent Parameters**: Use JSON strings for complex data, simple types for events
- **Documentation**: Always document when signals are emitted

### Method Signatures
```python
# Good: Clear, typed, documented
def set_web_content(self, content_path: str, dev_html: str | None = None) -> None:

# Avoid: Unclear parameters, missing types
def setup(self, path, html=None):
```

## Dependencies and Compatibility

### Core Dependencies
- **QtPy**: For Qt abstraction across PySide6/PyQt6/PySide2/PyQt5
- **Minimal**: No heavy dependencies, keep the package lightweight

### Development Dependencies
- **pytest + pytest-qt**: Testing framework
- **ruff**: Linting and formatting
- **mypy**: Type checking
- **PySide6**: Reference Qt implementation for development

### Version Compatibility
- **Python**: 3.11+ (follow supported Python versions)
- **Qt**: Support major Qt versions through QtPy
- **Cross-platform**: Ensure compatibility with Windows, macOS, Linux

## Performance Considerations

### Resource Management
- **Widget Cleanup**: Proper cleanup of Qt resources
- **Memory Leaks**: Avoid circular references between Python and Qt objects
- **WebView Lifecycle**: Clean shutdown of WebEngine processes

### Optimization Guidelines
- **Lazy Loading**: Load web content only when needed
- **Minimal DOM**: Keep JavaScript bridge calls lightweight
- **Error Recovery**: Gracefully handle WebView crashes and reloads

## Security Best Practices

### WebView Security
- **Content Validation**: Validate web content paths before loading
- **JavaScript Isolation**: Limit JavaScript access to Python APIs
- **File System Access**: Restrict web content to designated directories

### Bridge Security
- **Input Validation**: Always validate data from JavaScript
- **Error Information**: Don't expose sensitive information in error messages
- **API Boundaries**: Clear separation between trusted Python and untrusted web content

## CI/CD and Release Standards

### Continuous Integration Requirements
- **Multi-platform Testing**: Ubuntu, Windows, macOS
- **Python Version Matrix**: 3.11, 3.12
- **Quality Gate Enforcement**: All checks must pass before merge
- **Automated Testing**: pytest with Qt widget testing

### Release Process Standards
1. **Version Bumping**: Update `pyproject.toml` version
2. **Tag Creation**: Use semantic versioning tags (`v1.2.3`)
3. **Automated Publishing**: GitHub Actions with OIDC trusted publishing
4. **Manual Approvals**: Required for TestPyPI and PyPI deployments
5. **Documentation**: Automatic rebuild on Read the Docs

### Security Standards
- **No Long-lived Tokens**: Use OIDC trusted publishing only
- **Environment Protection**: Manual approval gates for production
- **Attestation Generation**: PEP 740 attestations for all releases
- **Dependency Security**: Dependabot for automated security updates

### Documentation Standards
- **API Documentation**: Auto-generated from docstrings with sphinx-autoapi
- **User Guides**: Comprehensive guides for all major features
- **Examples**: Working examples for common use cases
- **Read the Docs**: Professional documentation hosting with multiple formats

### Code Quality Standards
- **Zero Warnings**: All quality tools must pass without warnings
- **Test Coverage**: Comprehensive test coverage for public APIs
- **Type Safety**: Full type hints for all public methods
- **Import Organization**: Consistent import ordering with Ruff