==============================
Metashield-clean-up-sdk-python
==============================

Installation
============

Install the ``metashield_clean_up`` package using pip::

    pip install metashield_clean_up

Usage
=====

Example for cleaning a file.

.. code-block:: python

    import metashield_clean_up

    api = metashield_clean_up.MetashieldCleanUp("APP_ID_HERE", "SECRET_KEY_HERE")
    response = api.clean_file(stream, "my_file.pdf")
    response = api.get_clean_result(response.data["resultId"])


Run tests
=========

Before run tests, replace some settings in *tests/settings_default.py* module.

Tests was built with Python Unittest, run the following commands::

    python -m unittest discover tests
