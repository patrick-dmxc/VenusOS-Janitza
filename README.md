# VenusOS-Janitza
Service to use Janitza Meters with Venus OS
![Picture](https://github.com/patrick-dmxc/VenusOS-Janitza-UMG-96-RM/blob/main/Picture%201.png?raw=true)

## Installation
1. Download the JanitzaUmg96RM.py: `wget https://raw.githubusercontent.com/patrick-dmxc/VenusOS-Janitza/refs/heads/main/JanitzaUmg96RM.py`
2. Copy JanitzaUmg96RM.py to the victron directory: `cp JanitzaUmg96RM.py /opt/victronenergy/dbus-modbus-client/`
3. Delete or rename the `__pycache__` folder from the same directory
4. Add the line `import JanitzaUmg96RM` after `import carlo_gavazzi` in the file `dbus-modbus-client.py`
5. Reboot the Cerbo GX

## Supported Meters
UMG 96 RM [all variations with Modbus RTU or Modbus TCP]\
UMG 96 PQ [all variations with Modbus RTU or Modbus TCP] (untested)
UMG 503 [all variations with Modbus RTU or Modbus TCP] (untested)

## Issues
If its not working, please open an issue and we can fix it

## Your Meter is not Supported
Open an Issue and we can see if its possible to implement your Meter as well

## Note
The script disappears during firmware updates and needs to be reinstalled. In the event that Victron has changed, added, or removed methods from register.py, it is possible that the script may not function correctly right away.
