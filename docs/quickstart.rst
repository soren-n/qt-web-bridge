Quick Start
===========

This guide will get you up and running with Qt Web Bridge in just a few minutes.

Basic WebView
-------------

Here's the simplest way to create a WebView that hosts web content:

.. code-block:: python

    from qtpy.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
    from qt_web_bridge import BridgedWebView

    app = QApplication([])

    # Create main window
    window = QMainWindow()
    window.setWindowTitle("My Web App")
    window.setGeometry(100, 100, 1200, 800)

    # Setup central widget
    central_widget = QWidget()
    window.setCentralWidget(central_widget)
    layout = QVBoxLayout(central_widget)

    # Create WebView
    webview = BridgedWebView()
    layout.addWidget(webview)

    # Load web content (adjust path to your web app)
    webview.set_web_content("path/to/your/web/dist")
    webview.load_content()

    window.show()
    app.exec()

Loading Different Content Types
-------------------------------

Development vs Production
~~~~~~~~~~~~~~~~~~~~~~~~~

Qt Web Bridge automatically handles different content loading scenarios:

.. code-block:: python

    # For production (built web app)
    webview.set_web_content("dist/")

    # For development (with dev server)
    webview.set_dev_html_path("dev/index.html")

    # Or inline HTML for testing
    webview.set_dev_html_content("""
    <!DOCTYPE html>
    <html>
    <head><title>Test App</title></head>
    <body><h1>Hello from Qt Web Bridge!</h1></body>
    </html>
    """)

Adding Python-JavaScript Communication
---------------------------------------

Simple Data Bridge
~~~~~~~~~~~~~~~~~~

Create bidirectional communication between Python and JavaScript:

.. code-block:: python

    from qt_web_bridge import BridgedWebView, DataBridge

    # Create a data bridge
    class MyDataBridge(DataBridge):
        def __init__(self):
            super().__init__()
            # Initialize with some data
            self.update_data({"message": "Hello from Python!"})

        def handle_search(self, query: str) -> list:
            # Handle search requests from JavaScript
            return [f"Result for: {query}"]

    # Setup WebView with bridge
    webview = BridgedWebView()
    data_bridge = MyDataBridge()
    webview.register_bridge_object("data", data_bridge)

In your JavaScript code, you can now interact with Python:

.. code-block:: javascript

    // Access the bridge (available after page load)
    window.qt.webChannelTransport.onmessage = function(message) {
        const data = JSON.parse(message.data);
        console.log("Received from Python:", data);
    };

    // Send search query to Python
    data.searchData("my query");

Action Bridge for RPC Calls
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

For more structured Python function calls from JavaScript:

.. code-block:: python

    from qt_web_bridge import ActionBridge

    class MyActionBridge(ActionBridge):
        def save_file(self, filename: str, content: str) -> bool:
            """Save file from JavaScript."""
            try:
                with open(filename, 'w') as f:
                    f.write(content)
                return True
            except Exception as e:
                self.error_occurred.emit(f"Save failed: {e}")
                return False

        def get_system_info(self) -> dict:
            """Return system information."""
            import platform
            return {
                "platform": platform.system(),
                "python_version": platform.python_version(),
            }

    # Register the action bridge
    action_bridge = MyActionBridge()
    webview.register_bridge_object("actions", action_bridge)

JavaScript usage:

.. code-block:: javascript

    // Call Python functions
    actions.saveFile("test.txt", "Hello World!");

    // Get system info
    const info = actions.getSystemInfo();
    console.log("Python version:", info.python_version);

Using the Utility Function
---------------------------

For simple use cases, use the convenience function:

.. code-block:: python

    from qt_web_bridge import create_simple_webview

    # Creates a ready-to-use WebView widget
    webview = create_simple_webview(
        content_path="path/to/web/content",
        window_title="My App",
        window_size=(1200, 800)
    )

Complete Example
----------------

Here's a complete working example that demonstrates most features:

.. code-block:: python

    import sys
    from qtpy.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
    from qt_web_bridge import BridgedWebView, DataBridge, ActionBridge

    class AppDataBridge(DataBridge):
        def __init__(self):
            super().__init__()
            self.update_data({"users": ["Alice", "Bob", "Charlie"]})

        def handle_search(self, query: str) -> list:
            users = self.get_data().get("users", [])
            return [user for user in users if query.lower() in user.lower()]

    class AppActionBridge(ActionBridge):
        def add_user(self, name: str) -> bool:
            print(f"Adding user: {name}")
            return True

        def delete_user(self, name: str) -> bool:
            print(f"Deleting user: {name}")
            return True

    def main():
        app = QApplication(sys.argv)

        # Create main window
        window = QMainWindow()
        window.setWindowTitle("Qt Web Bridge Demo")
        window.setGeometry(100, 100, 1200, 800)

        # Setup UI
        central_widget = QWidget()
        window.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        # Create WebView with bridges
        webview = BridgedWebView()
        data_bridge = AppDataBridge()
        action_bridge = AppActionBridge()

        webview.register_bridge_object("data", data_bridge)
        webview.register_bridge_object("actions", action_bridge)

        # Set content and load
        webview.set_dev_html_content("""
        <!DOCTYPE html>
        <html>
        <head><title>Qt Web Bridge Demo</title></head>
        <body>
            <h1>Qt Web Bridge Demo</h1>
            <p>Check the browser console for bridge interactions!</p>
            <script>
                // Bridge will be available after page load
                window.addEventListener('load', function() {
                    console.log('Page loaded, bridges available!');
                });
            </script>
        </body>
        </html>
        """)

        layout.addWidget(webview)
        webview.load_content()

        window.show()
        return app.exec()

    if __name__ == "__main__":
        sys.exit(main())

Next Steps
----------

Now that you have a basic understanding:

1. :doc:`guides/basic-usage` - Learn more about WebView configuration
2. :doc:`guides/bridges` - Deep dive into Python-JavaScript communication
3. :doc:`guides/advanced` - Advanced features and best practices
4. :doc:`examples/index` - More comprehensive examples
