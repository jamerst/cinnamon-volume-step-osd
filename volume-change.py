#!/usr/bin/python3
# By: Garrett Holbrook. Modified by James Tattersall.
# Date: August 27th, 2015. Modified January 8th 2022.
#
# Usage: Changes the system volume through amixer and then
#        makes a dbus method call to the Cinnamon shell to get the
#        Cinnamon volume OSD (On Screen Display)
#
# Requires: python3 and python-dbus (on Arch) or python3-dbus
#           (on Debian) or equivalent
import dbus
import sys
from subprocess import getoutput, call

# Getting the dbus interface to communicate with Cinnamon's OSD
session_bus = dbus.SessionBus()
proxy = session_bus.get_object('org.Cinnamon', '/org/Cinnamon')
interface = dbus.Interface(proxy, 'org.Cinnamon')

# Interpreting how to affect the volume and by what percentage and
# then creating a bash command that will reduce the stdout to the
# new percentage volume. Vol = volume
vol_action = sys.argv[1]
vol_percent_change = int(sys.argv[2])

# Get the volumes for all the channels
comm_get_volume='amixer get Master | grep -oP "\[\d*%\]" | sed s:[][%]::g'
vol_percentages=list(map(int, getoutput(comm_get_volume).split()))

# Average them into a single value (note the +0.5 for rounding errors)
vol_percentage=int(sum(vol_percentages)/len(vol_percentages)+0.5)

# Add/subtract the value of volume (handle negative values)
increase = (vol_action == 'increase')
if (increase):
    if vol_percentage == 100:
        exit(0)

    vol_percentage=max(0, (vol_percentage + vol_percent_change))
else:
    if vol_percentage == 0:
        exit(0)

    vol_percentage=max(0, (vol_percentage - vol_percent_change))


# Set the volume for both channels
command = 'amixer sset Master ' + str(vol_percentage) + '% > /dev/null'

if (increase):
    command += ' && amixer set Master unmute > /dev/null'

# Apply volume
call(command, shell=True)

# If it's 0 then add mute flag (trigger sub-action, keyboard light for example)
if vol_percentage == 0:
	call('amixer set Master mute', shell=True);

# Determining which logo to use based off of the percentage
logo = 'audio-volume-'
if vol_percentage == 0:
	logo += 'muted'
elif vol_percentage < 30:
    logo += 'low'
elif vol_percentage < 70:
    logo += 'medium'
else:
    logo += 'high'
logo += '-symbolic'

# Make the dbus method call
interface.ShowOSD({"icon":logo, "level":vol_percentage})
