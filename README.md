# MQTT-Pwn

## Authors
* Daniel Abeles
* Moshe Zioni

## About
MQTT-PWN intends to be a one-stop-shop for IoT Broker penetration-testing and security assessment operations, as it combines enumeration, supportive functions and exploitation modules while packing it all within command-line-interface with an easy-to-use and extensible shell-like environment. 

 
## Features
Amongst its abilities/modules:
* credential brute-forcer - configurable brute force password cracking to bypass authentication controls
* topic enumerator - establishing comprehensive topic list via continuous sampling over time
* useful information grabber - obtaining and labeling data from an extensible predefined list containing known topics of interest
* GPS tracker - plotting routes from devices using OwnTracks app and collecting published coordinates
* Sonoff exploiter – design to extract passwords and other sensitive information


## Usage
### Installation
To install mqtt-pwn, first make sure you're running python 3 (recommended 3.6 and above). Then, install the required packages:
```bash
pip install -r requirements.txt
```

### Operator Side
To operate your "server" side operation, simply run the tool by:
```bash
python run.py
```

If you see the screen below, everything works fine:
```
⇒  python run.py

    ╔╦╗╔═╗╔╦╗╔╦╗  ╔═╗┬ ┬╔╗╔
    ║║║║═╬╗║  ║───╠═╝│││║║║
    ╩ ╩╚═╝╚╩  ╩   ╩  └┴┘╝╚╝

        by @Akamai
        
>>
```

Now, to see what features and capabilities just hit the "help" command:
```
>> help

Documented commands (type help <topic>):

Broker Related Operations
-------------------------
discovery  scans  system_info  topics

General Commands
----------------
back  edit  help  history  quit  shell

Victim Related Operations
-------------------------
commands  exec  exploit  select  victims
```

As shown above, the commands are separated into three categories:
* *Broker Related Operation* - commands that require interaction only with the broker, in example, retrieve the brokers' information.
* *Victim Related Operation* - commands that require interaction with the C2 feature victim, in example run a command on one of those victim.
* *General Commands* - commands that do not require any kind of 3rd party interaction, in example run local command or print the help menu.

### Arguments
Every command on the `run.py` file, is built like a command line arguments pattern (using the `argparse` library), in example, enter `-h / --help` flag to show all the options for a specific command:
```
>> topics --help
usage: topics [-h] [-s] [-i ID] [-l LABEL] [-n NAME]

List topics that were detected through discovery scans

optional arguments:
  -h, --help            show this help message and exit
  -s, --show-only-labeled
                        show only labeled topics
  -i ID, --id ID        show only a specific topic by id
  -l LABEL, --label LABEL
                        show only specific topics that startswith a label
  -n NAME, --name NAME  show only specific topics that startswith a topic name
``` 

### Victim Side
When you will desire to start the C2 feature, you first need to infect a victim with the `victim.py` file. Once that victim is infected, he will automatically register to the selected `mqtt broker`.
Then, it is possible to select that victim to execute shell commands on it. 

## C2 Flow
The MQTT protocol works in the `publish/subscribe` pattern, so every victim that we infect, will:
* Subscribe to a specific `input` topic to receive commands
* Publish to a specific `output` topic when he is ready to post back the output.

```
     subscribe: "input" +------------+   publish: "whoami"
     +----------------> |            | <-------------------+
     |                  |            |                     |
+----+----+             |   MQTT     |                  +--+------+
| Victim  |             |   Broker   |                  | Attacker|
+----+----+             |            |                  +--+------+
     |                  |            |                     |
     +----------------> |            | <-------------------+
      publish: "root"   +------------+  subscribe: "output"
```

## Future Development
* add url shortener ticket to the backlog [owntracks]
* one point in owntracks might indicate the last good known packet [owntracks]
* battery data, multiple timestamps in device, wifi/gsm [owntracks] [future]
* ^ might show in the single query [owntracks]
* duplicates in topics