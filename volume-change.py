#!/usr/bin/python3
# By: James Tattersall. Originally based on Garrett Holbrook's script for GNOME.
# Date: January 9th 2022.
#
# Usage: Changes the system volume through pactl and then
#        makes a dbus method call to the Cinnamon shell to get the
#        Cinnamon volume OSD (On Screen Display)
#
# Requires: python3 and python-dbus (on Arch) or python3-dbus
#           (on Debian) or equivalent

import dbus
import sys
import re
from subprocess import getoutput, call

volRegex = re.compile('.*\/\s+(?P<vol>\d+)%.*')
currentVolume = int(volRegex.match(getoutput('pactl get-sink-volume @DEFAULT_SINK@')).group('vol'))

amount = int(sys.argv[1])

if currentVolume == 100 and amount > 0:
    exit()
elif currentVolume == 0 and amount < 0:
    exit()

newVolume = currentVolume + amount

if newVolume >= 98:
    # workaround for weird issue where setting volumes >= 98% just jumps to 100%
    newVolume = 100 if amount > 0 else 96
elif newVolume < 0:
    newVolume = 0

if newVolume != currentVolume:
    call(f"pactl set-sink-volume @DEFAULT_SINK@ {newVolume}%", shell=True)


# Getting the dbus interface to communicate with Cinnamon's OSD
sessionBus = dbus.SessionBus()
proxy = sessionBus.get_object('org.Cinnamon', '/org/Cinnamon')
interface = dbus.Interface(proxy, 'org.Cinnamon')

logo = 'audio-volume-'
if newVolume == 0:
	logo += 'muted'
elif newVolume < 30:
    logo += 'low'
elif newVolume < 70:
    logo += 'medium'
else:
    logo += 'high'
logo += '-symbolic'

# Make the dbus method call
interface.ShowOSD({ "icon": logo, "level": newVolume })
