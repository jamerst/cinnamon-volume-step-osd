# cinnamon-volume-step-osd

A workaround script that allows you to change the system volume by a desired step size while still triggering Cinnamon's volume notification OSD (On Screen Display).

Originally based on [garrett92895's script](https://github.com/garrett92895/gnome-volume-step-osd) for GNOME.

## Requirements

The script is built using Python3 and has a the following requirements
- `python3`
- `python3-dbus` (or equivalent)
- `pactl`

The package with the correct version is listed as python-dbus in the Arch repositories and python3-dbus in the Debian and Fedora repositories. You can get pactl from the `pulseaudio-utils` package in Fedora (still works fine with PipeWire).

## Usage
Note that the usage differs to the original script.

    python volume-change.py [change]
Where `[change]` is the percentage to change volume by, e.g. `-2` or `2` to decrease/increase by 2%.
### Compiling

Because this script will run every time you press the volume up or down keys, you may want to run a compiled version. You can compile the script with basic optimizations with

    python -O -m py_compile volume-change.py

You can then grab the .pyc output from the \_\_pycache\_\_ folder and substitute `volume-change.py` for that.

## Motivation and Explanation

The motivation for this script is the same as the original: the volume step amount is too large and is hardcoded into Cinnamon. The GNOME devs have since been sensible and made this configurable through a config setting, but the same cannot be said for the Cinnamon devs who have [actively refused to make the same change](https://github.com/linuxmint/cinnamon/pull/8884#issuecomment-553994539).

Previously I used [perspektiv](https://github.com/he-la/perspektiv) as a replacement for the volume OSD, however it now crashes with newer GTK versions so I decided to look into using the built-in OSD instead.

This script also uses pactl instead of amixer like the original script. This is because setting the volume with amixer somehow results in Cinnamon reporting a different value.