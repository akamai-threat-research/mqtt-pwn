MQTT-PWN
========

.. image:: https://readthedocs.org/projects/ansicolortags/badge/?version=latest
   :target: http://mqtt-pwn.readthedocs.io/?badge=latest

.. image:: https://img.shields.io/github/license/akamai-threat-research/mqtt-pwn.svg
   :target: https://github.com/akamai-threat-research/mqtt-pwn/blob/master/LICENSE

.. image:: https://img.shields.io/badge/python-3%2E6-green.svg
   :target: https://github.com/akamai-threat-research/mqtt-pwn/

.. image:: https://img.shields.io/badge/docker-friendly-blue.svg
   :target: https://github.com/akamai-threat-research/mqtt-pwn/

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

- Credential Brute-Forcer - configurable brute force password cracking to bypass authentication controls
- Topic Enumerator - establishing comprehensive topic list via continuous sampling over time
- Useful Information Grabber - obtaining and labeling data from an extensible predefined list containing known topics of interest
- GPS tracker - plotting routes from devices using OwnTracks app and collecting published coordinates
- Sonoff Exploiter – design to extract passwords and other sensitive information
- Extensibility - the framework was designed to add new custom plugins with ease
- Shodan - search through `Shodan.io` API for available vulnerable MQTT brokers

Documentation
-------------

Documentation is available at https://mqtt-pwn.readthedocs.io/.
