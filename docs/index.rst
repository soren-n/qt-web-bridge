Qt Web Bridge
=============

**Clean Qt WebView widgets for hosting modern web UIs without styling conflicts.**

Qt Web Bridge enables seamless integration of modern web UIs (React, Vue, TypeScript)
into Qt desktop applications without the typical styling conflicts that plague WebView implementations.

.. grid:: 2

    .. grid-item-card:: ⚡ Quick Start
        :link: quickstart
        :link-type: doc

        Get up and running with Qt Web Bridge in just a few lines of code.

    .. grid-item-card:: 📖 User Guide
        :link: guides/index
        :link-type: doc

        Learn how to integrate web UIs into your Qt applications.

    .. grid-item-card:: 🔧 API Reference
        :link: api/index
        :link-type: doc

        Complete API documentation for all classes and functions.

    .. grid-item-card:: 🎯 Examples
        :link: examples/index
        :link-type: doc

        Real-world examples and code snippets.

Features
--------

✨ **Zero Qt Styling Conflicts** - No interference with your web content's CSS

🔗 **Clean Python-JavaScript Bridges** - Simple bidirectional communication via WebChannel

🚀 **Easy Integration** - Drop into any Qt application with minimal setup

🛠️ **Development Friendly** - Support for both development and production content loading

📦 **QtPy Compatible** - Works with PySide6, PyQt6, PySide2, and PyQt5

🎯 **Minimal API** - Small, focused API surface for easy learning

Installation
------------

Install from PyPI:

.. code-block:: bash

    pip install soren-n-qt-web-bridge

For development with examples:

.. code-block:: bash

    pip install soren-n-qt-web-bridge[examples]

Basic Usage
-----------

.. code-block:: python

    from qtpy.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
    from qt_web_bridge import BridgedWebView

    app = QApplication([])

    # Create main window
    window = QMainWindow()
    central_widget = QWidget()
    window.setCentralWidget(central_widget)
    layout = QVBoxLayout(central_widget)

    # Create and setup WebView
    webview = BridgedWebView()
    webview.set_web_content("path/to/your/web/dist")
    layout.addWidget(webview)

    # Load content
    webview.load_content()

    window.show()
    app.exec()

.. toctree::
   :maxdepth: 2
   :hidden:

   installation
   quickstart
   guides/index
   examples/index
   API Reference <api/qt_web_bridge/index>

.. toctree::
   :maxdepth: 1
   :caption: Project Links
   :hidden:

   GitHub Repository <https://github.com/soren-n/qt-web-bridge>
   PyPI Package <https://pypi.org/project/soren-n-qt-web-bridge/>
   Issue Tracker <https://github.com/soren-n/qt-web-bridge/issues>
