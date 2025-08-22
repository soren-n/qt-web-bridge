# Dependencies and Technology Stack

## Core Technology Stack

### Python Runtime
- **Version**: Python 3.11+ (supports 3.11, 3.12)
- **Rationale**: Modern Python with enhanced type hints and performance improvements
- **Future**: Will follow Python's end-of-life schedule for version support

### Qt Framework (via QtPy)
- **Primary Dependency**: QtPy 2.0.0+
- **Supported Implementations**:
  - PySide6 (recommended, Qt 6.x)
  - PyQt6 (Qt 6.x alternative)
  - PySide2 (Qt 5.x, legacy)
  - PyQt5 (Qt 5.x, legacy)

**QtPy Abstraction Benefits**:
- Single codebase supports multiple Qt implementations
- User can choose their preferred Qt backend
- Smooth migration path between Qt versions
- Licensing flexibility (MIT vs GPL vs Commercial)

### Core Qt Modules Used
```python
from qtpy.QtCore import QObject, Signal, Slot, QUrl, QTimer
from qtpy.QtWidgets import QWidget, QVBoxLayout, QApplication  
from qtpy.QtWebEngineWidgets import QWebEngineView
from qtpy.QtWebChannel import QWebChannel
```

**Module Dependencies**:
- **QtCore**: Base object system, signals/slots, URL handling
- **QtWidgets**: UI components, layouts, application lifecycle
- **QtWebEngineWidgets**: Chromium-based WebView component
- **QtWebChannel**: JavaScript bridge communication

## Runtime Dependencies

### Production Dependencies
```toml
[project]
dependencies = [
    "qtpy>=2.0.0",
    # Qt implementation provided by user:
    # PySide6, PyQt6, PySide2, or PyQt5
]
```

**Dependency Philosophy**:
- **Minimal**: Only QtPy as direct dependency
- **User Choice**: Let users choose their Qt implementation
- **No Transitive Dependencies**: Avoid heavy third-party packages
- **Cross-Platform**: All dependencies must support Windows, macOS, Linux

### Optional Dependencies
```toml
[project.optional-dependencies]
dev = [
    "pytest>=7.0",       # Testing framework
    "pytest-qt>=4.0",    # Qt testing utilities
    "ruff>=0.1.0",       # Modern linting/formatting (replaces black)
    "mypy>=1.0",         # Static type checking
    "pre-commit>=3.0.0", # Git hooks for quality enforcement
    "PySide6>=6.0",      # Development Qt implementation
]

examples = [
    "PySide6>=6.0",      # Qt implementation for examples
]

docs = [
    "sphinx>=8.2.3",             # Documentation generator
    "furo>=2025.7.19",           # Modern Sphinx theme
    "sphinx-autoapi>=3.6.0",     # Auto API documentation
    "myst-parser>=4.0.1",        # Markdown support
    "sphinx-copybutton>=0.5.2",  # Copy code buttons
    "sphinx-design>=0.6.1",      # Design components
    "sphinxext-opengraph>=0.12.0", # Open Graph metadata
    "linkify-it-py>=2.0.3",      # Link detection
]
```

## Development Tools Stack

### Code Quality Tools

#### Ruff (Primary Tool)
- **Purpose**: Linting, formatting, import sorting
- **Version**: 0.1.0+
- **Replaces**: flake8, black, isort, pyupgrade
- **Configuration**: Extensive rule selection in `pyproject.toml`

**Selected Rules**:
```toml
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

#### MyPy (Type Checking)
- **Version**: 1.0+
- **Configuration**: Strict typing with QtPy exceptions
- **Target**: Comprehensive type coverage

#### Pytest (Testing)
- **Version**: 7.0+
- **Extensions**: pytest-qt for Qt widget testing
- **Configuration**: Tailored for Qt application testing

### Modern Development Tools

#### uv (Package Manager)
- **Version**: Latest
- **Purpose**: Modern Python package and project management
- **Benefits**: 
  - 10-100x faster than pip
  - Reproducible builds with uv.lock
  - Single tool for virtual environments and dependencies
  - Drop-in replacement for pip/pip-tools
- **Usage**: Primary development workflow tool

#### Pre-commit (Quality Gates)
- **Version**: 3.0+
- **Purpose**: Automated code quality enforcement via git hooks
- **Configuration**: `.pre-commit-config.yaml`
- **Hooks**: Ruff formatting/linting, MyPy type checking, basic file checks

### Build and Distribution Tools

#### Hatchling (Build Backend)
- **Purpose**: Modern Python package building
- **Configuration**: Minimal configuration in `pyproject.toml`
- **Benefits**: Standards-compliant, efficient builds

#### Package Structure
```toml
[tool.hatch.build.targets.wheel]
packages = ["src/qt_web_bridge"]

[tool.hatch.build.targets.sdist]
include = [
    "/src",
    "/tests", 
    "/examples",
    "/README.md",
    "/LICENSE",
    "/pyproject.toml",
]
```

## Platform Compatibility

### Operating Systems
- **Windows**: Windows 10+ (Qt WebEngine requirements)
- **macOS**: macOS 10.14+ (Qt WebEngine requirements)
- **Linux**: Modern distributions with Qt WebEngine support

### Qt Version Compatibility Matrix
| Qt Version | QtPy Support | WebEngine | Status |
|------------|--------------|-----------|---------|
| Qt 6.5+    | ✅ PySide6   | ✅ Modern | Recommended |
| Qt 6.2+    | ✅ PySide6   | ✅ Stable | Supported |
| Qt 5.15    | ✅ PySide2   | ⚠️ Legacy | Maintenance |
| Qt 5.12    | ✅ PySide2   | ⚠️ Legacy | Minimum |

### WebEngine Compatibility
**Chromium Version**: Depends on Qt version
- Qt 6.5: Chromium 102+
- Qt 6.2: Chromium 94+  
- Qt 5.15: Chromium 87+

**Web Standards Support**:
- ES2020+ JavaScript
- CSS Grid, Flexbox
- WebComponents (custom elements)
- Modern DOM APIs

## Dependency Management Strategy

### Version Pinning Philosophy
- **Runtime**: Minimum versions only (`qtpy>=2.0.0`)
- **Development**: Compatible ranges (`pytest>=7.0`)
- **Examples**: Specific implementation (`PySide6>=6.0`)

### Security and Updates
- **Regular Updates**: Monitor dependencies for security updates
- **Testing**: Comprehensive testing across Qt implementations
- **Breaking Changes**: Careful evaluation of dependency updates

### Dependency Resolution
```bash
# User installs core package
pip install soren-n-qt-web-bridge

# User chooses Qt implementation  
pip install PySide6  # or PyQt6, PySide2, PyQt5

# Modern development setup with uv
uv sync --dev

# Traditional development setup
pip install soren-n-qt-web-bridge[dev]
```

## CI/CD and Infrastructure Stack

### GitHub Actions
- **Platform**: GitHub Actions (cloud-based CI/CD)
- **Operating Systems**: Ubuntu 24.04, Windows latest, macOS latest
- **Python Versions**: 3.11, 3.12 (matrix testing)
- **Workflow Files**: `.github/workflows/ci.yml`, `.github/workflows/publish.yml`

### PyPI Publishing
- **Security**: OIDC Trusted Publishing (no API tokens)
- **Environments**: TestPyPI → PyPI with manual approvals
- **Attestations**: PEP 740 automatic attestation generation
- **Package Formats**: Wheel (.whl) and Source Distribution (.tar.gz)

### Documentation Infrastructure
- **Generator**: Sphinx 8.2+ with Python 3.12
- **Theme**: Furo (modern, responsive design)
- **Extensions**:
  - sphinx-autoapi (automatic API documentation)
  - myst-parser (Markdown file support)
  - sphinx-copybutton (copy code buttons)
  - sphinx-design (design components)
  - sphinxext-opengraph (social media metadata)
- **Hosting**: Read the Docs (readthedocs.io)
- **URL**: https://qt-web-bridge.readthedocs.io/
- **Formats**: HTML, PDF, ePub

### Dependency Management
- **Primary**: uv with uv.lock for reproducible builds
- **Fallback**: pip with requirements files
- **Updates**: Dependabot for automated dependency updates
- **Security**: GitHub Security Advisories integration

### Quality Assurance Infrastructure
- **Code Quality**: Ruff (linting + formatting)
- **Type Safety**: MyPy with strict configuration
- **Testing**: Pytest with pytest-qt for Qt widget testing
- **Pre-commit**: Automated quality gates via git hooks
- **Coverage**: Pytest-cov for test coverage reporting

## Technology Decisions and Rationale

### Why QtPy?
1. **Implementation Flexibility**: Users choose Qt backend
2. **License Compatibility**: Supports both GPL and commercial Qt
3. **Migration Path**: Easy Qt version upgrades
4. **Community Standard**: Widely adopted in Qt Python ecosystem

### Why QWebEngineView?
1. **Modern Web Standards**: Full Chromium engine
2. **Performance**: Hardware-accelerated rendering
3. **Security**: Chromium's security model
4. **JavaScript Bridge**: Built-in QWebChannel support

**Alternatives Considered**:
- QWebView (deprecated)
- Electron integration (too heavy)
- CEF Python (complex deployment)

### Why Minimal Dependencies?
1. **Deployment Simplicity**: Fewer version conflicts
2. **Security Surface**: Fewer third-party vulnerabilities  
3. **Performance**: Lighter runtime footprint
4. **Reliability**: Less dependency update churn

## Integration Ecosystem

### Compatible Frameworks
**Frontend Technologies**:
- React 18+ with TypeScript
- Vue 3+ with TypeScript
- Vanilla JavaScript/TypeScript
- Angular (with QWebChannel integration)

**Python Integration**:
- Django (for data backends)
- Flask (for API services)
- FastAPI (for modern APIs)
- SQLAlchemy (for database integration)

### Host Application Integration
**Desktop Frameworks**:
- Maya (Autodesk)
- Houdini (SideFX) 
- Blender (via Qt)
- Custom Qt Applications

**Integration Patterns**:
- Plugin architectures
- Panel systems
- Embedded UIs
- Standalone applications

## Performance Characteristics

### Memory Usage
- **Base WebView**: ~50-100MB (Chromium engine overhead)
- **Bridge Objects**: <1MB per bridge
- **Python Integration**: Minimal overhead via QWebChannel

### Startup Performance
- **Cold Start**: 1-3 seconds (WebEngine initialization)
- **Warm Start**: 100-500ms (subsequent WebViews)
- **Content Loading**: Depends on web content complexity

### Runtime Performance
- **JavaScript Bridge**: ~1ms per call (JSON serialization overhead)
- **UI Rendering**: Native Chromium performance
- **Memory Growth**: Managed by Chromium's garbage collection

## Future Technology Roadmap

### Short-term (6 months)
- **Qt 6.6+ Support**: Latest Qt features
- **Ruff Migration**: Complete transition from black/flake8
- **Python 3.13**: Support for latest Python

### Medium-term (1 year)  
- **Qt 7 Preparation**: Monitor Qt development
- **WebAssembly**: Investigate WASM integration
- **Performance Optimization**: Bridge communication improvements

### Long-term (2+ years)
- **Alternative WebViews**: Evaluate WebKit, CEF alternatives
- **Mobile Support**: Qt for Android/iOS integration
- **Cloud Integration**: Remote content loading patterns

## Troubleshooting Common Dependencies

### Qt Installation Issues
```bash
# PySide6 installation problems
pip install --upgrade pip
pip install PySide6

# Alternative: conda installation
conda install pyside6

# Verify installation
python -c "from PySide6.QtWebEngineWidgets import QWebEngineView"
```

### WebEngine Missing
**Symptoms**: ImportError on QWebEngineView
**Solutions**:
1. Install full Qt package (not just QtCore)
2. Check system WebEngine dependencies
3. Verify Chromium runtime availability

### Platform-Specific Issues

#### Windows
- **Visual C++ Runtime**: Ensure MSVC redistributable installed
- **WebView2**: May conflict with Qt WebEngine

#### macOS
- **Security**: May need to allow WebEngine in security settings
- **Rosetta**: Ensure compatibility on Apple Silicon

#### Linux
- **libxcb**: Ensure X11 dependencies installed
- **Wayland**: Qt WebEngine Wayland support varies

This technology stack provides a solid foundation for cross-platform WebView integration while maintaining flexibility and performance.