# cinnamon-volume-step-osd
------------------------
A workaround script that allows you to change the system volume by a desired step size while still triggering Cinnamon's volume notification OSD (On Screen Display).

Based on [garrett92895's script](https://github.com/garrett92895/gnome-volume-step-osd) for GNOME.

Requirements
------------
The script is built using Python3 and has a the following requirements
*    `python3`
*    `python3-dbus` (or equivalent)

The package with the correct version is listed as python-dbus in the Arch repositories and python3-dbus in the Debian and Fedora repositories

How to Use
------------------
Just download the script and make sure it is executable with
   ```chmod +x volume-change.py```
The script takes in two arguments:
* [string arg1] increase or decrease
* [int arg2] percentage change

an example for running this script might look like

    python3 volume-change.py increase 2

This would increase the volume by 2 percent

You can then create a custom keyboard shortcut setting the command to either of these commands

    python3 [SCRIPT_DIRECTORY]/volume-change.py [arg1] [arg2]
    ./[SCRIPT_DIRECTORY]/volume-change.py [arg1] [arg2]

Because this script will run every time you press the volume up or down keys, you may want to run a compiled version. You can compile the script with basic optimizations with

    python3 -O -m py_compile volume-change.py

and then your command would be

    python3 [SCRIPT_DIRECTORY]/__pycache__/volume-change.cpython-[PYTHON_VERSION].pyo [arg1] [arg2]

Motivation and Explanation
--------------------------
The motivation for this script is the same as the original: the volume step amount is too large and is hardcoded into Cinnamon. The GNOME devs have since been sensible and made this configurable through a config setting, but the same cannot be said for the Cinnamon devs who have [actively refused to make the same change](https://github.com/linuxmint/cinnamon/pull/8884#issuecomment-553994539).

Previously I used [perspektiv](https://github.com/he-la/perspektiv) as a replacement for the volume OSD, however it now crashes with newer GTK versions so I decided to look into using the built-in OSD instead.

This solution isn't perfect however. Cinnamon appears to do some very weird things with volume where the volume reported in the UI is different to that reported by amixer. I'm guessing they've implemented some kind of non-linear volume curve. Thankfully I don't really use the Cinnamon UI to change the volume, so I can just ignore it.