Installation
============

Qt Web Bridge is available on PyPI and can be installed using pip.

Requirements
------------

* Python 3.11 or higher
* One of the following Qt bindings:

  * PySide6 (recommended)
  * PyQt6
  * PySide2
  * PyQt5

* A QWebEngineView-compatible environment

Installing from PyPI
---------------------

Basic Installation
~~~~~~~~~~~~~~~~~~

.. code-block:: bash

    pip install soren-n-qt-web-bridge

This installs the core package with minimal dependencies.

With Examples
~~~~~~~~~~~~~

To install with example dependencies (includes PySide6):

.. code-block:: bash

    pip install soren-n-qt-web-bridge[examples]

Development Installation
~~~~~~~~~~~~~~~~~~~~~~~~

For development work on the package itself:

.. code-block:: bash

    git clone https://github.com/soren-n/qt-web-bridge.git
    cd qt-web-bridge
    pip install -e .[dev]

Installing Qt Backend
---------------------

Qt Web Bridge uses QtPy for Qt compatibility, which means you need to install
one of the supported Qt backends:

PySide6 (Recommended)
~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

    pip install PySide6

PySide6 is the official Python binding for Qt6 and is actively maintained by The Qt Company.

PyQt6
~~~~~

.. code-block:: bash

    pip install PyQt6

PyQt6 is a comprehensive set of Python bindings for Qt6.

Legacy Options
~~~~~~~~~~~~~~

For older environments:

.. code-block:: bash

    # PySide2 (Qt5)
    pip install PySide2

    # PyQt5 (Qt5)
    pip install PyQt5

Verifying Installation
----------------------

You can verify your installation by running:

.. code-block:: python

    import qt_web_bridge
    print(qt_web_bridge.__version__)

To test that Qt is working correctly:

.. code-block:: python

    from qtpy.QtWidgets import QApplication
    app = QApplication([])
    print("Qt backend:", app.instance())

Running Examples
----------------

After installing with the ``[examples]`` extra, you can run the included examples:

.. code-block:: bash

    # Simple WebView example
    python -m qt_web_bridge.examples.simple_webview_example

    # Bridge communication example
    python -m qt_web_bridge.examples.bridge_communication_example

Troubleshooting
---------------

Common Issues
~~~~~~~~~~~~~

**ImportError: No module named 'qtpy'**
  Make sure you have installed one of the Qt backends (PySide6, PyQt6, PySide2, or PyQt5).

**QWebEngineView not available**
  Some Qt installations don't include QWebEngineView. Try installing the full Qt package:

  .. code-block:: bash

      pip install PySide6[all]

**Qt platform plugin issues**
  On Linux systems, you may need additional packages:

  .. code-block:: bash

      # Ubuntu/Debian
      sudo apt-get install qt6-base-dev

      # CentOS/RHEL
      sudo yum install qt6-qtbase-devel

Getting Help
~~~~~~~~~~~~

If you encounter issues:

1. Check the `GitHub Issues <https://github.com/soren-n/qt-web-bridge/issues>`_
2. Create a new issue with your system information and error details
3. Include Python version, Qt backend, and operating system information
