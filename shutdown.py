# Shutdown.py - Mark Harris
# Used to blank the e-paper display when RPi is shutdown

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