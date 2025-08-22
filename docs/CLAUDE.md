# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Development Commands

### Environment Setup
```bash
# Install development dependencies
pip install -e ".[dev]"

# Install with examples
pip install -e ".[examples]"
```

### Code Quality
```bash
# Run all quality checks
ruff check .                    # Lint code
ruff format .                   # Format code
mypy src/                       # Type checking
pytest                          # Run tests

# Run specific test file
pytest tests/test_webview.py

# Run single test
pytest tests/test_bridge.py::test_data_bridge_functionality
```

### Git Hooks Setup
```bash
# Set up pre-commit hooks (one-time setup)
python scripts/setup-hooks.py

# Manual hook commands
pre-commit run --all-files      # Run all hooks manually
pre-commit run ruff             # Run only ruff
pre-commit run mypy             # Run only mypy  
pre-commit run pytest --hook-stage manual  # Run tests manually

# Test hooks are working
python scripts/test-hooks.py

# Update hook versions
pre-commit autoupdate
```

### Examples
```bash
# Run example applications (requires PySide6/PyQt6)
python examples/simple_webview_example.py
python examples/bridge_communication_example.py
```

### Package Building
```bash
# Build package for distribution
python -m build
```

## Architecture Overview

This package provides Qt WebView widgets that host modern web UIs without Qt styling conflicts. The architecture centers around three core patterns:

### Core Components Architecture

**CleanWebView** (`src/qt_webview_bridge/webview.py`)
- Primary WebView widget with zero Qt stylesheet interference
- Manages QWebEngineView with transparent zero-margin layouts
- Handles content loading priority: production build → dev HTML → inline content
- Coordinates bridge object registration via QWebChannel

**Bridge System** (`src/qt_webview_bridge/bridge.py`)
- `WebViewBridge`: Base class with JSON serialization, error handling, common signals
- `DataBridge`: Specialized for data synchronization and search functionality
- `ActionBridge`: Handles RPC-style JavaScript-to-Python calls
- All communication uses JSON serialization for type safety

**WebViewPanel** (`src/qt_webview_bridge/panel.py`)
- Optional wrapper for host application integration
- Maintains zero styling philosophy
- Provides lifecycle management and utility functions

### Communication Flow

```
JavaScript                    Python
     │                          │
     │ ── Action Calls ────→    │ (@Slot methods)
     │                          │
     │ ←──── Data Push ────     │ (Qt Signals)
     │                          │
     └── QWebChannel ←→ QWebChannel
```

### Key Design Principles

- **Zero Styling Conflicts**: Never applies Qt stylesheets that interfere with web content
- **QtPy Abstraction**: Works with PySide6, PyQt6, PySide2, and PyQt5
- **JSON Communication**: All bridge data uses JSON for cross-boundary type safety
- **Signal-Based Events**: Leverages Qt's event system for loose coupling

### Content Loading Strategy

The WebView loads content with this priority:
1. Production build (`content_path/index.html`)
2. Development HTML file (`dev_html_path`)
3. Development HTML content (inline string)
4. Error state

### Bridge Pattern Implementation

Bridges inherit from `WebViewBridge` and use:
- `@Slot` decorators for JavaScript-callable methods
- Qt `Signal`s for Python-to-JavaScript data push
- `_safe_json_dumps/_loads` for error-resistant serialization
- Error isolation through signal emission

## File Structure Context

- `src/qt_webview_bridge/__init__.py`: Public API exports
- `src/qt_webview_bridge/webview.py`: Core WebView widget implementation
- `src/qt_webview_bridge/bridge.py`: Bridge classes for Python-JS communication
- `src/qt_webview_bridge/panel.py`: Optional panel wrapper
- `src/qt_webview_bridge/utils.py`: Helper functions and debugging utilities
- `tests/`: Pytest test suite with Qt testing support
- `examples/`: Runnable examples demonstrating usage patterns
- `scripts/`: Development and setup scripts
- `docs/`: Documentation and guides

## Testing Strategy

Uses pytest with pytest-qt for Qt widget testing. Tests focus on:
- WebView widget creation and lifecycle
- Bridge JSON communication round-trips
- Content loading fallback behavior
- Integration between WebView and bridge objects

## Development Notes

- Python version: 3.11+ required
- Line length: 88 characters (ruff configuration)
- Type hints required for all public methods
- Uses Google-style docstrings
- QtPy provides cross-Qt-version compatibility
- Temporary files created in `src/qt_webview_bridge/temp/` for development content