MQTT-PWN
========

MQTT is a machine-to-machine connectivity protocol designed as an extremely lightweight publish/subscribe 
messaging transport and widely used by millions of IoT devices worldwide. MQTT-PWN intends to be a one-stop-shop 
for IoT Broker penetration-testing and security assessment operations, as it combines enumeration, 
supportive functions and exploitation modules while packing it all within command-line-interface 
with an easy-to-use and extensible shell-like environment.


.. image:: https://raw.githubusercontent.com/akamai-threat-research/mqtt-pwn/master/docs/_static/images/another-logo-trans-bg-small.png
    :target: https://github.com/akamai-threat-research/mqtt-pwn

Authors
-------

- `Daniel Abeles <https://twitter.com/Daniel_Abeles>`_
- `Moshe Zioni <https://twitter.com/dalmoz_>`_

Feature Support
---------------

- credential brute-forcer - configurable brute force password cracking to bypass authentication controls
- topic enumerator - establishing comprehensive topic list via continuous sampling over time
- useful information grabber - obtaining and labeling data from an extensible predefined list containing known topics of interest
- GPS tracker - plotting routes from devices using OwnTracks app and collecting published coordinates
- sonoff exploiter – design to extract passwords and other sensitive information

Documentation
-------------

Documentation is available at https://mqtt-pwn.readthedocs.io/en/latest/.
