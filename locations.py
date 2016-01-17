#! /usr/bin/env python
# -*- coding: utf-8 -*-
# 2016 dava
# locations based on https://github.com/rimar/wifi-location-changer

import json
import time
import subprocess
import logging
from subprocess import Popen, PIPE


config_file = "settings.json"

class Location:
    def __init__(self, config_file):
        self.config_file = config_file
        self.settings = self.load_config()

    def load_config(self):
        """
        Simply returns loaded json config
        """
        try:
            json_data = open(self.config_file)
            data = json.load(json_data)
        except Exception, e:
            #logging.critical('Config file has errors, aborting – %s' % e)
            raise e
        else:
            pass
            #logging.info('Config – %s' % config_file)
        json_data.close()
        return data

    def check_locations(self, location):
        """
        Returns True if location defined in settings.json
        """
        if location in self.settings['Locations']:
            return True
        else:
            return False

    def check_mount_point(self, location):
        if len(self.settings['Points'][location]) > 0:
            return True
        else:
            return False

    def need_switch_location(self, SSID, current_location):
        location = 'none'
        for key, value in self.settings['Locations'].items():
            for v in value:
                #print(v)
                if SSID in v:
                    location = key
        if location != 'none':
            if location != current_location:
                return True, location
            else:
                return False, location
        else:
            return False, location

    def switch_location(self, location):
        cmd = 'scselect %s' % location
        self.run_command(cmd)

    def automount(self, location):
        for line in self.settings['Points'][location]:
            tell = ('set sfiles to "'+ line +
                    '"\ntell application "Finder"'
                    '\nmount volume sfiles'
                    '\nend tell')
            cmd = 'osascript -e \'' + tell + '\''
            self.run_command(cmd)

    def get_ssid(self):
        SSID = self.run_command('/System/Library/PrivateFrameworks/Apple80211.framework/Versions/A/Resources/airport -I'
            '| grep \' SSID:\' | cut -d \':\' -f 2 | tr -d \' \'')[0]
        return SSID

    def get_locations(self):
        location_list = self.run_command('scselect | tail -n +2 | cut -d \"(\" -f 2 | cut -d \")\" -f 1')
        return location_list

    def get_current_location(self):
        current_location = self.run_command('scselect | grep \" \* \" | cut -d \"(\" -f 2 | cut -d \")\" -f 1')[0]
        return current_location

    def run_command(self, cmd):
        return subprocess.Popen(cmd,
                                shell=True,
                                stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE,
                                stdin=subprocess.PIPE).communicate()[0].split('\n')


time.sleep(2)

loc = Location(config_file)
SSID = loc.get_ssid()
locations_list = loc.get_locations()
current_location = loc.get_current_location()

if not loc.check_locations(current_location):
    raise SystemExit(0)

if not loc.check_mount_point(current_location):
    raise SystemExit(0)

need_switch, new_location = loc.need_switch_location(SSID, current_location)

if need_switch:
    loc.switch_location(new_location)
    loc.automount(new_location)