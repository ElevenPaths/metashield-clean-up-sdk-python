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

    import time
    import base64
    from metashield_clean_up.api import MetashieldCleanUp

    api = MetashieldCleanUp("REPLACE_APP_ID_HERE", "REPLACE_SECRET_KEY_HERE")
    with open("file.pdf", "rb") as f:
        response = api.clean_file(f.read(), "file.pdf")

    clean_id = response.data["cleanId"]

    time.sleep(5)  # wait until file is cleaned

    response2 = api.get_clean_result(clean_id)
    decoded = base64.b64decode(response2.data[clean_id])

    with open("cleanFile.pdf", "w") as f:
        f.write(decoded)


Run tests
=========

Before run tests, replace some settings in *tests/settings_default.py* module.

Tests was built with Python Unittest, run the following commands::

    python -m unittest discover tests
    
    
