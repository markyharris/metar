# metar_settings.py
# Metar Display Settings - Mark Harris
# Version 2.1
# Part of Epaper Display project found at; https://github.com/markyharris/metar/
#
# UPDATED FAA API 12-2023, https://aviationweather.gov/data/api/
#
# These settings will be used if script is run with no cmd line arguments

# Default User Settings
airport = "KFLG"         # enter default airport identifier to display
use_disp_format = -2     # Choose which display layout to use. -1 = Random layout, -2 = Cycle layouts
interval = 60            # enter default time in seconds between METAR updates - i.e. 3600 = 1 hour
use_remarks = 0          # 0 = display airport information, 1 = display metar remarks info

# Display Units
wind_speed_units = 0     # 0=km/h, 1=m/s, 2=knots, 3=miles per hour
cloud_layer_units = 1    # 0=feet, 1=meters
visibility_units = 1     # 0=miles, 1=kilometers
temperature_units = 0    # 0=°C Celsius, 1=°F Farhenheit
pressure_units = 0       # 0=Hectopascal, 1=Inch Hg

# Random Airports Choices (Layout5):
# This is the only layout that doesn't use cmd line arguments
# For the same airports in the same locations on screen, place 12 airports in list. The 13th will be the default airport
# For randomly selected airports, put more than 12 in list. 12 will randomly be displayed, 13th will be default
# If you put less than 12 airports in list, it will pad the missing spots with the default airport above.
random_airports = ["KEYW","KFVE","KSEA","KCVG", "KLAS","KCMR","KGRR","KMSN", \
                   "KLAX","KNBC","KFVE","KBUF"] 
