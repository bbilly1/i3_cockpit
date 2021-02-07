# loose collection of scripts related to i3 and i3blocks

## mpd_controller 
A set of Python scripts to manage mpd (Music Player Daemon). It uses notify-send to display the current song playing with cover art if embeded in the metadata. Is meant to run as a scritp from i3blocks  
but can also be called via the media keys on your keyboard.

### how to use
The main file is **mpd_main.py**, called without arguments, it will just output the current status.  
The script expects mpd to be running on localhost:6600, and will try to start the daemon  
if it looks like it is not running already.
Additionaly the following arguments can be passed:

* **toggle**: if mpd is playing, it will pause, if is paused it will resume
* **next**: jump to next song in playlist
* **prev**: jump to previous song in playlist

### Config:
in mpd_main.py edit *signal_id* to change to the id used in your i3blocks.conf file so the script can be called from anywhere.

### Install:
None standard Python dependencies:
**python-mpd** [python-mpd2](https://pypi.org/project/python-mpd2/)
* On Arch: `sudo pacman -S python-mpd2`
* Via Pip: `pip install python-mpd2`

### Additional:
`notify-send` will get called via subprocess, works best with [Dunst](https://dunst-project.org/documentation/) to show current song playing with cover art extracted from metadata.


## i3block_py
A collection of standalone python scripts for the slightly more complicated things.  
* **energy.py**: parses `acpi` to output current battery status. Uses `notify-send` to send messages on changes.
* **cpu.py**: parses `/proc/loadavg` to output load average values for last 1, last 5 and last 15 min.
    * call `cpu.py 1` to get the avg from last min
    * call `cpu.py 5` to get the avg from last 5 min
    * call `cpu.py 15` to get the avg from last 15 min


## i3block_shell
A bunch of simple bash scripts to be called via i3blocks.
* **coretemp.sh**: Echos average temperature of all CPU cores by parsing output of `sensors` from package *lm_sensors*, uses icons from [fontawesome.com](https://fontawesome.com/).
* **date.sh**: Echos the current date.
    * on left click: uses notify-send to print current three month calendar.
* **df.sh**: Echos current diskfree level of the root partition.
    * on left click: uses notify-send to print the df of all relevant connected partitions.
* **ip.sh**: Echos current ip addresses in use or inactive when offline.
* **updates.sh**: Echos how many updates are pending.
    * on left click: echos the complete list of all pending updates.
    * on right click: refreshes the current pending updates and echos result.
* **wifiinfo.sh**: Echos current db level of signal strength.
    * on left click: Uses nmcli to echo all device status.


## weather_applet
Standalone script that pulls weather data from [openweathermap.org](https://openweathermap.org/) and prints out 
current temperature and weather. Meant to be used from i3blocks.  
Icons used to display the current weather condition are from [fontawesome.com](https://fontawesome.com/).
* on left click: Get three days forecast, use `notify-send` to send message, works best with *dunst* setup.

### Config:
Get your free openweathermap API key from [here](https://home.openweathermap.org/api_keys).  
Create a file called *config* in the same directory as the *weather.py* script and copy the sample 
data from *config.sample*:
* Replace the dummy *openweathermap_api_key* with your key.
* Add *lat* and *lon* values with the latitude and longitude values from your location.

### Install:
None standard Python dependencies:
**python-requests** [requests](https://requests.readthedocs.io/en/master/)
* On Arch: `sudo pacman -S python-requests`
* Via Pip: `pip install requests`

Fontawesome font pakage:
* On Arch: `sudo pacman -S ttf-font-awesome`
* On Ubuntu: `sudo apt install fonts-font-awesome`
