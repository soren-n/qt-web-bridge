# Project Architecture Overview

## Project Mission
**qt-webview-bridge** enables seamless integration of modern web UIs (React, Vue, TypeScript) into Qt desktop applications without the typical styling conflicts that plague WebView implementations. The architecture prioritizes clean separation, minimal overhead, and zero visual interference with host applications.

## High-Level Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Host Qt Application                       │
│  ┌─────────────────────────────────────────────────────────┐ │
│  │                  WebViewPanel                           │ │
│  │  ┌───────────────────────────────────────────────────┐  │ │
│  │  │               BridgedWebView                      │  │ │
│  │  │  ┌─────────────────────────────────────────────┐  │  │ │
│  │  │  │            QWebEngineView                   │  │  │ │
│  │  │  │                    │                        │  │  │ │
│  │  │  │              QWebChannel                    │  │  │ │
│  │  │  └─────────────────────────────────────────────┘  │  │ │
│  │  └───────────────────────────────────────────────────┘  │ │
│  └─────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
                                │
                          Python-JS Bridge
                                │
┌─────────────────────────────────────────────────────────────┐
│                     Web Content Layer                       │
│  ┌─────────────────────────────────────────────────────────┐ │
│  │              TypeScript/React/Vue UI                    │ │
│  │                                                         │ │
│  │  JavaScript ←→ QWebChannel ←→ Python Bridge Objects     │ │
│  │                                                         │ │
│  │  • DataBridge (data synchronization)                   │ │
│  │  • ActionBridge (user action handling)                 │ │
│  │  • Custom bridges (domain-specific)                    │ │
│  └─────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
```

## Core Components

### 1. BridgedWebView (`webview.py`)
**Purpose**: Primary WebView widget with zero styling conflicts

**Key Responsibilities**:
- Host QWebEngineView with zero Qt stylesheet interference
- Manage content loading (development vs production builds)
- Coordinate Python-JavaScript bridge registration
- Handle WebView lifecycle events

**Design Decisions**:
- Zero-margin layouts to be completely transparent to host styling
- Support for multiple content loading strategies
- Built-in temporary file management for development content
- Signal-based event communication

**Integration Points**:
```python
webview = BridgedWebView()
webview.set_web_content("path/to/dist")  # Production build
webview.set_dev_html_content(html_str)   # Development content
webview.register_bridge_object("api", bridge)
webview.load_content()
```

### 2. Bridge System (`bridge.py`)
**Purpose**: Clean Python-JavaScript communication layer

**Architecture Pattern**: 
- Base class (`WebViewBridge`) provides common functionality
- Specialized bridges (`DataBridge`, `ActionBridge`) for specific use cases
- JSON-based serialization for all cross-boundary communication

**Key Components**:

#### WebViewBridge (Base Class)
- Common signals: `data_updated`, `status_changed`, `error_occurred`
- JSON serialization helpers with error handling
- Bridge capability introspection

#### DataBridge (Specialized)
- Item management: `set_items()`, `update_item()`, `add_item()`
- Search functionality with customizable filtering
- Real-time data synchronization via Qt signals

#### ActionBridge (Specialized)  
- Action handler registration: `register_action_handler()`
- RPC-style JavaScript-to-Python calls
- Async operation support with result callbacks

**Communication Flow**:
```
JavaScript                Python
    │                        │
    │ ──── Action Call ────→  │ (via @Slot methods)
    │                        │
    │ ←──── Data Push ─────   │ (via Qt Signals)
    │                        │
    │ ←──── Status Update ──  │ (via Qt Signals)
```

### 3. WebViewPanel (`panel.py`)
**Purpose**: Optional wrapper for host application integration

**Design Philosophy**:
- Provides integration points without imposing structure
- Zero styling to maintain host application aesthetics
- Lifecycle management for complex applications

**Usage Patterns**:
- Simple wrapper: Panel + WebView for basic integration
- Factory functions for common configurations (asset browser, dashboard, etc.)
- Clean resource management and cleanup

### 4. Utilities (`utils.py`)
**Purpose**: Helper functions for common patterns and debugging

**Key Functions**:
- `create_simple_webview()`: Quick setup for basic use cases
- `detect_qt_styling_conflicts()`: Debug styling interference
- `validate_web_content_path()`: Content validation utilities
- Factory functions for specialized WebView configurations

## Data Flow Architecture

### Content Loading Strategy
```
┌─────────────────────────────────────────────────────────┐
│                Content Loading Priority                 │
├─────────────────────────────────────────────────────────┤
│ 1. Production Build (content_path/index.html)          │
│ 2. Development HTML File (dev_html_path)               │  
│ 3. Development HTML Content (inline string)            │
│ 4. Error: No content available                         │
└─────────────────────────────────────────────────────────┘
```

### Python-JavaScript Communication
```
Python Side                          JavaScript Side
┌─────────────────┐                 ┌──────────────────┐
│   DataBridge    │ ────signals───→ │  Event Handlers  │
│                 │                 │                  │
│   ActionBridge  │ ←───calls─────  │  Action Triggers │
│                 │                 │                  │
│   WebViewBridge │ ←─→ QWebChannel │  QWebChannel     │
└─────────────────┘                 └──────────────────┘
```

### Error Handling Strategy
```
Error Level          Handler                   Recovery
┌────────────────────────────────────────────────────────┐
│ Bridge Errors    →  Signal + Callback    →  Continue   │
│ Content Loading  →  Signal + Fallback    →  Dev Mode   │
│ JavaScript       →  Console + Signal     →  Log Only   │  
│ Qt Integration   →  Exception + Cleanup  →  Fail Safe  │
└────────────────────────────────────────────────────────┘
```

## Module Dependencies

### Internal Dependencies
```
webview.py
├── bridge.py (for WebViewBridge types)
└── utils.py (for temporary file management)

bridge.py  
└── (standalone, minimal Qt dependencies)

panel.py
├── webview.py (for BridgedWebView)
└── bridge.py (for type hints)

utils.py
├── webview.py (for factory functions)
├── bridge.py (for factory functions)  
└── panel.py (for factory functions)
```

### External Dependencies
```
QtPy Abstraction Layer
├── QtCore (QObject, Signal, Slot, QUrl, QTimer)
├── QtWidgets (QWidget, QVBoxLayout, QApplication)
├── QtWebEngineWidgets (QWebEngineView)
└── QtWebChannel (QWebChannel)

Python Standard Library
├── json (serialization)
├── pathlib (file management)
├── typing (type annotations)
└── collections.abc (protocols)
```

## Extension Points

### Custom Bridge Development
```python
class CustomBridge(WebViewBridge):
    # Domain-specific signals
    domain_event = Signal(str)
    
    def _get_capabilities(self) -> list[str]:
        return ["custom_feature", "domain_integration"]
    
    @Slot(str, result=str)
    def domain_specific_call(self, params: str) -> str:
        # Implementation here
        pass
```

### Content Loading Extensions
```python
class ExtendedWebView(BridgedWebView):
    def load_content(self) -> None:
        # Custom loading logic
        if self._try_custom_content_source():
            return
        # Fall back to base implementation
        super().load_content()
```

### Panel Customization
```python
def create_custom_panel(config: dict) -> WebViewPanel:
    panel = WebViewPanel(config["title"])
    webview = panel.setup_webview(config["content_path"])
    
    # Add custom bridges
    if "data_source" in config:
        bridge = create_data_bridge_for(config["data_source"])
        webview.register_bridge_object("data", bridge)
        
    return panel
```

## Performance Characteristics

### Memory Management
- **WebView Lifecycle**: Proper cleanup of QWebEngineView resources
- **Bridge Objects**: WeakRef patterns to avoid circular references  
- **Temporary Files**: Automatic cleanup of development content files

### Rendering Performance
- **Zero Styling Overhead**: No Qt stylesheet processing interference
- **Minimal Layout**: Direct widget hierarchy with zero margins
- **Native WebEngine**: Leverage Chromium's optimized rendering

### JavaScript Bridge Performance
- **JSON Serialization**: Efficient but bounded by data size
- **Signal Delivery**: Asynchronous, non-blocking communication
- **Slot Calls**: Direct method invocation, minimal overhead

## Security Model

### Content Security
```
Trusted Zone              Boundary                 Untrusted Zone
┌─────────────────┐       ┌─────────────┐         ┌──────────────────┐
│ Python Backend  │ ←─→   │ QWebChannel │   ←─→   │ JavaScript/HTML  │
│                 │       │             │         │                  │  
│ • File System   │       │ • JSON Only │         │ • Web Content    │
│ • System APIs   │       │ • Type Safe │         │ • User Input     │
│ • Databases     │       │ • Validated │         │ • External Data  │
└─────────────────┘       └─────────────┘         └──────────────────┘
```

### Bridge Security
- **Input Validation**: All JavaScript data validated before processing
- **Error Isolation**: Bridge errors don't crash the host application
- **API Boundaries**: Clear distinction between trusted Python and untrusted web content

## Testing Strategy

### Unit Testing (`tests/`)
```
test_webview.py     → BridgedWebView functionality
test_bridge.py      → Bridge communication patterns
test_utils.py       → Utility function validation
test_integration.py → Full component integration
```

### Testing Patterns
- **Mock Qt Objects**: Use pytest-qt for widget testing
- **Bridge Communication**: JSON serialization round-trip tests  
- **Content Loading**: File system and URL handling validation
- **Error Scenarios**: Graceful failure mode verification

## Deployment Architecture

### Package Structure
```
qt-webview-bridge/
├── src/qt_webview_bridge/    # Source code
├── tests/                    # Test suite
├── examples/                 # Usage examples
├── docs/                     # Documentation
└── pyproject.toml           # Build configuration
```

### Distribution Strategy
- **PyPI Package**: Standard Python package distribution
- **Minimal Dependencies**: Only QtPy as runtime dependency
- **Optional Dependencies**: Development tools, examples
- **Cross-Platform**: Windows, macOS, Linux support via QtPy