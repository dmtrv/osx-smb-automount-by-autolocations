#! /usr/bin/env python
# -*- coding: utf-8 -*-
# 2016 dava
# locations based on https://github.com/rimar/wifi-location-changer

import time
import subprocess
from subprocess import Popen, PIPE

TELEZON_HOSTS = ("TelezonOffice", "office")
#MOUNT_LIST =

def run_command(cmd):
    return subprocess.Popen(cmd,
                            shell=True,
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE,
                            stdin=subprocess.PIPE).communicate()[0].split('\n')

time.sleep(2)

SSID = run_command('/System/Library/PrivateFrameworks/Apple80211.framework/Versions/A/Resources/airport -I' \
        '| grep \' SSID:\' | cut -d \':\' -f 2 | tr -d \' \'')[0]
LOCATION_NAMES=run_command('scselect | tail -n +2 | cut -d \"(\" -f 2 | cut -d \")\" -f 1')
CURRENT_LOCATION=run_command('scselect | grep \" \* \" | cut -d \"(\" -f 2 | cut -d \")\" -f 1')[0]

NEW_LOCATION = 'unknown'

if SSID in TELEZON_HOSTS:
    SSID = 'Telezon'

if SSID in LOCATION_NAMES:
    NEW_LOCATION = SSID

else:
    if 'Automatic' in LOCATION_NAMES:
        NEW_LOCATION = 'Automatic'
    elif 'auto' in LOCATION_NAMES:
        NEW_LOCATION = 'auto'
    else:
        print "Automatic location was not found!"
        print "The following locations are known:"
        print LOCATION_NAMES

if NEW_LOCATION != CURRENT_LOCATION:
        print "Changing to %s" % NEW_LOCATION
        cmd = 'scselect %s' % NEW_LOCATION
        run_command(cmd)
        cmd = 'osascript -e \'mount volume "smb://ddu@192.168.3.42/data"\''
        run_command(cmd)
