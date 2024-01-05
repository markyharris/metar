# metar_main.py
# E-Paper METAR Display - by Mark Harris
# Version 2.1
# Part of Epaper Display project found at; https://github.com/markyharris/metar/
#
# UPDATED to New FAA API 12-2023, https://aviationweather.gov/data/api/
#
# Thanks to Aerodynamics for providing a great start for this project
# Visit his page at;
#   https://github.com/aerodynamics-py/WEATHER_STATION_PI
#
# This script uses the api at weather.gov;
#   https://www.weather.gov/documentation/services-web-api#
# This script also uses IFR Low maps from;
#   https://vfrmap.com/map_api.html
# 
# The script will then either display the json weather information provided, 
# or if the json information is not given, the script will use the data scraped 
# from the raw metar string provided. However, the json data is a bit more accurate.
#
# Dynamic icon's are displayed depending on the value of each weather field.
#
# For specific info on using e-paper display with RPi, see;
#   https://www.waveshare.com/wiki/Template:Raspberry_Pi_Guides_for_SPI_e-Paper
# For information on the specific display used for this project see;
#   https://www.waveshare.com/wiki/7.5inch_e-Paper_HAT_(B)
#
# Software is organized into separate scripts depending on its focus
#   metar_main.py - loads the other files as necessary and executes layout routine
#   metar_routines.py - metar specific routines, typically needed for decoding and scraping
#   metar_layouts.py - houses all the different layouts available for display
#   metar_display.py - provides the routines and fonts needed to pring to e-paper
#   metar_settings.py - User defined default settings such as airport and update interval
#   metar_remarks.py - file created from FAA's definitions of a METAR's remarks (RMK)
#   shutdown.py - Used to blank e-Paper on shutdown.
#   epaper.html - html file used to control the metar display
#   data.txt - stores the last run setup for restart purposes
#   temp_pic.png - temporary storage of IFR Low map image when that layout is used
#   webapp.py - flask module to provide needed data to epaper.html and provide simple web server

# Imports
from metar_layouts import *
from metar_settings import *
from metar_routines import *
import time
import requests
import json
import sys
import os
import sys

# epd7in5b_V2 = 3-color 7 by 5 display. Change this based on the display used.
# find 'epd = epd7in5b_V2.EPD()' towards bottom and change also if needed.
# These are located in the directory 'waveshare_epd'
from waveshare_epd import epd7in5b_V2 

# Layouts - add new layouts to this list as necessary
layout_list = [layout0,layout1,layout2,layout3,layout4,layout5,layout6,layout7,layout8,layout9] # ,layout6 Add layout routine names here

# Check for cmdline args and use passed variables instead of the defaults
# example ['/home/pi/metar/metar_main.py', 'metar', 'kabe', '1', '0', '1', '2', '0', '0', '1', '1']
print('len(sys.argv):',len(sys.argv)) # debug
print('sys.argv:',sys.argv,'\n') # debug

# check to see if web admin is supplying the args. If not, use settings.py
if len(sys.argv) >= 10:
    print('Using Args passed from web admin')
    airport = str(sys.argv[1].upper())
    use_disp_format = int(sys.argv[2])
    interval = int(sys.argv[3])
    use_remarks = int(sys.argv[4])
    wind_speed_units = int(sys.argv[5])
    cloud_layer_units = int(sys.argv[6])
    visibility_units = int(sys.argv[7])
    temperature_units = int(sys.argv[8])
    pressure_units = int(sys.argv[9])
else:
    print('Using Args from settings.py file')

print("\nAirport\t", "Layout\t", "Update\t", "Remarks")
print(str(airport)+"\t", str(use_disp_format)+"\t", str(interval)+"\t", str(use_remarks)+"\n")


def main():
    global display,metar,remarks,print_table,use_remarks,use_disp_format,interval,wind_speed_units,cloud_layer_units,visibility_units,temperature_units,pressure_units,layout_list
    
    # Choose  which layout to use.        
    if use_disp_format == -1:
        random_layout(display,metar,remarks,print_table,use_remarks,use_disp_format,interval,wind_speed_units,cloud_layer_units,visibility_units,temperature_units,pressure_units,layout_list)

    elif use_disp_format == -2:
        cycle_layout(display,metar,remarks,print_table,use_remarks,use_disp_format,interval,wind_speed_units,cloud_layer_units,visibility_units,temperature_units,pressure_units,layout_list)

    else:    
        for index, item in enumerate(layout_list):
            if index == use_disp_format:
                print("Layout -->",index,'<--') # debug
                layout_list[index](display,metar,remarks,print_table,use_remarks,use_disp_format,interval,wind_speed_units,cloud_layer_units,visibility_units,temperature_units,pressure_units) # call appropriate layout

    # Print to e-Paper - This is setup to display on 7x5 3 color waveshare panel. epd7in5b_V2
    # To use on 2 color panel, remove ', epd.getbuffer(display.im_red)' from 6 lines lower.
    # All calls to 'display.draw_red.text' will need to be changed to display.draw_black.text
    # The author has not tried this, but this should accommodate the 2 color display.
    print("Updating screen...")
    try:
        epd.init()          
        time.sleep(1)
        print("Printing METAR Data to E-Paper")
        epd.display(epd.getbuffer(display.im_black), epd.getbuffer(display.im_red))
        print("Done")
        time.sleep(2)

    except:
        print("Printing error")
    print("------------")
    return True


# Execute code starting here.
if __name__ == "__main__":
    epd = epd7in5b_V2.EPD() # Instantiate instance for display.
  
    while True:        
#        try:
#        while True: # debug
#            error = 1/0 #debug  # forces error to test the try-except statements
        if True:  # used instead of the try-except statements for debug purposes.
            current_time = time.strftime("%m/%d/%Y %H:%M", time.localtime())
            
            metar = Metar(airport) # pass to routines

            remarks, print_table = decode_remarks(get_rawOb(metar)) # metar.data[0]['rawOb'])
#            print('remarks:',remarks,'print_table:',print_table) # debug
            flightcategory, icon = flight_category(metar)
            
            if len(get_rawOb(metar)) > 0: 
                print('get_rawOb(metar):',get_rawOb(metar),'\n') # debug
            else:
                print("No METAR Being Reported")
                
            print("Updated " + current_time)
            print("Creating display")
            epd.init()
            epd.Clear()
            display = Display() # pass to routines

            # Update values
            metar.update(airport)
            print("Metar Updated")

            main() # Build METAR data to display using specific layout
                                    
            # Setup update interval
            # The update interval can be selected via cmd line or web iterface
            # If Auto Interval is selected, then Flight Category dictates update
            # So the worse the weather, the more often it updates.

            if interval != 0: # if not auto interval selected
                print("sleep ",interval) # debug
                time.sleep(interval) # Sets interval of updates. 3600 = 1 hour

            else:
                if flightcategory == "VFR":
                    print("Auto Interval VFR - Sleep 1 hour") # debug
                    time.sleep(3600) # 1 hour if weather is good
                elif flightcategory == "MVFR":
                    print("Auto Interval MVFR - Sleep 30 mins") # debug
                    time.sleep(1800) # 30 mins if marginal
                elif flightcategory == "IFR":
                    print("Auto Interval IFR - Sleep 20 mins") # debug
                    time.sleep(1200) # 20 mins if stormy
                elif flightcategory == "LIFR": 
                    print("Auto Interval LIFR - Sleep 10 mins") # debug
                    time.sleep(600) # 10 mins if stormy and low visibility
          
            epd.init()
            epd.sleep()
            
#        except Exception as e:
"""
            time.sleep(2)
            print("Error Occurred in Main While Loop")
            exception_type, exception_object, exception_traceback = sys.exc_info()
            filename = exception_traceback.tb_frame.f_code.co_filename
            line_number = exception_traceback.tb_lineno
            print(e)
            print("Exception type: ", exception_type)
            print("File name: ", filename)
            print("Line number: ", line_number)
            
            # Print to e-Paper that there is an error
            epd.init()
            epd.Clear()            
            display = Display()
            
            # If error caused because weather.gov server hiccuped, then display image and wait to retry
            if "properties" in str(e) or "index out of" in str(e) or "HTTPSConnectionPool" in str(e): # METAR not being provided
                display.draw_icon(70, 10, "b", 660, 470, "testpattern3")
                
            # Otherwise another processing error occured so we'll display the message on the e-paper
            else: 
                msg1 = "- Error Occurred -"
                msg2 = "One Moment While We Try Again..."    
            
                w, h = display.draw_black.textsize(msg1, font=font48)
                display.draw_black.text((400-(w/2), 170), msg1, fill=0, font=font48)
                w, h = display.draw_black.textsize(msg2, font=font24)            
                display.draw_red.text((400-(w/2), 230), msg2, fill=0, font=font24)
                
                display.draw_black.text((40, 340), str(e), fill=0, font=font24)
                display.draw_black.text((40, 370), str(exception_type), fill=0, font=font24)
                display.draw_black.text((40, 400), str(filename), fill=0, font=font24)
                display.draw_black.text((40, 430), "Line number: "+str(line_number), fill=0, font=font24)
            
            print("Printing Error info to E-Paper...")
            epd.display(epd.getbuffer(display.im_black), epd.getbuffer(display.im_red))
            print("Done")
            time.sleep(60) # Sets interval of updates. 60 = 1 minute
            epd.init()
            epd.sleep()          
"""