# OpenBCI
Hight level Python module OpenBCI hardware.

::: warning
  * This is NOT an official package from [OpenBCI team](https://openbci.com/).
  * This module is still unstable and not recommended for use in production.
:::

## What is?

A Python module for interaction with [OpenBCI boards](https://openbci.com/).
Currently, we have support for Cyton (and Daisy) and their WiFi module.
All source code can be accessed from our [bitbucket repository](https://bitbucket.org/gcpds/python-openbci/src/master/).


## What do we want?

We want a stable, high level, easy to use and extensible Python module for work
with OpenBCI, for students and researchers. We are developing a set of tools for
preprocessing, real-time data handling and streaming.


## Who are we?
We are a research group focused on digital processing of signals and machine
learning from the National University of Colombia at Manizales ([GCPDS](http://www.hermes.unal.edu.co/pages/Consultas/Grupo.xhtml;jsessionid=8701CFAD84FB5D540090846EA8912D48.tomcat6?idGrupo=615&opcion=1>)).



## How works?

An acquisition object can be instantiated from differents backend imlplementation:
Serial, WiFi and WebSockets.


| **Interface**                 | **Module**                           |
|:------------------------------|:-------------------------------------|
| Serial (RFduino)              | bci = CytonRFDuino()                 |
| WiFi                          | bci = CytonWiFi(ip_address)          |
| WebSockets                    | bci = CytonWS(ip_address)            |

Each instance has a set of common methods to handle data acquisition.

| **Method/Object**             | **Serial** | **WiFi** | **WebSockets** |
|:------------------------------|:----------:|:--------:|:--------------:|
| bci.start_collect()           |     yes    |    yes   |       yes      |
| bci.stop_collect()            |     yes    |    yes   |       yes      |
| bci.reset_input_buffer()      |     yes    |    yes   |       no       |
| bci.reset_output_buffer()     |     yes    |    yes   |       no       |
| bci.eeg_serial                |     yes    |    yes   |       no       |
| bci.eeg_buffer                |     yes    |    yes   |       no       |
| bci.eeg_pack                  |     yes    |    yes   |       yes      |


## Contact:

Main developer: Yeison Cardona yencardonaal@unal.edu.co, [@yeisondev](https://twitter.com/yeisondev).


