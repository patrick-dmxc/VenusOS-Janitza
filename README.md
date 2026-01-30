# VenusOS-Janitza
Service to use Janitza Meters with Venus OS
![Picture](https://github.com/patrick-dmxc/VenusOS-Janitza/blob/main/Picture%201.png?raw=true)

## Automatic Installation to Survive Firmware Updates
1. Place sript called `install-janitza.sh` which mimics manual installation flow into `/data` directory by running these commands
   ```
   cd /data
   wget https://raw.githubusercontent.com/patrick-dmxc/VenusOS-Janitza/main/install-janitza.sh -O install-janitza.sh
   ```
3. make `/data/install-janitza.sh` file executable by `chmod +x /data/install-janitza.sh`
4. run  the install script by `./install-janitza.sh` command
5. reboot
6. everything in the section below called "Manual Installation" should be taken care of


## Manual Installation
1. Download the Janitza.py: `wget https://raw.githubusercontent.com/patrick-dmxc/VenusOS-Janitza/main/Janitza.py`
2. Copy Janitza.py to the victron directory: `cp Janitza.py /opt/victronenergy/dbus-modbus-client/`
3. Delete or rename the `__pycache__` folder from the same directory
4. Add the line `import Janitza` after `import victron_em` in the file `dbus-modbus-client.py`
5. Reboot the Cerbo GX

## Supported Meters
| Device               | Modbus RTU | Modbus TCP         | Status                       | Notes                     |
|----------------------|------------|--------------------|------------------------------|---------------------------|
| UMG 96 RM            | ✅         | (✅) with Gateway | 🟡 untested                  | —                         |
| UMG 96 RM-E-RCM      | ✅         |  ✅               | 🟡 untested                  | —                         |
| UMG 96 RM-E          | ✅         |  ✅               | 🟢 tested by @patrick-dmxc   | —                         |
| UMG 96 RM-P          | ✅         | (✅) with Gateway | 🟡 untested                  | —                         |
| UMG 96 RM-CBM        | ✅         | (✅) with Gateway | 🟡 untested                  | —                         |
| UMG 96 RM-M          | ✅         | (✅) with Gateway | 🟡 untested                  | —                         |
| UMG 96 RM-PN         | ✅         |  ✅               | 🟡 untested                  | —                         |
| UMG 96 RM (ohters)   | ✅         | (✅) with Gateway | 🟡 untested                  | possible                  |
| UMG 96 PQ-L          | ✅         | (✅) with Gateway | 🟡 untested                  | —                         |
| UMG 96 PQ (ohters)   | ✅         | (✅) with Gateway | 🟡 untested                  | possible                  |
| UMG 103-CBM          | ✅         | (✅) with Gateway | 🟢 tested by @kommando828    | —                         |
| ohters               ||| [Request](https://github.com/patrick-dmxc/VenusOS-Janitza/issues/new/choose) | possible   |

Please provide feedback if your Device is working or not with this Script

## Issues
If its not working, please open an issue and we can fix it

## Your Meter is not Supported
Open an Issue and we can see if its possible to implement your Meter as well

## Note
1. The script will disappear during firmware updates if you chosed the Manuel Instalation and needs to be reinstalled.\
2. In the event that Victron has changed, added, or removed methods from register.py, it is possible that the script may not function correctly right away.
