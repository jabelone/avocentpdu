avocentpdu
==========

A python module that allows switching outlets on/off on an Avocent PDU
(PM3012V, PM3009H, may work with others)

Installation
------------
With Pip:

``pip install avocentpdu``

Manually:

Just drop the ``pdu.py`` file into the same folder as the python
file you’re calling it from.

Usage
-----

It’s super easy. First, include the module like so

.. code:: python

    import pdu

then initialise an instance of the PDU class

.. code:: python

 import pdu
 pdu = pdu.PDU("pdu_username", "pdu_password", "JabelonePDU", "https://192.168.0.1")

and finally make a function call to ``switch_outlet()``

.. code:: python

    import pdu
    with pdu.PDU("pdu_username", "pdu_password", "JabelonePDU", "https://192.168.0.1") as pdu:
        pdu.switch_outlet(1, 1)

Reference
---------

PDU(string [username], string [password], string [protocol:ip])
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

When you create a new instance you should supply it with the username,
password and protocol/IP address of the webserver running on the PDU
box.

Example:

.. code:: python

    pdu = pdu.PDU("jabelone", "1234", "JabelonePDU", "https://192.168.0.99")

switch\_outlet(string [outlet\_number], boolean [state])
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

When you toggle an outlet you must specify the outlet number (as written
on the PDU) and a state. The state should be either ``True`` for on or
``False`` for off. It will send the http requests out even if it’s
already in the requested state so don’t spam it. Or do. ``¯\_(ツ)_/¯``

Example:

.. code:: python

    # Turn outlet 1 off
    pdu.switch_outlet(1, 0)
    # Turn outlet 13 on
    pdu.switch_outlet(13, 1)
