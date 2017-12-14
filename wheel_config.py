G25_wheel_config = {
"WHEEL_NAME": "Logitech G25 Racing Wheel USB",
"STEERING_WHEEL": 0,
"ACCELERATOR": 2,
"BRAKE": 3,
"CLUTCH": 4,

"GEAR_1": 8,
"GEAR_2": 9,
"GEAR_3": 10,
"GEAR_4": 11,
"GEAR_5": 12,
"GEAR_6": 13,
"TOP_GEAR": 13,
"GEAR_REVERSE": 14,

"IGNITION": 4,
"PARKING_BRAKE": 5,
"HEADLAMP": 1,
"HIGH_BEAM": 3,
"WINDSHIELD_WIPER": 2,

"STEERING_WHEEL_TOLERANCE": 10,
"PEDAL_TOLERANCE": 5
}

G27_wheel_config = {
"WHEEL_NAME": "G27 Racing Wheel",
"STEERING_WHEEL": 0,
"ACCELERATOR": 1,
"BRAKE": 2,
"CLUTCH": 3,

"GEAR_1": 12,
"GEAR_2": 13,
"GEAR_3": 14,
"GEAR_4": 15,
"GEAR_5": 16,
"GEAR_6": 17,
"TOP_GEAR": 17,
"GEAR_REVERSE": 22,

"IGNITION": 11,
"PARKING_BRAKE": 10,
"HEADLAMP": 1,
"HIGH_BEAM": 3,
"WINDSHIELD_WIPER": 2,

"STEERING_WHEEL_TOLERANCE": 10,
"PEDAL_TOLERANCE": 5
}

wheels = [G25_wheel_config, G27_wheel_config]

class WheelConfig:

  wheel_config = G27_wheel_config

  def find_wheel_name(self, wheel_name):
    for wheel in wheels:
      if wheel_name == wheel["WHEEL_NAME"]:
        return True
    return False
	
  def set_name(self, wheel_name):
    for wheel in wheels:
      if wheel_name == wheel["WHEEL_NAME"]:
        wheel_config = wheel
        return wheel
    return None

  def is_gear_lever(self,button):
    return (button in range(wheel_config["GEAR_1"], wheel_config["TOP_GEAR"]) or 
      button == wheel_config["GEAR_REVERSE"])

  def get_gear_from_button(self, button):
    # returns None when the button is not a gear shift button
    # -1 for reverse gear, gear otherwise
    if button == wheel_config["GEAR_REVERSE"]:
      return -1
    if self.is_gear_lever(button):
      return button - wheel_config["GEAR_1"] + 1
    return None

  def get_steering_Wheel_angle(self, val):
    # pygame returns a value between -1 and 1 for every axis
    # openxc-vehicle-simulator expects a value between -600 and 600
    if val > 1:
      return 600
    if val < -1:
      return -600
    return val * 600

  def get_pedal_percentage(self, pedal, val):
    # pygame returns a value between -1 (fully pressed) and 1 (not pressed) for every axis
    # openxc-vehicle-simulator expects a percentage value between 0 and 100
    if pedal not in (wheel_config.ACCELERATOR, wheel_config.BRAKE, wheel_config.CLUTCH):
      return None
    if val > 1:
      return 0
    if val < -1:
      return 100
    return (1 - val) * 50


