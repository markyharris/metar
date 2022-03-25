# metar_poweroff.py - Mark Harris

#from weather import *
#from news import *
from metar_display import *
import json
import sys
from waveshare_epd import epd7in5b_V2

def shutdown():
    epd = epd7in5b_V2.EPD()
    epd.init()
    print("One Moment Please...")
    epd.Clear()
    print("Screen Should Now Be Blank")

if __name__ == "__main__":
    shutdown()