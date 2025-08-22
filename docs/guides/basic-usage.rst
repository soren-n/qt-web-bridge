Basic Usage
===========

This guide covers the fundamental concepts and usage patterns for Qt Web Bridge.

Creating a WebView
------------------

The core component is :class:`~qt_web_bridge.BridgedWebView`, which provides a clean
WebView widget designed to host modern web UIs without styling conflicts.

Basic WebView Setup
~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    from qtpy.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
    from qt_web_bridge import BridgedWebView

    app = QApplication([])

    # Create main window
    window = QMainWindow()
    window.setWindowTitle("My Web App")
    window.setGeometry(100, 100, 1200, 800)

    # Setup layout
    central_widget = QWidget()
    window.setCentralWidget(central_widget)
    layout = QVBoxLayout(central_widget)

    # Create WebView
    webview = BridgedWebView()
    layout.addWidget(webview)

    # Configure and load content
    webview.set_web_content("path/to/web/dist")
    webview.load_content()

    window.show()
    app.exec()

Content Loading Strategies
--------------------------

Qt Web Bridge supports multiple content loading strategies to accommodate
different development workflows.

Production Content Loading
~~~~~~~~~~~~~~~~~~~~~~~~~

For built web applications (production):

.. code-block:: python

    webview = BridgedWebView()
    webview.set_web_content("dist/")  # Path to built web app
    webview.load_content()

Development Content Loading
~~~~~~~~~~~~~~~~~~~~~~~~~~

For development with hot-reload servers:

.. code-block:: python

    webview = BridgedWebView()
    webview.set_dev_html_path("dev/index.html")  # Development HTML file
    webview.load_content()

Inline Content for Testing
~~~~~~~~~~~~~~~~~~~~~~~~~~

For quick testing or embedded content:

.. code-block:: python

    html_content = """
    <!DOCTYPE html>
    <html>
    <head><title>Test App</title></head>
    <body>
        <h1>Hello from Qt Web Bridge!</h1>
        <script>console.log('WebView loaded!');</script>
    </body>
    </html>
    """

    webview = BridgedWebView()
    webview.set_dev_html_content(html_content)
    webview.load_content()

Content Loading Priority
~~~~~~~~~~~~~~~~~~~~~~~

Qt Web Bridge attempts content loading in this order:

1. **Production build** - ``content_path/index.html``
2. **Development HTML** - ``dev_html_path``
3. **Inline content** - ``dev_html_content``
4. **Error state** - Shows error if all fail

This design allows seamless transitions between development and production environments.

WebView Configuration
--------------------

The WebView can be configured for different use cases:

Window and Layout Options
~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    # Set window properties
    webview.setMinimumSize(800, 600)
    webview.setMaximumSize(1920, 1080)

    # Configure for specific layouts
    webview.setSizePolicy(
        QtWidgets.QSizePolicy.Expanding,
        QtWidgets.QSizePolicy.Expanding
    )

Zero Styling Philosophy
~~~~~~~~~~~~~~~~~~~~~~

Qt Web Bridge is designed with a "zero styling" philosophy - it applies no Qt
stylesheets that could interfere with your web content:

.. code-block:: python

    # These are automatically handled by BridgedWebView:
    # - Zero margins and padding
    # - Transparent background
    # - No custom stylesheets
    # - Minimal chrome/UI elements

Error Handling
--------------

Handling Load Errors
~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    from qtpy.QtCore import QUrl
    from qtpy.QtWebEngineWidgets import QWebEngineView

    webview = BridgedWebView()

    def on_load_finished(success: bool):
        if success:
            print("Content loaded successfully")
        else:
            print("Failed to load content")

    # Connect to load finished signal
    webview.web_engine_view.loadFinished.connect(on_load_finished)

Content Validation
~~~~~~~~~~~~~~~~~

.. code-block:: python

    from qt_web_bridge.utils import validate_web_content_path

    content_path = "path/to/web/content"

    if validate_web_content_path(content_path):
        webview.set_web_content(content_path)
        webview.load_content()
    else:
        print(f"Invalid content path: {content_path}")

Utility Functions
----------------

Convenience Creation
~~~~~~~~~~~~~~~~~~~

For simple use cases, use the utility function:

.. code-block:: python

    from qt_web_bridge import create_simple_webview

    webview = create_simple_webview(
        content_path="dist/",
        window_title="My App",
        window_size=(1200, 800)
    )

Debugging Utilities
~~~~~~~~~~~~~~~~~~

.. code-block:: python

    from qt_web_bridge.utils import detect_qt_styling_conflicts

    # Check for potential styling conflicts
    conflicts = detect_qt_styling_conflicts(webview)
    if conflicts:
        print("Potential styling conflicts detected:", conflicts)

Best Practices
--------------

1. **Content Organization**

   - Keep web content in a dedicated ``web/`` or ``dist/`` directory
   - Use relative paths for assets within your web content
   - Test both development and production content loading

2. **Performance**

   - Load content after the WebView is properly sized
   - Avoid frequent content reloading
   - Use development content loading only during development

3. **Integration**

   - Create WebView widgets as part of your normal Qt layout
   - Don't apply custom stylesheets to the WebView
   - Let the web content handle its own styling

4. **Error Handling**

   - Always validate content paths before loading
   - Handle load failures gracefully
   - Provide fallback content for error states

Next Steps
----------

- :doc:`bridges` - Learn about Python-JavaScript communication
- :doc:`advanced` - Advanced configuration and optimization
- :doc:`../examples/index` - See complete working examples
