.. MQTT-PWN documentation master file, created by
   sphinx-quickstart on Thu Jul 19 19:51:45 2018.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to MQTT-PWN!
====================

MQTT is a machine-to-machine connectivity protocol designed as an extremely lightweight publish/subscribe messaging transport and widely used by millions of IoT devices worldwide.
MQTT-PWN intends to be a one-stop-shop for IoT Broker penetration-testing and security assessment operations, as it combines enumeration, supportive functions and exploitation modules while packing it all within command-line-interface with an easy-to-use and extensible shell-like environment.

.. code-block:: shell

   daniel@lab:~/mqtt_pwn ⇒ python run.py

    ╔╦╗╔═╗╔╦╗╔╦╗  ╔═╗┬ ┬╔╗╔
    ║║║║═╬╗║  ║───╠═╝│││║║║
    ╩ ╩╚═╝╚╩  ╩   ╩  └┴┘╝╚╝

        by @Akamai
   >> help


**Features:**

- credential brute-forcer - configurable brute force password cracking to bypass authentication controls
- topic enumerator - establishing comprehensive topic list via continuous sampling over time
- useful information grabber - obtaining and labeling data from an extensible predefined list containing known topics of interest
- GPS tracker - plotting routes from devices using OwnTracks app and collecting published coordinates
- sonoff exploiter – design to extract passwords and other sensitive information


MQTT-PWN Documentation
----------------------

.. toctree::
   :maxdepth: 2

   intro
   plugins
   extensions
   source/modules


Additional Information
----------------------

If you can't find the information you're looking for, have a look at the
index or try to find it using the search function:

* :ref:`genindex`
* :ref:`search`