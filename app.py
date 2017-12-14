#!/usr/bin/python
# Control openxc-vehicle-simulator from a Logitech G27 controller
# by Juergen Schmerder (@schmerdy)
from __future__ import print_function

import sys
from wheel import Wheel

DEBUG = True

# first command line parameter can be hostname
# if simulator runs on different computer
if len(sys.argv) > 1:
  HOST = sys.argv[1] 
else:
  HOST = "localhost"

try:
    import urllib2,urllib
    no_urllib2 = False
except:
    no_urllib2 = True
import pygame
import math
import os
import traceback
from wheel_config import WheelConfig

wheel_cfg = None

# make sure pygame doesn't try to open an output window
os.environ["SDL_VIDEODRIVER"] = "dummy"

ignition_status_values = {
  0: "off",
  1: "accessory",
  2: "start",
  3: "run"
}

def send_data(name, value, HOST='localhost'):
  if no_urllib2:
    print('%s: %s' % (name, value))
  else:
      url = "http://" + HOST + ":50000/_set_data"
      post_data = urllib.urlencode([('name',name),('value',value)])
      if DEBUG: 
        print(post_data)
      try:
        req = urllib2.urlopen(url, post_data)
      except Exception as ex:
        if DEBUG:
          print(ex)

def is_simulator_running(HOST):
  url = "http://" + HOST + ":50000"
  if not no_urllib2:
      try:
        req = urllib2.urlopen(url)
      except Exception as ex:
        print (ex)
        print (traceback.format_exc())
        print ("No openxc-vehicle-simulator running on", url)
        print ("logging wheel input instead")
        return False
      return True
  return False
 
def cycle_ignition_status(old_status):
  if old_status == 3:
    return 0
  return old_status + 1

def on_accelerator(val):
  send_data("accelerator", val)
def on_brake(val):
  send_data("brake", val)
def on_clutch(val):
  send_data("clutch", val)
  pass
def on_angle(val):
  send_data('angle', val)
def on_ignition(val):
  send_data("ignition_status", str(val))
def on_parking_brake(val):
  send_data("parking_brake_status", str(val).lower())
def on_headlamp(val):
  send_data("headlamp_status", str(val).lower())
def on_high_beam(val):
  send_data("high_beam_status", str(val).lower())
def on_windshied_wiper(val):
  send_data("windshield_wiper_status", str(val).lower())
def on_gear_shift(gear):
  send_data("gear_lever_position", gear)

wheel_o = Wheel()

if wheel_o.wheel_found():
    wheel_cfg = wheel_o.get_wheel_config()
    wheel_o.register_steering_wheel(on_angle)
    wheel_o.register_pedal(wheel_cfg["ACCELERATOR"], on_accelerator)
    wheel_o.register_pedal(wheel_cfg["BRAKE"], on_brake)
    wheel_o.register_pedal(wheel_cfg["CLUTCH"], on_clutch)
    wheel_o.register_button(wheel_cfg["IGNITION"], on_ignition)
    wheel_o.register_button(wheel_cfg["PARKING_BRAKE"], on_parking_brake)
    wheel_o.register_button(wheel_cfg["HEADLAMP"], on_headlamp)
    wheel_o.register_button(wheel_cfg["HIGH_BEAM"], on_high_beam)
    wheel_o.register_button(wheel_cfg["WINDSHIELD_WIPER"], on_windshied_wiper)
    wheel_o.register_gear_shift(on_gear_shift)

    try: 
        
      if not is_simulator_running(HOST):
        HOST = None
      else:
        print("Found car on", HOST)

      wheel_o.loop()
  
    except Exception as e:
      print(e)
      print(traceback.format_exc())
