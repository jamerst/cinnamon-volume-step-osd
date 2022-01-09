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
currentVolume = int(volRegex.match(getoutput('pactl get-sink-volume 0')).group('vol'))

amount = int(sys.argv[1])

if currentVolume == 100 and amount > 0:
    exit()
elif currentVolume == 0 and amount < 0:
    exit()

change = f"+{amount}%" if amount > 0 else f"{amount}%"

call(f"pactl set-sink-volume 0 {change}", shell=True)

newVolume = currentVolume + amount

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
