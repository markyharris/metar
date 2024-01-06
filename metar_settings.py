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
use_disp_format = -2     # Choose which display layout to use. -1=Random layout, -2=Cycle layouts, -3=Display IP
interval = 60            # enter default time in seconds between METAR updates - i.e. 3600 = 1 hour
use_remarks = 0          # 0 = display airport information, 1 = display metar remarks info

# Display Units
wind_speed_units = 0     # 0=km/h, 1=m/s, 2=knots, 3=miles per hour
cloud_layer_units = 1    # 0=feet, 1=meters
visibility_units = 1     # 0=miles, 1=kilometers
temperature_units = 0    # 0=°C Celsius, 1=°F Farhenheit
pressure_units = 0       # 0=Hectopascal, 1=Inch Hg


# preferred_layouts - select the preferred layouts to cycle through by putting a '1' in its location.
# then change the 'use_preferred' variable below to '1'
use_preferred = 0        # 0 = No, 1 = Yes
# Map the list below to match the layout list here; [layout0,layout1,layout2,layout3,layout4,layout5,layout6,layout7,layout8,layout9]
#   for instance  - [1,0,0,0,0,0,0,0,0,1] will only display layout0 and layout9.
preferred_layouts = [0,0,0,1,1,0,0,0,0,1] # 0=Do Not Display layout, 1=Do Display Layout


# Random Airports Choices (Layout5):
# This is the only layout that doesn't use cmd line arguments
# For the same airports in the same locations on screen, place 12 airports in list. The 13th will be the default airport
# For randomly selected airports, put more than 12 in list. 12 will randomly be displayed, 13th will be default
# If you put less than 12 airports in list, it will pad the missing spots with the default airport above.
random_airports = ["KEYW","KFVE","KSEA","KCVG", "KLAS","KCMR","KGRR","KMSN", \
                   "KLAX","KNBC","KFVE","KBUF"]


