# loose collection of scripts related to i3 and i3blocks

## mpd_controller 
A set of Python scripts to manage mpd (Music Player Daemon). It uses notify-send to display the current song playing with cover art if embeded in the metadata. Is meant to run as a scritp from i3blocks  
but can also be called via the media keys on your keyboard.

### how to use
The main file is **mpd_main.py**, called without arguments, it will just output the current status.  
Additionaly the following arguments can be passed:

* **toggle**: if mpd is playing, it will pause, if is paused it will resume
* **next**: jump to next song in playlist
* **prev**: jump to previous song in playlist

### Config:
in mpd_main.py edit *signal_id* to change to the id used in your i3blocks.conf file so the script can be called from anywhere.

### Install:
None standard Python dependencies:
**python-mpd** Link [python-mpd](https://pypi.org/project/python-mpd/)
* On Arch: `sudo pacman -S python-mpd2`
* Via Pip: `pip install python-mpd`

### Additional:
`notify-send` will get called via subprocess, works best with [Dunst](https://dunst-project.org/documentation/) to show current song playing with cover art extracted from metadata.
