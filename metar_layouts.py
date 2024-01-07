# metar_layouts.py
# Layouts for Metar Display - Mark Harris
# Version 2.1
# Part of Epaper Display project found at; https://github.com/markyharris/metar/
#
# UPDATED FAA API 12-2023, https://aviationweather.gov/data/api/
#
# Each Layout offers a different look and amount of information.
# More can be created by starting at the bottom and pasting the following;
# ################
# #  Layout ?    #
# ################
# # My Own Created Layout
#  def layout?(display, metar, remarks, print_table, use_remarks):
#      # Get metar data along with flightcategory and related icon
#      decoded_airport,decoded_time,decoded_wndir,decoded_wnspd,decoded_wngust,decoded_vis,\
#      decoded_alt,decoded_temp,decoded_dew,decoded_cloudlayers,decoded_weather,decoded_rvr \
#      = decode_rawmessage(get_rawOb(metar))   
#      flightcategory, icon = flight_category(metar)
#      airport = decoded_airport
#
# Then using the other layouts as a guide create your own.
# You must add the name of your layout to 2 locations;
#   metar_main.py to the variable "layout_list"
#   metar.html to the '<select name="data_field2" id="myselection">' option list


# Imports
from metar_display import *
from metar_routines import *
from metar_settings import *
from datetime import datetime, timedelta
import random
import numpy as np


# Misc Variables
d = " " # d = delimiter used to split metar on 'spaces' then re-join them into 2 parts
cycle_num = 0
pref_cycle = 0

# Utility routines   
def center_line(display,text,font=font24b,pos_x=400):
    w, h = display.draw_black.textsize(text, font=font)
    return(pos_x-(w/2))

def last_update():
    now = datetime.now()
    last_update = "Last Updated at "+now.strftime("%I:%M %p") #, %m/%d/%Y"
    return(last_update)
 
def check_preferred_layout(layout_name):
    global preferred_flag
    preferred_flag = 0
    if use_preferred == 0:
        print('use_preferred = 0') # debug
        preferred_flag = False
        return(False)
    if layout_name in preferred_layouts:
        print('use_preferred = 1 and found in layout_list') # debug
        preferred_flag = True
        return(True)
    else:
        print('use_preferred = 1 and NOT in layout_list') # debug
        preferred_flag = False
        return(False)
    

###########################
#  Display IP Address -3  #
###########################
def disp_ip(display, ip_address):
    LINE0 = 120
    LINE1 = 220
    LINE2 = 300
    LINE3 = 350
    LINE4 = 420
    RADIUS = 20
    
    admin_url = "http://"+get_ip_address()+":5000"
    msg1 = "METAR Display will show within 60 seconds"
    
    display.round_line(40, 40, 725, 410, RADIUS, "r")
    display.draw_red.text((center_line(display,"For Admin URL, Enter:",font48b), LINE0), "For Admin URL, Enter:", fill=0, font=font48b)
    display.draw_black.text((center_line(display,admin_url,font36b), LINE1), admin_url, fill=0, font=font36b)
    display.draw_red.text((center_line(display,"Into a Web Browser",font36b), LINE2), "Into a Web Browser", fill=0, font=font36b)
    display.draw_red.text((center_line(display,"on Same Network",font36b), LINE3), "on Same Network", fill=0, font=font36b)
    display.draw_black.text((center_line(display,msg1,font16b), LINE4), msg1, fill=0, font=font16b)
    
    print('\nWeb Admin URL:',admin_url,'\n') # debug


###########################
#  Cycle Through Each -2  #
###########################
def cycle_layout(display,metar,remarks,print_table,use_remarks,use_disp_format,interval,wind_speed_units,cloud_layer_units,visibility_units,temperature_units,pressure_units,layout_list,preferred_layouts,use_preferred):
    global cycle_num
    global pref_cycle
#    print('use_preferred:',use_preferred) # debug
    
    if use_preferred == 1:        
        p_layouts_lst = [int(a) for a in str(preferred_layouts)]
        print('p_layouts_lst:',p_layouts_lst) # debug
           
        print('\033[96m!!! Preferred Layout:',p_layouts_lst[pref_cycle],' IN LIST !!!\033[0m')
        cycle_pick = layout_list[p_layouts_lst[pref_cycle]]           
        cycle_pick(display,metar,remarks,print_table,use_remarks,use_disp_format,interval,wind_speed_units,cloud_layer_units,visibility_units,temperature_units,pressure_units)
        pref_cycle += 1
        if pref_cycle == len(p_layouts_lst):
            pref_cycle = 0
                
    else:
        print('\033[91m--> cycle_num Layout:',cycle_num,'<--\033[0m') # debug
        cycle_pick = layout_list[cycle_num]
        cycle_pick(display,metar,remarks,print_table,use_remarks,use_disp_format,interval,wind_speed_units,cloud_layer_units,visibility_units,temperature_units,pressure_units)
        cycle_num += 1
        if cycle_num == len(layout_list):
            cycle_num = 0

    
##################
#  Randomize -1  #
##################
def random_layout(display,metar,remarks,print_table,use_remarks,use_disp_format,interval,wind_speed_units,cloud_layer_units,visibility_units,temperature_units,pressure_units,layout_list):
    rand_pick = random.choice(layout_list)
    print('\033[91m--> Random Layout:',str(rand_pick)[10:18],'<--\033[0m') # debug
    rand_pick(display,metar,remarks,print_table,use_remarks,use_disp_format,interval,wind_speed_units,cloud_layer_units,visibility_units,temperature_units,pressure_units)


################
#   Layout 0   #
################
# Simple large flight category and metar
def layout0(display,metar,remarks,print_table,use_remarks,use_disp_format,interval,wind_speed_units,cloud_layer_units,visibility_units,temperature_units,pressure_units):
    # Get metar data along with flightcategory and related icon
    decoded_airport,decoded_time,decoded_wndir,decoded_wnspd,decoded_wngust,decoded_vis,\
    decoded_alt,decoded_temp,decoded_dew,decoded_cloudlayers,decoded_weather,decoded_rvr \
    = decode_rawmessage(get_rawOb(metar))
    
    flightcategory, icon = flight_category(metar)
    airport = decoded_airport
   
    # Data layout for layout0 using pixels.
    # 0,0 in upper left hand corner. 800,480 in lower right corner
    LINE0 = 50
    LINE1 = 382
    LINE2 = 20
    COL1 = 20
    COL2 = 100
    
    # Create Grid box
    display.draw_red.rectangle((5, 5, 795, 475), fill=255, outline=0, width=5)
    display.draw_red.line((5, 380, 795, 380), fill=0, width=5)  # Horizontal 1

    # Flight Category    
    if flightcategory == "VFR":
        display.draw_black.rectangle((5, 5, 795, 380), fill=255, outline=0, width=10)
        display.draw_icon(680, LINE0-30, "r", 100, 100, icon)
        display.draw_black.text((COL1, LINE2), airport, fill=0, font=font48b)
        display.draw_black.text((center_line(display,flightcategory,font296b), LINE0), flightcategory, fill=0, font=font296b)
        display.draw_black.text((center_line(display,last_update(),font16b), LINE0+290), last_update(), fill=0, font=font16b)
    elif flightcategory == "MVFR":
        display.draw_black.rectangle((5, 5, 795, 380), fill=0, outline=0, width=10)
        display.draw_black.text((COL1, LINE2), airport, fill=255, font=font48b)
        display.draw_black.text((center_line(display,flightcategory,font296b), LINE0), flightcategory, fill=255, font=font296b)
        display.draw_black.text((center_line(display,last_update(),font16b), LINE0+290), last_update(), fill=255, font=font16b)
    elif flightcategory == "IFR":
        display.draw_red.rectangle((5, 5, 795, 380), fill=255, outline=0, width=10)
        display.draw_icon(680, LINE0-30, "r", 100, 100, icon)
        display.draw_red.text((COL1, LINE2), airport, fill=0, font=font48b)
        display.draw_red.text((center_line(display,flightcategory,font296b), LINE0), flightcategory, fill=0, font=font296b)
        display.draw_red.text((center_line(display,last_update(),font16b), LINE0+290), last_update(), fill=0, font=font16b)
    elif flightcategory == "LIFR":
        display.draw_red.rectangle((5, 5, 795, 380), fill=0, outline=0, width=10)
        display.draw_red.text((COL1, LINE2), airport, fill=255, font=font48b)
        display.draw_red.text((center_line(display,flightcategory,font296b), LINE0), flightcategory, fill=255, font=font296b)
        display.draw_red.text((center_line(display,last_update(),font16b), LINE0+290), last_update(), fill=255, font=font16b)
    else:
        display.draw_black.rectangle((5, 5, 795, 380), fill=255, outline=0, width=10)
        display.draw_black.text((COL1, LINE2), airport, fill=0, font=font48b)
        display.draw_black.text((center_line(display,flightcategory,font296b), LINE0), "N/A", fill=0, font=font296b)
        display.draw_black.text((center_line(display,last_update(),font16b), LINE0+290), last_update(), fill=0, font=font16b)

    # Display Raw METAR
    rawmetar = get_metartype(metar)+': '+get_rawOb(metar)
    w, h = display.draw_black.textsize(rawmetar, font=font24)
#    print(w, w/2, w/3) # debug

    if w/3 > 770:
        print("Raw Metar has 4 Lines") # debug
        rmline1 = d.join(rawmetar.split()[:9])
        rmline2 = d.join(rawmetar.split()[9:18])
        rmline3 = d.join(rawmetar.split()[18:27])
        rmline4 = d.join(rawmetar.split()[27:])
        display.draw_black.text((COL1, LINE1), rmline1, fill=0, font=font20)
        display.draw_black.text((COL1, LINE1+20), rmline2, fill=0, font=font20)
        display.draw_black.text((COL1, LINE1+40), rmline3, fill=0, font=font20)
        display.draw_black.text((COL1, LINE1+60), rmline4, fill=0, font=font20)
    elif w/2 > 770: # and w/3 > 770
        print("Raw Metar has 3 Lines") # debug
        rmline1 = d.join(rawmetar.split()[:8])
        rmline2 = d.join(rawmetar.split()[8:16])
        rmline3 = d.join(rawmetar.split()[16:])
        display.draw_black.text((COL1, LINE1), rmline1, fill=0, font=font24)
        display.draw_black.text((COL1, LINE1+30), rmline2, fill=0, font=font24)
        display.draw_black.text((COL1, LINE1+60), rmline3, fill=0, font=font24)
    elif w > 770: # w/2 < 770 and 
        print("Raw Metar has 2 Lines") # debug
        rmline1 = d.join(rawmetar.split()[:8])
        rmline2 = d.join(rawmetar.split()[8:])
        display.draw_black.text((COL1, LINE1+15), rmline1, fill=0, font=font24)
        display.draw_black.text((COL1, LINE1+45), rmline2, fill=0, font=font24)
    else:
        print("Raw Metar has 1 Lines") # debug
        display.draw_black.text((COL1, LINE1+30), rawmetar, fill=0, font=font24)


################
#   Layout 1   #
################
# Information with Icons and flight category in top row
#           display,metar,remarks,print_table,use_remarks,use_disp_format,interval,wind_speed_units,cloud_layer_units,visibility_units,temperature_units,pressure_units
def layout1(display,metar,remarks,print_table,use_remarks,use_disp_format,interval,wind_speed_units,cloud_layer_units,visibility_units,temperature_units,pressure_units):    
    # Get metar data along with flightcategory and related icon
    decoded_airport,decoded_time,decoded_wndir,decoded_wnspd,decoded_wngust,decoded_vis,\
    decoded_alt,decoded_temp,decoded_dew,decoded_cloudlayers,decoded_weather,decoded_rvr \
    = decode_rawmessage(get_rawOb(metar)) 
    
    flightcategory, icon = flight_category(metar)
    airport = decoded_airport
   
    # Data layout for layout1 using pixels.
    # 0,0 in upper left hand corner. 800,480 in lower right corner
    LINE0 = 10
    LINE1 = 80
    LINE2 = 110
    LINE3 = 170
    LINE4 = 230
    LINE5 = 290
    LINE6 = 350
    COL1 = 30
    COL2 = 545
    ICON_OFFSET = 175
    ICON_OFFSET1 = 30

    # Create Grid boxes
    display.draw_red.rectangle((5, 5, 795, 475), fill=255, outline=0, width=5)
    display.draw_red.line((5, 100, 795, 100), fill=0, width=5)  # Horizontal 1
    display.draw_red.line((5, 170, 795, 170), fill=0, width=1)  # Horizontal 2
    display.draw_red.line((5, 230, 276, 230), fill=0, width=1)  # Horizontal 3a
    display.draw_red.line((5, 290, 276, 290), fill=0, width=1)  # Horizontal 4a    
    display.draw_red.line((522, 230, 795, 230), fill=0, width=1)  # Horizontal 3b
    display.draw_red.line((522, 290, 795, 290), fill=0, width=1)  # Horizontal 4b
    display.draw_red.line((5, 350, 795, 350), fill=0, width=1)  # Horizontal 4
    display.draw_red.line((522, 100, 522, 350), fill=0, width=1)  # Vertical 1
    display.draw_red.line((276, 170, 276, 475), fill=0, width=1)  # Vertical 2

    # Flight Category
    if flightcategory == "VFR":
        display.draw_black.rectangle((276, 170, 522, 350), fill=255, outline=0, width=10)
        display.draw_black.text((center_line(display,flightcategory,font96b), 205), flightcategory, fill=0, font=font96b) 
    elif flightcategory == "MVFR":
        display.draw_black.rectangle((276, 170, 522, 350), fill=0, outline=0, width=10)
        display.draw_black.text((center_line(display,flightcategory,font96b), 205), flightcategory, fill=255, font=font96b)
    elif flightcategory == "IFR":
        display.draw_red.rectangle((276, 170, 522, 350), fill=255, outline=0, width=10)
        display.draw_red.text((center_line(display,flightcategory,font96b), 205), flightcategory, fill=0, font=font96b)
    elif flightcategory == "LIFR":
        display.draw_red.rectangle((276, 170, 522, 350), fill=0, outline=0, width=10)
        display.draw_red.text((center_line(display,flightcategory,font96b), 205), flightcategory, fill=255, font=font96b)    
    else:
        display.draw_black.rectangle((276, 170, 522, 350), fill=255, outline=0, width=10)
        display.draw_black.text((center_line(display,"N/A",font96b), 205), "N/A", fill=0, font=font96b) 

    # Display Raw METAR
    rawmetar = get_metartype(metar)+': '+ get_rawOb(metar) 
    w, h = display.draw_black.textsize(rawmetar, font=font24b)
#    print(w, w/2, w/3) # debug

    if w/3 > 770:
        print("Raw Metar has 4 Lines") # debug
        rmline1 = d.join(rawmetar.split()[:9])
        rmline2 = d.join(rawmetar.split()[9:18])
        rmline3 = d.join(rawmetar.split()[18:27])
        rmline4 = d.join(rawmetar.split()[27:])
        display.draw_black.text((COL1, LINE0), rmline1, fill=0, font=font20b)
        display.draw_black.text((COL1, LINE0+20), rmline2, fill=0, font=font20b)
        display.draw_black.text((COL1, LINE0+40), rmline3, fill=0, font=font20b)
        display.draw_black.text((COL1, LINE0+60), rmline4, fill=0, font=font20b)
    elif w/2 > 770: # and w/3 > 770
        print("Raw Metar has 3 Lines") # debug
        rmline1 = d.join(rawmetar.split()[:8])
        rmline2 = d.join(rawmetar.split()[8:16])
        rmline3 = d.join(rawmetar.split()[16:])
        display.draw_black.text((COL1, LINE0), rmline1, fill=0, font=font24b)
        display.draw_black.text((COL1, LINE0+30), rmline2, fill=0, font=font24b)
        display.draw_black.text((COL1, LINE0+60), rmline3, fill=0, font=font24b)
    elif w > 770: # w/2 < 770 and 
        print("Raw Metar has 2 Lines") # debug
        rmline1 = d.join(rawmetar.split()[:8])
        rmline2 = d.join(rawmetar.split()[8:])
        display.draw_black.text((COL1, LINE0+15), rmline1, fill=0, font=font24b)
        display.draw_black.text((COL1, LINE0+45), rmline2, fill=0, font=font24b)
    else:
        print("Raw Metar has 1 Lines") # debug
        display.draw_black.text((COL1, LINE0+30), rawmetar, fill=0, font=font24b)

    # Display Weather Description
    descript = get_wxstring(metar)

    display.draw_black.text((COL1, LINE2), "Weather:", fill=0, font=font24)    
    w, h = display.draw_black.textsize(descript, font=font24b)
    
    display.draw_black.text((COL1, LINE2+25), descript, fill=0, font=font24b)
    if (w+ICON_OFFSET1) < ICON_OFFSET:
        desc_icon_offset = ICON_OFFSET
    else:
        desc_icon_offset = w+ICON_OFFSET1
    
    if "Snow" in descript:
        display.draw_icon(COL1+desc_icon_offset, LINE2+5, "r", 50, 50, "snow")
    elif "Rain" in descript:
        display.draw_icon(COL1+desc_icon_offset, LINE2+5, "r", 50, 50, "umbrella")
    elif "Thunder" in descript:
        display.draw_icon(COL1+desc_icon_offset, LINE2+5, "r", 50, 50, "thunder")
    elif "Snow" in descript:
        display.draw_icon(COL1+desc_icon_offset, LINE2+5, "r", 50, 50, "windy1")
    elif "Smoke" in descript:
        display.draw_icon(COL1+desc_icon_offset, LINE2+5, "r", 50, 50, "factory")
    elif "Mist" in descript or "fog" in descript:
        display.draw_icon(COL1+desc_icon_offset, LINE2+5, "r", 50, 50, "mist")
    elif "Drizzle" in descript:
        display.draw_icon(COL1+desc_icon_offset, LINE2+5, "r", 50, 50, "drizzle")
    elif "Humidity" in descript:
        display.draw_icon(COL1+desc_icon_offset, LINE2+5, "r", 50, 50, "humidity")
    elif "Clear" in descript:
        display.draw_icon(COL1+desc_icon_offset, LINE2+5, "r", 50, 50, "rainbow")
    elif "Tornado" in descript:
        display.draw_icon(COL1+desc_icon_offset, LINE2+5, "r", 50, 50, "tornado")
    elif "Cloud" in descript:
        display.draw_icon(COL1+desc_icon_offset, LINE2+5, "r", 50, 50, "cloudy")
    else:
        display.draw_icon(COL1+desc_icon_offset, LINE2+5, "r", 50, 50, "sun")        
        
    # Display Temperature
    tempf,dis_unit = get_temp(metar,temperature_units)
        
    if float(tempf) >= 70:
        display.draw_icon(COL2+ICON_OFFSET, LINE2+5, "r", 50, 50, "hot")
    elif float(tempf) >= 40 and float(tempf) < 70:
        display.draw_icon(COL2+ICON_OFFSET, LINE2+5, "r", 50, 50, "mild")
    else:
        display.draw_icon(COL2+ICON_OFFSET, LINE2+5, "r", 50, 50, "cold")  
        
    display.draw_black.text((COL2, LINE2), "Temperature:\n"+tempf+dis_unit, fill=0, font=font24b)

    # Display Wind Direction
    winddir,winddir_raw = get_wdir(metar)

    display.draw_black.text((COL1, LINE3), "Wind Vector:\n"+winddir, fill=0, font=font24b)
    display.draw_icon(COL1+ICON_OFFSET, LINE3+5, "r", 50, 50, wind_arrow(winddir_raw))  

    # Display Wind Speed
    windsp,dis_unit = get_wspd(metar,wind_speed_units)

    if windsp == "Calm" or windsp == "n/a" or float(windsp) < 5.0:
        display.draw_icon(COL2+ICON_OFFSET, LINE3+5, "r", 50, 50, "windvanelow")
    elif float(windsp) >= 5.0 and float(windsp) < 15.0:
        display.draw_icon(COL2+ICON_OFFSET, LINE3+5, "r", 50, 50, "windvanemed")
    elif float(windsp) >= 15.0: 
        display.draw_icon(COL2+ICON_OFFSET, LINE3+5, "r", 50, 50, "windvanehigh")
      
    display.draw_black.text((COL2, LINE3), "Wind Speed:\n"+windsp+dis_unit, fill=0, font=font24b) 
        
    # Display Wind Gust Speed
    gustsp,dis_unit = get_wgst(metar,wind_speed_units)
          
    display.draw_black.text((COL1, LINE4), "Wind Gust:\n"+gustsp+dis_unit, fill=0, font=font24b)
    if gustsp == "n/a":
        display.draw_icon(COL1+ICON_OFFSET, LINE4+5, "r", 50, 50, "wind vane1")
    else:
        display.draw_icon(COL1+ICON_OFFSET, LINE4+5, "r", 50, 50, "windy1") 
    
    # Display Baro Pressure
    baro,dis_unit = get_altim(metar,pressure_units)

    if float(baro) >= 28.0 and float(baro) < 29.0:
        display.draw_icon(COL2+ICON_OFFSET, LINE4+5, "r", 50, 50, "baro0")  
    elif float(baro) >=29.0 and float(baro) < 29.5:
        display.draw_icon(COL2+ICON_OFFSET, LINE4+5, "r", 50, 50, "baro25")
    elif float(baro) >=29.5 and float(baro) < 30.0:
        display.draw_icon(COL2+ICON_OFFSET, LINE4+5, "r", 50, 50, "baro50")
    elif float(baro) >=30.0 and float(baro) < 30.5:
        display.draw_icon(COL2+ICON_OFFSET, LINE4+5, "r", 50, 50, "baro75")
    elif float(baro) >=30.5 and float(baro) < 31.0:
        display.draw_icon(COL2+ICON_OFFSET, LINE4+5, "r", 50, 50, "baro100")
        
    display.draw_black.text((COL2, LINE4), "Baro Press:\n"+baro+dis_unit, fill=0, font=font24b)    
        
    # Display Visibility
    vis,dis_unit = get_visib(metar,visibility_units)

    display.draw_black.text((COL1, LINE5), "Visibility:\n"+vis+dis_unit, fill=0, font=font24b)
    display.draw_icon(COL1+ICON_OFFSET, LINE5+5, "r", 50, 50, "vis")
        
    # Display Metar Type
    metartype = get_metartype(metar) # CHANGE This
     
    if metartype == None:
        metartype = 'n/a'    
    display.draw_black.text((COL2, LINE5), "Metar Type:\n"+metartype, fill=0, font=font24b)

    # Display Cloud Cover - Grab the first 3 layers of clouds being reported
    display.draw_black.text((COL1, LINE6), "Cloud Cover:\n", fill=0, font=font24b)
    
    cctype_lst,ccheight_lst,dis_unit = get_clouds(metar,cloud_layer_units)
    for i in range(len(cctype_lst)):
        cctype = cctype_lst[i]
        ccheight = ccheight_lst[i]

        if i == 3:
            break
        
        display.draw_black.text((COL1, LINE6+27+(27*i)), cctype+" "+ccheight+dis_unit, fill=0, font=font24b)
        if cctype == "OVC" or cctype == "VV": # Overcast
            display.draw_icon(COL1+ICON_OFFSET, LINE6+5+(27*i), "r", 50, 50, "cloud")      
        if cctype == "BKN": # Broken
            display.draw_icon(COL1+ICON_OFFSET, LINE6+5+(27*i), "r", 50, 50, "cloudy")
        if cctype == "SCT": # Scattered
            display.draw_icon(COL1+ICON_OFFSET, LINE6+5+(27*i), "r", 50, 50, "25_clouds")  
        if cctype == "FEW": # Few
            display.draw_icon(COL1+ICON_OFFSET, LINE6+5+(27*i), "r", 50, 50, "few_clouds") 
        if cctype == "SKC" or cctype == "CLR": # Sky Clear
            display.draw_icon(COL1+ICON_OFFSET, LINE6+5+(27*i), "r", 50, 50, "sun")        
     

    # Display Info box - Choose which info to display, airport or metar remarks   
    if use_remarks == 1:
        if len(print_table) < 10:
            for i in range(9-len(print_table)):
                print_table.append(" ")
#            print("!!!",remarks) # debug
#            print("!!!",print_table) # debug
            
        w, h = display.draw_black.textsize(remarks, font=font14b)
        if w > 450:
            remarks_pt1 = d.join(remarks.split()[:8])
            remarks_pt2 = d.join(remarks.split()[8:16])
            
            display.draw_red.text((286, LINE6+4), remarks_pt1, fill=0, font=font16b)
            display.draw_red.text((286, LINE6+26), remarks_pt2, fill=0, font=font16b)
            
        else:
            display.draw_black.text((286, LINE6+4), airport+" "+last_update(), fill=0, font=font16b)
            display.draw_red.text((286, LINE6+26), remarks, fill=0, font=font16b)
            
        display.draw_black.text((286, LINE6+44), print_table[0][:30], fill=0, font=font14b) 
        display.draw_black.text((540, LINE6+44), print_table[1][:30], fill=0, font=font14b) 

        display.draw_black.text((286, LINE6+62), print_table[2][:30], fill=0, font=font14b)
        display.draw_black.text((540, LINE6+62), print_table[3][:30], fill=0, font=font14b)

        display.draw_black.text((286, LINE6+80), print_table[4][:30], fill=0, font=font14b)
        display.draw_black.text((540, LINE6+80), print_table[5][:30], fill=0, font=font14b)

        display.draw_black.text((286, LINE6+98), print_table[6][:30], fill=0, font=font14b)
        display.draw_black.text((540, LINE6+98), print_table[7][:30], fill=0, font=font14b)
       
    else:
        icaoid,obstime,elev,lat,lon,name = get_misc(metar)
        display.draw_red.text((286, LINE6+4), airport+" "+last_update(), fill=0, font=font16b)
        display.draw_black.text((286, LINE6+26),"ICAO ID: " + icaoid, fill=0, font=font14b) 
        display.draw_black.text((286, LINE6+44), "Obs Time: " + str(obstime), fill=0, font=font14b)
        display.draw_black.text((286, LINE6+62), "Elevation: " + str(elev) +" ft", fill=0, font=font14b) # *3.28084
        display.draw_black.text((286, LINE6+80), "Coordinates: " + str(lat) + " " + str(lon), fill=0, font=font14b)
        display.draw_black.text((286, LINE6+98), "Info: " + name, fill=0, font=font14b)


################
#   Layout 2   #
################
# Information with Icons and flight category in the center
def layout2(display,metar,remarks,print_table,use_remarks,use_disp_format,interval,wind_speed_units,cloud_layer_units,visibility_units,temperature_units,pressure_units):
    # Get metar data along with flightcategory and related icon
    decoded_airport,decoded_time,decoded_wndir,decoded_wnspd,decoded_wngust,decoded_vis,\
    decoded_alt,decoded_temp,decoded_dew,decoded_cloudlayers,decoded_weather,decoded_rvr \
    = decode_rawmessage(get_rawOb(metar))
    
    flightcategory, icon = flight_category(metar)
    airport = decoded_airport

    # Data layout for layout2 using pixels.
    # 0,0 in upper left hand corner. 800,480 in lower right corner
    LINE0 = 10
    LINE1 = 80
    LINE2 = 110
    LINE3 = 170
    LINE4 = 230
    LINE5 = 290
    LINE6 = 350
    COL1 = 40
    COL2 = 410

    # Create Grid boxes
    display.draw_black.rectangle((5, 5, 795, 475), fill=255, outline=0, width=2) 
    display.draw_black.line((400, 110, 400, 475), fill=0, width=1)  # VERTICAL 1
    display.draw_red.line((5, 65, 795, 65), fill=0, width=3)    # Horizontal 0
    display.draw_black.line((5, 110, 795, 110), fill=0, width=1)  # Horizontal 1
    display.draw_black.line((5, 170, 795, 170), fill=0, width=1)  # Horizontal 2
    display.draw_black.line((5, 230, 795, 230), fill=0, width=1)  # Horizontal 3
    display.draw_black.line((5, 290, 795, 290), fill=0, width=1)  # Horizontal 4
    display.draw_black.line((5, 350, 795, 350), fill=0, width=1)  # Horizontal 4

    # Airport ID, Flight Category and Icon
    display.draw_black.text((COL1+3, LINE0+3), airport+" - "+flightcategory, fill=0, font=font48b)
    display.draw_red.text((COL1, LINE0), airport+" - "+flightcategory, fill=0, font=font48b)
    display.draw_icon( 378, LINE0+3, "b", 50, 50, icon)
    display.draw_icon( 375, LINE0, "r", 50, 50, icon)
    
#    display.draw_black.text((COL2+100, LINE0+10), last_update(), fill=0, font=font16b)
    
    # Display Raw METAR
    rawmetar = get_metartype(metar)+': '+ get_rawOb(metar) 
    w, h = display.draw_black.textsize(rawmetar)

    if w > 470:
        rmline1 = d.join(rawmetar.split()[:10])
        rmline2 = d.join(rawmetar.split()[10:])
        display.draw_black.text((COL1, LINE1-10), rmline1, fill=0, font=font16b)
        display.draw_black.text((COL1, LINE1+10), rmline2, fill=0, font=font16b)
    else:
        display.draw_black.text((COL1, LINE1), rawmetar, fill=0, font=font16b)
        
    # Display Weather Description
    descript = get_wxstring(metar)

    display.draw_black.text((COL1, LINE2), "Weather:", fill=0, font=font24b)    
    w, h = display.draw_black.textsize(descript)
#    print("Description Width = " + str(w)) # debug
    
    if w > 135:
        display.draw_black.text((COL1, LINE2+25), descript, fill=0, font=font16b)
    else:
        display.draw_black.text((COL1, LINE2+25), descript, fill=0, font=font24b)
    
    if "Snow" in descript:
        display.draw_icon(COL1+300, LINE2+5, "r", 50, 50, "snow")
    elif "Rain" in descript:
        display.draw_icon(COL1+300, LINE2+5, "r", 50, 50, "umbrella")
    elif "Thunder" in descript:
        display.draw_icon(COL1+300, LINE2+5, "r", 50, 50, "thunder")
    elif "Snow" in descript:
        display.draw_icon(COL1+300, LINE2+5, "r", 50, 50, "windy1")
    elif "Smoke" in descript:
        display.draw_icon(COL1+300, LINE2+5, "r", 50, 50, "factory")
    elif "Mist" in descript or "fog" in descript:
        display.draw_icon(COL1+300, LINE2+5, "r", 50, 50, "mist")
    elif "Drizzle" in descript:
        display.draw_icon(COL1+300, LINE2+5, "r", 50, 50, "drizzle")
    elif "Humidity" in descript:
        display.draw_icon(COL1+300, LINE2+5, "r", 50, 50, "humidity")
    elif "Clear" in descript:
        display.draw_icon(COL1+300, LINE2+5, "r", 50, 50, "rainbow")
    elif "Tornado" in descript:
        display.draw_icon(COL1+300, LINE2+5, "r", 50, 50, "tornado")
    elif "Cloud" in descript:
        display.draw_icon(COL1+300, LINE2+5, "r", 50, 50, "cloudy")
    else:
        display.draw_icon(COL1+300, LINE2+5, "r", 50, 50, "sun")        
        
    # Display Temperature
    tempf,dis_unit = get_temp(metar,temperature_units)
        
    if float(tempf) >= 70:
        display.draw_icon(COL2+300, LINE2+5, "r", 50, 50, "hot")
    elif float(tempf) >= 40 and float(tempf) < 70:
        display.draw_icon(COL2+300, LINE2+5, "r", 50, 50, "mild")
    else:
        display.draw_icon(COL2+300, LINE2+5, "r", 50, 50, "cold")  
        
    display.draw_black.text((COL2, LINE2), "Temperature:\n"+tempf+dis_unit, fill=0, font=font24b)

    # Display Wind Direction
    winddir,winddir_raw = get_wdir(metar)

    display.draw_black.text((COL1, LINE3), "Wind Direction:\n"+winddir, fill=0, font=font24b)
    display.draw_icon(COL1+300, LINE3+5, "r", 50, 50, wind_arrow(winddir_raw))  
#    print(wind_arrow(winddir_raw)) # debug

    # Display Wind Speed
    windsp,dis_unit = get_wspd(metar,wind_speed_units)

    display.draw_black.text((COL2, LINE3), "Wind Speed:\n"+windsp+dis_unit, fill=0, font=font24b) 
        
    # Display Wind Gust Speed
    gustsp,dis_unit = get_wgst(metar,wind_speed_units)

    display.draw_black.text((COL1, LINE4), "Wind Gust:\n"+gustsp+dis_unit, fill=0, font=font24b)
    if gustsp == "Not Present":
        display.draw_icon(COL1+300, LINE4+5, "r", 50, 50, "wind vane1")
    else:
        display.draw_icon(COL1+300, LINE4+5, "r", 50, 50, "windy1") 
    
    # Display Baro Pressure
    baro,dis_unit = get_altim(metar,pressure_units)
    
    if float(baro) >= 28.0 and float(baro) < 29.0:
        display.draw_icon(COL2+300, LINE4+5, "r", 50, 50, "baro0")  
    elif float(baro) >=29.0 and float(baro) < 29.5:
        display.draw_icon(COL2+300, LINE4+5, "r", 50, 50, "baro25")
    elif float(baro) >=29.5 and float(baro) < 30.0:
        display.draw_icon(COL2+300, LINE4+5, "r", 50, 50, "baro50")
    elif float(baro) >=30.0 and float(baro) < 30.5:
        display.draw_icon(COL2+300, LINE4+5, "r", 50, 50, "baro75")
    elif float(baro) >=30.5 and float(baro) < 31.0:
        display.draw_icon(COL2+300, LINE4+5, "r", 50, 50, "baro100")
        
    display.draw_black.text((COL2, LINE4), "Baro Pressure:\n"+baro+dis_unit, fill=0, font=font24b)    
        
    # Display Visibility
    vis,dis_unit = get_visib(metar,visibility_units)   

    display.draw_black.text((COL1, LINE5), "Visibility:\n"+vis+dis_unit, fill=0, font=font24b)
    display.draw_icon(COL1+300, LINE5+5, "r", 50, 50, "vis")
        
    # Display Metar Type
    metartype = get_metartype(metar) # CHANGE   
       
    if metartype == None:
        metartype = 'n/a'    
    display.draw_black.text((COL2, LINE5), "Metar Type:\n"+metartype, fill=0, font=font24b)

    # Display Cloud Cover - Grab the first 3 layers of clouds being reported
    display.draw_black.text((COL1, LINE6), "Cloud Cover:\n", fill=0, font=font24b)
    
    cctype_lst,ccheight_lst,dis_unit = get_clouds(metar,cloud_layer_units)
    for i in range(len(cctype_lst)):
        cctype = cctype_lst[i]
        ccheight = ccheight_lst[i]

        if i == 3:
            break
    
        display.draw_black.text((COL1, LINE6+27+(27*i)), cctype+" "+ccheight+dis_unit, fill=0, font=font24b)
        if cctype == "OVC" or cctype == "VV": # Overcast
            display.draw_icon(COL1+300, LINE6+5+(27*i), "r", 50, 50, "cloud")      
        if cctype == "BKN": # Broken
            display.draw_icon(COL1+300, LINE6+5+(27*i), "r", 50, 50, "cloudy")
        if cctype == "SCT": # Scattered
            display.draw_icon(COL1+300, LINE6+5+(27*i), "r", 50, 50, "25_clouds")  
        if cctype == "FEW": # Few
            display.draw_icon(COL1+300, LINE6+5+(27*i), "r", 50, 50, "few_clouds") 
        if cctype == "SKC" or cctype == "CLR": # Sky Clear
            display.draw_icon(COL1+300, LINE6+5+(27*i), "r", 50, 50, "sun")        
                                
    # Display Info box - Choose which info to display, airport or metar remarks
    if use_remarks == 1:
        if len(print_table) < 10:
            for i in range(9-len(print_table)):
                print_table.append(" ")
            
        w, h = display.draw_black.textsize(remarks, font=font14b)
        if w > 350:
            remarks_pt1 = d.join(remarks.split()[:4])
            remarks_pt2 = d.join(remarks.split()[4:8])
            
            display.draw_red.text((405, LINE6+4), remarks_pt1, fill=0, font=font16b)
            display.draw_red.text((405, LINE6+26), remarks_pt2, fill=0, font=font16b)
            
        else:
            display.draw_black.text((405, LINE6+4), airport+" "+last_update(), fill=0, font=font16b)
            display.draw_red.text((405, LINE6+26), remarks, fill=0, font=font16b)
            
        display.draw_black.text((405, LINE6+44), print_table[0][:22], fill=0, font=font14b) 
        display.draw_black.text((605, LINE6+44), print_table[1][:22], fill=0, font=font14b) 

        display.draw_black.text((405, LINE6+62), print_table[2][:22], fill=0, font=font14b)
        display.draw_black.text((605, LINE6+62), print_table[3][:22], fill=0, font=font14b)

        display.draw_black.text((405, LINE6+80), print_table[4][:22], fill=0, font=font14b)
        display.draw_black.text((605, LINE6+80), print_table[5][:22], fill=0, font=font14b)

        display.draw_black.text((405, LINE6+98), print_table[6][:22], fill=0, font=font14b)
        display.draw_black.text((605, LINE6+98), print_table[7][:22], fill=0, font=font14b)
       
    else:
        icaoid,obstime,elev,lat,lon,name = get_misc(metar)
        now = datetime.now()    
        display.draw_red.text((COL2, LINE6+4), "INFO: Updated " + now.strftime("%I:%M %p, %m/%d/%Y"), fill=0, font=font14b)
        display.draw_black.text((COL2, LINE6+22),"ICAO ID: " + icaoid, fill=0, font=font14b) 
        display.draw_black.text((COL2, LINE6+40), "Obs Time: " + str(obstime), fill=0, font=font14b)
        display.draw_black.text((COL2, LINE6+58), "Elevation: " + str(elev) +" ft", fill=0, font=font14b)
        display.draw_black.text((COL2, LINE6+76), "Coordinates: " + str(lat) + " " + str(lon), fill=0, font=font14b)
        display.draw_black.text((COL2, LINE6+94), "Info: " + name, fill=0, font=font14b)       


################ 
#   Layout 3   #
################
# Large flight category, no metar listed
def layout3(display,metar,remarks,print_table,use_remarks,use_disp_format,interval,wind_speed_units,cloud_layer_units,visibility_units,temperature_units,pressure_units):    
    # Get metar data along with flightcategory and related icon
    decoded_airport,decoded_time,decoded_wndir,decoded_wnspd,decoded_wngust,decoded_vis,\
    decoded_alt,decoded_temp,decoded_dew,decoded_cloudlayers,decoded_weather,decoded_rvr \
    = decode_rawmessage(get_rawOb(metar)) 
    
    icaoid,obstime,elev,lat,lon,name = get_misc(metar)
    
    flightcategory, icon = flight_category(metar)
    airport = decoded_airport
    
    print(get_rawOb(metar)) # debug
   
    # Data layout for layout3 using pixels.
    # 0,0 in upper left hand corner. 800,480 in lower right corner
    LINE0 = 100
    LINE1 = 15
    LINE2 = 445
    COL1 = 30
    COL2 = 100
    
    # Flight Category
    print(flightcategory) # debug
    
    if flightcategory == "VFR":
        display.round_line(25, 25, 755, 435, 20, "b")
        display.draw_black.text((center_line(display,airport,font48b), LINE1+5), airport, fill=0, font=font48b)
        display.draw_black.text((center_line(display,name,font24), LINE1+50), name, fill=0, font=font24)
        display.draw_black.text((center_line(display,flightcategory,font296b), LINE0), flightcategory, fill=0, font=font296b)
        display.draw_black.text((center_line(display,last_update(),font16b), LINE2), last_update(), fill=0, font=font16b)
    elif flightcategory == "MVFR":
        display.round_box(25, 25, 755, 435, 20, "b")
        display.draw_black.text((center_line(display,airport,font48b), LINE1+5), airport, fill=255, font=font48b)
        display.draw_black.text((center_line(display,name,font24), LINE1+50), name, fill=255, font=font24)
        display.draw_black.text((center_line(display,flightcategory,font296b), LINE0), flightcategory, fill=255, font=font296b)
        display.draw_black.text((center_line(display,last_update(),font16b), LINE2), last_update(), fill=255, font=font16b)
    elif flightcategory == "IFR":
        display.round_line(25, 25, 755, 435, 20, "r")
        display.draw_red.text((center_line(display,airport,font48b), LINE1+5), airport, fill=0, font=font48b)
        display.draw_red.text((center_line(display,name,font24), LINE1+50), name, fill=0, font=font24)
        display.draw_red.text((center_line(display,flightcategory,font296b), LINE0), flightcategory, fill=0, font=font296b)
        display.draw_red.text((center_line(display,last_update(),font16b), LINE2), last_update(), fill=0, font=font16b)
    elif flightcategory == "LIFR":
        display.round_box(25, 25, 755, 435, 20, "r")
        display.draw_red.text((center_line(display,airport,font48b), LINE1+5), airport, fill=255, font=font48b)
        display.draw_red.text((center_line(display,name,font24), LINE1+50), name, fill=255, font=font24)
        display.draw_red.text((center_line(display,flightcategory,font296b), LINE0), flightcategory, fill=255, font=font296b)
        display.draw_red.text((center_line(display,last_update(),font16b), LINE2), last_update(), fill=255, font=font16b)
    else:
        display.round_line(25, 25, 755, 435, 20, "b")
        display.draw_black.text((center_line(display,airport,font48b), LINE1+5), airport, fill=0, font=font48b)
        display.draw_black.text((center_line(display,name,font24), LINE1+50), name, fill=0, font=font24)
        display.draw_black.text((center_line(display,"N/A",font296b), LINE0), "N/A", fill=0, font=font296b)
        display.draw_black.text((center_line(display,last_update(),font16b), LINE2), last_update(), fill=0, font=font16b)


################
#   Layout 4   #
################
# 3 Area Layout with big flight category in lower right
def layout4(display,metar,remarks,print_table,use_remarks,use_disp_format,interval,wind_speed_units,cloud_layer_units,visibility_units,temperature_units,pressure_units):
    # Get metar data along with flightcategory and related icon
    decoded_airport,decoded_time,decoded_wndir,decoded_wnspd,decoded_wngust,decoded_vis,\
    decoded_alt,decoded_temp,decoded_dew,decoded_cloudlayers,decoded_weather,decoded_rvr \
    = decode_rawmessage(get_rawOb(metar)) 
    
    flightcategory, icon = flight_category(metar)
    airport = decoded_airport
   
    # Data layout for layout4 using pixels.
    # 0,0 in upper left hand corner. 800,480 in lower right corner
    LINE0 = 10
    LINE1 = 40
    LINE2 = 70
    LINE3 = 130
    LINE4 = 190
    LINE5 = 250
    LINE6 = 310
    LINE7 = 370
    LINE8 = 430
    LINE9 = 470
    LINE10 = 225 # Big Letters

    COL0 = 20
    COL1 = 225
    COL2 = 295
    COL3 = 480
    ICON_OFFSET = 200
    MARGIN = 5

    # Create Rounded solid boxes
    # up_left_x, up_left_y, box_width, box_height, radius, box_color="b"
    display.round_box(COL0+MARGIN, 25, COL1, 435, 20, "b") # Left Black
    display.round_box(COL2+MARGIN, 25, COL3, 115, 20, "r") # Upper Red
    
    # Create Info Separators
    display.draw_black.line((COL0+90, LINE2-8, COL1-55, LINE2-7), fill=255, width=2)    
    display.draw_circle(((COL2-COL0)/2)+3, LINE2-8, 5, "wb")    
    display.draw_black.line((COL0+90, LINE3-8, COL1-55, LINE3-7), fill=255, width=2)
    display.draw_circle(((COL2-COL0)/2)+3, LINE3-8, 5, "wb")    
    display.draw_black.line((COL0+90, LINE4-8, COL1-55, LINE4-7), fill=255, width=2)
    display.draw_circle(((COL2-COL0)/2)+3, LINE4-8, 5, "wb")    
    display.draw_black.line((COL0+90, LINE5-8, COL1-55, LINE5-7), fill=255, width=2)
    display.draw_circle(((COL2-COL0)/2)+3, LINE5-8, 5, "wb")    
    display.draw_black.line((COL0+90, LINE6-8, COL1-55, LINE6-7), fill=255, width=2)
    display.draw_circle(((COL2-COL0)/2)+3, LINE6-8, 5, "wb")    
    display.draw_black.line((COL0+90, LINE7-8, COL1-55, LINE7-7), fill=255, width=2)
    display.draw_circle(((COL2-COL0)/2)+3, LINE7-8, 5, "wb")    
    display.draw_black.line((COL0+90, LINE8-8, COL1-55, LINE8-7), fill=255, width=2)
    display.draw_circle(((COL2-COL0)/2)+3, LINE8-8, 5, "wb")
    
    # Flight Category
    print(flightcategory) # debug

    if flightcategory == "VFR":
        display.round_line(COL2+5,190,COL3,270,20,"b",0,5)
        display.draw_black.text((center_line(display,flightcategory,font196b,534), LINE10), flightcategory, fill=0, font=font196b) 
    elif flightcategory == "MVFR":
        display.round_box(COL2+5, 190, COL3, 270, 20, "b")
        display.draw_black.text((center_line(display,flightcategory,font196b,534), LINE10), flightcategory, fill=255, font=font196b)
    elif flightcategory == "IFR":
        display.round_line(COL2+5,190,COL3,270,20,"r",0,5)
        display.draw_red.text((center_line(display,flightcategory,font196b,534), LINE10), flightcategory, fill=0, font=font196b)
    elif flightcategory == "LIFR":
        display.round_box(COL2+5, 190, COL3, 270, 20, "r")
        display.draw_red.text((center_line(display,flightcategory,font196b,534), LINE10), flightcategory, fill=255, font=font196b)    
    else:
        display.round_line(COL2-5,190,COL3,270,20,"b",0,5)
        display.draw_black.text((center_line(display,"N/A",font196b,534), LINE10), "N/A", fill=0, font=font196b) 

    # Display Raw METAR
    rawmetar = get_metartype(metar)+': '+ get_rawOb(metar) 
    w, h = display.draw_black.textsize(rawmetar, font=font24)

    if w/3 > 500:
        print("Raw Metars has 4 Lines") # debug
        rmline1 = d.join(rawmetar.split()[:5])
        rmline2 = d.join(rawmetar.split()[5:11])
        rmline3 = d.join(rawmetar.split()[11:17])
        rmline4 = d.join(rawmetar.split()[17:])
        display.draw_red.text((COL2+5, LINE0), rmline1, fill=255, font=font24b)
        display.draw_red.text((COL2+5, LINE0+30), rmline2, fill=255, font=font24b)
        display.draw_red.text((COL2+5, LINE0+60), rmline3, fill=255, font=font24b)
        display.draw_red.text((COL2+5, LINE0+90), rmline4, fill=255, font=font24b)
    elif w/2 > 500: # and w/3 > 770
        print("Raw Metars has 3 Lines") # debug
        rmline1 = d.join(rawmetar.split()[:5])
        rmline2 = d.join(rawmetar.split()[5:11])
        rmline3 = d.join(rawmetar.split()[11:])
        display.draw_red.text((COL2+5, LINE0), rmline1, fill=255, font=font24b)
        display.draw_red.text((COL2+5, LINE0+30), rmline2, fill=255, font=font24b)
        display.draw_red.text((COL2+5, LINE0+60), rmline3, fill=255, font=font24b)
    elif w > 500: # w/2 < 770 and 
        print("Raw Metars has 2 Lines") # debug
        rmline1 = d.join(rawmetar.split()[:5])
        rmline2 = d.join(rawmetar.split()[5:])
        display.draw_red.text((COL2+5, LINE0), rmline1, fill=255, font=font24b)
        display.draw_red.text((COL2+5, LINE0+30), rmline2, fill=255, font=font24b)
    else:
        print("Raw Metars has 1 Lines") # debug
        display.draw_red.text((COL2+5, LINE0), rawmetar, fill=255, font=font24b)
        
    display.draw_red.text((center_line(display,last_update(),font16,534), LINE0+130), last_update(), fill=255, font=font16)

    # Display Airport ID andIcon
    # Display Weather Description
    descript = get_wxstring(metar)

    display.draw_black.text((COL0+5, LINE0), airport, fill=255, font=font48b)  
    
    if "Snow" in descript:
        display.draw_icon(COL0+ICON_OFFSET-5, LINE0+5, "wb", 50, 50, "snow")
    elif "Rain" in descript:
        display.draw_icon(COL0+ICON_OFFSET-5, LINE0+5, "wb", 50, 50, "umbrella")
    elif "Thunder" in descript:
        display.draw_icon(COL0+ICON_OFFSET-5, LINE0+5, "wb", 50, 50, "thunder")
    elif "Snow" in descript:
        display.draw_icon(COL0+ICON_OFFSET-5, LINE0+5, "wb", 50, 50, "windy1")
    elif "Smoke" in descript:
        display.draw_icon(COL0+ICON_OFFSET-5, LINE0+5, "wb", 50, 50, "factory")
    elif "Mist" in descript or "fog" in descript:
        display.draw_icon(COL0+ICON_OFFSET-5, LINE0+5, "wb", 50, 50, "mist")
    elif "Drizzle" in descript:
        display.draw_icon(COL0+ICON_OFFSET-5, LINE0+5, "wb", 50, 50, "drizzle")
    elif "Humidity" in descript:
        display.draw_icon(COL0+ICON_OFFSET-5, LINE0+5, "wb", 50, 50, "humidity")
    elif "Clear" in descript:
        display.draw_icon(COL0+ICON_OFFSET-5, LINE0+5, "wb", 50, 50, "rainbow")
    elif "Tornado" in descript:
        display.draw_icon(COL0+ICON_OFFSET-5, LINE0+5, "wb", 50, 50, "tornado")
    elif "Cloud" in descript:
        display.draw_icon(COL0+ICON_OFFSET-5, LINE0+5, "wb", 50, 50, "cloudy")
    else:
        display.draw_icon(COL0+ICON_OFFSET-5, LINE0+5, "wb", 50, 50, "sun")
        
    # Start weather info display list
    # Weather description
    display.draw_black.text((COL0+5, LINE2), "Weather:", fill=255, font=font24b)    
    display.draw_black.text((COL0+5, LINE2+25), descript, fill=255, font=font16b)
    
    # Display Temperature
    tempf,dis_unit = get_temp(metar,temperature_units)
        
    display.draw_black.text((COL0+5, LINE3), "Temperature:\n"+tempf+dis_unit, fill=255, font=font24b)

    # Display Wind Direction
    winddir,winddir_raw = get_wdir(metar)

    display.draw_black.text((COL0+5, LINE4), "Wind Vector:\n"+winddir, fill=255, font=font24b)   
    display.draw_icon(COL0+ICON_OFFSET-5, LINE4-3, "wb", 50, 50, wind_arrow(winddir_raw))  

    # Display Wind Speed
    windsp,dis_unit = get_wspd(metar,wind_speed_units)
        
    if windsp == "Calm" or windsp == "n/a" or float(windsp) < 5.0:
        display.draw_icon(COL0+ICON_OFFSET-5, LINE5-3, "wb", 50, 50, "windvanelow")
    elif float(windsp) >= 5.0 and float(windsp) < 15.0:
        display.draw_icon(COL0+ICON_OFFSET-5, LINE5-3, "wb", 50, 50, "windvanemed")
    elif float(windsp) >= 15.0: 
        display.draw_icon(COL0+ICON_OFFSET-5, LINE5-3, "wb", 50, 50, "windvanehigh")

    display.draw_black.text((COL0+5, LINE5), "Wind Speed:\n"+windsp+dis_unit, fill=255, font=font24b)
        
    # Display Wind Gust Speed
    gustsp,dis_unit = get_wgst(metar,wind_speed_units)

    display.draw_black.text((COL0+5, LINE6), "Wind Gust:\n"+gustsp+dis_unit, fill=255, font=font24b)

    # Display Visibility
    vis,dis_unit = get_visib(metar,visibility_units)
   
    display.draw_black.text((COL0+5, LINE7), "Visibility:\n"+vis+dis_unit, fill=255, font=font24b)
    
    # Display Cloud Cover
    # Grab the first layer of clouds being reported
    display.draw_black.text((COL0+5, LINE8), "Cloud Cover:\n", fill=255, font=font24b)
    
    cctype_lst,ccheight_lst,dis_unit = get_clouds(metar,cloud_layer_units)
    for i in range(len(cctype_lst)):
        cctype = cctype_lst[i]
        ccheight = ccheight_lst[i]

        if i == 3:
            break
    
        display.draw_black.text((COL0+5, LINE8+20), cctype+" "+ccheight+dis_unit, fill=255, font=font24b)
        
        cctype = cctype_lst[0]
        ccheight = ccheight_lst[0]

        if cctype == "OVC" or cctype == "VV": # Overcast
            display.draw_icon(COL0+ICON_OFFSET-5, LINE8-15, "wb", 50, 50, "cloud")      
        if cctype == "BKN": # Broken
            display.draw_icon(COL0+ICON_OFFSET-5, LINE8-15, "wb", 50, 50, "cloudy")
        if cctype == "SCT": # Scattered
            display.draw_icon(COL0+ICON_OFFSET-5, LINE8-15, "wb", 50, 50, "25_clouds")  
        if cctype == "FEW": # Few
            display.draw_icon(COL0+ICON_OFFSET-5, LINE8-15, "wb", 50, 50, "few_clouds") 
        if cctype == "SKC" or cctype == "CLR": # Sky Clear
            display.draw_icon(COL0+ICON_OFFSET-5, LINE8-15, "wb", 50, 50, "sun")        


################
#   Layout 5   #
################
# Multiple Airport Layout
def layout5(display,metar,remarks,print_table,use_remarks,use_disp_format,interval,wind_speed_units,cloud_layer_units,visibility_units,temperature_units,pressure_units):
    global airports_list
    global airport
    icaoid,obstime,elev,lat,lon,name = get_misc(metar)
    
    # Data layout for layout5.
    # 0,0 in upper left hand corner. 800,480 in lower right corner
    LINE0 = 10
    LINE1 = 100
    LINE2 = 190
    LINE3 = 280
    LINE4 = 370

    COL0 = 20
    COL1 = 290
    COL2 = 550
    COL3 = 810
    
    RADIUS = 10
    MARGIN = 5
    SPACING = (2*RADIUS)+MARGIN
    ICON_OFFSET = COL1-COL0-60
    
    # check and select the airports to display
    airports_list = []
    if len(random_airports) > 12:
        airports_list = random.sample(random_airports,12)
        airports_list.append(airport)
    elif len(random_airports) == 12:
        airports_list = random_airports
        airports_list.append(airport)
    elif len(random_airports) < 12:
        airports_list = random_airports
        for i in range(len(random_airports),13):
            airports_list.append(airport)
                        
    # Display box with airport and flight category. The box must be drawn first than the text
    # To create rounded corner box provide the following variables in this order   
    # up_left_x, up_left_y, box_width, box_height, radius, box_color    
    def print_box(airport, pos1_x, pos1_y, pos2_x, pos2_y):
        metar = Metar(airport)
        flightcategory, icon = flight_category(metar)
        output = airport+":"+flightcategory+" "
        w, h = display.draw_black.textsize(output, font=font36b)
        w_name, h_name = display.draw_black.textsize(name[:26], font=font14b)
        if flightcategory == "VFR":
            display.round_line(pos1_x, pos1_y, pos2_x-pos1_x-SPACING, pos2_y-pos1_y-SPACING, RADIUS, "b", 0, 3)
            display.draw_black.text(((pos2_x-pos1_x)/2-(w/2)+(pos1_x-COL0), (pos2_y-pos1_y)/2-(h/2)+(pos1_y-LINE0)-10), output, fill=0, font=font36b)
            display.draw_icon(pos1_x+ICON_OFFSET, pos1_y, "b", 30, 30, icon)
            display.draw_black.text(((pos2_x-pos1_x)/2-(w_name/2)+(pos1_x-COL0), pos1_y+50), name[:26], fill=0, font=font14b) 
        elif flightcategory == "MVFR":
            display.round_box(pos1_x, pos1_y, pos2_x-pos1_x-SPACING, pos2_y-pos1_y-SPACING, RADIUS, "b")
            display.draw_black.text(((pos2_x-pos1_x)/2-(w/2)+(pos1_x-COL0), (pos2_y-pos1_y)/2-(h/2)+(pos1_y-LINE0)-10), output, fill=255, font=font36b)
            display.draw_icon(pos1_x+ICON_OFFSET, pos1_y, "wb", 30, 30, icon)
            display.draw_black.text(((pos2_x-pos1_x)/2-(w_name/2)+(pos1_x-COL0), pos1_y+50), name[:26], fill=255, font=font14b) 
        elif flightcategory == "IFR":
            display.round_line(pos1_x, pos1_y, pos2_x-pos1_x-SPACING, pos2_y-pos1_y-SPACING, RADIUS, "r")
            display.draw_red.text(((pos2_x-pos1_x)/2-(w/2)+(pos1_x-COL0), (pos2_y-pos1_y)/2-(h/2)+(pos1_y-LINE0)-10), output, fill=0, font=font36b)
            display.draw_icon(pos1_x+ICON_OFFSET, pos1_y, "r", 30, 30, icon) 
            display.draw_red.text(((pos2_x-pos1_x)/2-(w_name/2)+(pos1_x-COL0), pos1_y+50), name[:26], fill=0, font=font14b) 
        elif flightcategory == "LIFR":
            display.round_box(pos1_x, pos1_y, pos2_x-pos1_x-SPACING, pos2_y-pos1_y-SPACING, RADIUS, "r")
            display.draw_red.text(((pos2_x-pos1_x)/2-(w/2)+(pos1_x-COL0), (pos2_y-pos1_y)/2-(h/2)+(pos1_y-LINE0)-10), output, fill=255, font=font36b)
            display.draw_icon(pos1_x+ICON_OFFSET, pos1_y, "wr", 30, 30, icon) 
            display.draw_red.text(((pos2_x-pos1_x)/2-(w_name/2)+(pos1_x-COL0), pos1_y+50), name[:26], fill=255, font=font14b) 
        else:
            display.round_line(pos1_x, pos1_y, pos2_x-pos1_x-SPACING, pos2_y-pos1_y-SPACING, RADIUS, "b")
            display.draw_red.text(((pos2_x-pos1_x)/2-(w/2)+(pos1_x-COL0), (pos2_y-pos1_y)/2-(h/2)+(pos1_y-LINE0)-10), output, fill=255, font=font36b)
            display.draw_icon(pos1_x+ICON_OFFSET, pos1_y, "wr", 30, 30, icon) 
            display.draw_red.text(((pos2_x-pos1_x)/2-(w_name/2)+(pos1_x-COL0), pos1_y+50),name[:26], fill=255, font=font14b) 

    # Column 1
    airport = airports_list[0]    
    print_box(airport, COL0, LINE0, COL1, LINE1)
    airport = airports_list[1]    
    print_box(airport, COL0, LINE1, COL1, LINE2)
    airport = airports_list[2]    
    print_box(airport, COL0, LINE2, COL1, LINE3)    
    airport = airports_list[3]    
    print_box(airport, COL0, LINE3, COL1, LINE4)

    # Column 2
    airport = airports_list[4]    
    print_box(airport, COL1, LINE0, COL2, LINE1)
    airport = airports_list[5]
    print_box(airport, COL1, LINE1, COL2, LINE2)
    airport = airports_list[6]
    print_box(airport, COL1, LINE2, COL2, LINE3)
    airport = airports_list[7]
    print_box(airport, COL1, LINE3, COL2, LINE4)

    # Column 3
    airport = airports_list[8]
    print_box(airport, COL2, LINE0, COL3, LINE1)
    airport = airports_list[9]
    print_box(airport, COL2, LINE1, COL3, LINE2)
    airport = airports_list[10]
    print_box(airport, COL2, LINE2, COL3, LINE3)
    airport = airports_list[11]
    print_box(airport, COL2, LINE3, COL3, LINE4)

    # Bottom Home Airport
    airport = airports_list[12]
    metar = Metar(airport)
    flightcategory, icon = flight_category(metar)
    output = airport+":"+flightcategory
        
    # Display Raw METAR
    icaoid,obstime,elev,lat,lon,name = get_misc(metar)
    rawmetar = get_metartype(metar)+': '+ get_rawOb(metar) 
    w, h = display.draw_black.textsize(rawmetar, font=font16b)

    if flightcategory == "VFR":
        display.round_line(COL0, LINE4, COL3-COL0-SPACING, 470-LINE4-MARGIN, RADIUS, "b")
        display.draw_black.text((COL0+10, LINE4+10), output, fill=0, font=font36b)
        display.draw_icon(COL0+ICON_OFFSET, LINE4+10, "b", 30, 30, icon)
        display.draw_black.text((COL0+10, LINE4+50), name[:26], fill=0, font=font14) 
        display.draw_black.text((COL0+10, LINE4+75), last_update(), fill=0, font=font16b) 

        if w/2 > 600: 
            print("Raw Metars has 3 Lines") # debug
            rmline1 = d.join(rawmetar.split()[:7])
            rmline2 = d.join(rawmetar.split()[7:14])
            rmline3 = d.join(rawmetar.split()[14:])
            display.draw_black.text((COL1, LINE4+5), rmline1, fill=0, font=font16b)
            display.draw_black.text((COL1, LINE4+25), rmline2, fill=0, font=font16b)
            display.draw_black.text((COL1, LINE4+45), rmline3, fill=0, font=font16b)
        elif w > 600: 
            print("Raw Metars has 2 Lines") # debug
            rmline1 = d.join(rawmetar.split()[:7])
            rmline2 = d.join(rawmetar.split()[7:])
            display.draw_black.text((COL1, LINE4+5), rmline1, fill=0, font=font16b)
            display.draw_black.text((COL1, LINE4+25), rmline2, fill=0, font=font16b)
        else:
            print("Raw Metars has 1 Lines") # debug
            display.draw_black.text((COL1, LINE4+5), rawmetar, fill=0, font=font16b)
            
    elif flightcategory == "MVFR":
        display.round_box(COL0, LINE4, COL3-COL0-SPACING, 470-LINE4-MARGIN, RADIUS, "b")
        display.draw_black.text((COL0+10, LINE4+10), output, fill=255, font=font36b)
        display.draw_icon(COL0+ICON_OFFSET, LINE4+10, "wb", 30, 30, icon)
        display.draw_black.text((COL0+10, LINE4+50), name[:26], fill=255, font=font14) 
        display.draw_black.text((COL0+10, LINE4+75), last_update(), fill=255, font=font16b) 

        if w/2 > 600: 
            print("Raw Metars has 3 Lines") # debug
            rmline1 = d.join(rawmetar.split()[:7])
            rmline2 = d.join(rawmetar.split()[7:14])
            rmline3 = d.join(rawmetar.split()[14:])
            display.draw_black.text((COL1, LINE4+5), rmline1, fill=255, font=font16b)
            display.draw_black.text((COL1, LINE4+25), rmline2, fill=255, font=font16b)
            display.draw_black.text((COL1, LINE4+45), rmline3, fill=255, font=font16b)
        elif w > 600: 
            print("Raw Metars has 2 Lines") # debug
            rmline1 = d.join(rawmetar.split()[:7])
            rmline2 = d.join(rawmetar.split()[7:])
            display.draw_black.text((COL1, LINE4+5), rmline1, fill=255, font=font16b)
            display.draw_black.text((COL1, LINE4+25), rmline2, fill=255, font=font16b)
        else:
            print("Raw Metars has 1 Lines") # debug
            display.draw_black.text((COL1, LINE4+5), rawmetar, fill=255, font=font16b)
            
    elif flightcategory == "IFR":
        display.round_line(COL0, LINE4, COL3-COL0-SPACING, 470-LINE4-MARGIN, RADIUS, "r")
        display.draw_red.text((COL0+10, LINE4+10), output, fill=0, font=font36b)
        display.draw_icon(COL0+ICON_OFFSET, LINE4+10, "r", 30, 30, icon)
        display.draw_red.text((COL0+10, LINE4+50), name[:26], fill=0, font=font14) 
        display.draw_red.text((COL0+10, LINE4+75), last_update(), fill=0, font=font16b)  

        if w/2 > 600: 
            print("Raw Metars has 3 Lines") # debug
            rmline1 = d.join(rawmetar.split()[:7])
            rmline2 = d.join(rawmetar.split()[7:14])
            rmline3 = d.join(rawmetar.split()[14:])
            display.draw_red.text((COL1, LINE4+5), rmline1, fill=0, font=font16b)
            display.draw_red.text((COL1, LINE4+25), rmline2, fill=0, font=font16b)
            display.draw_red.text((COL1, LINE4+45), rmline3, fill=0, font=font16b)
        elif w > 600: 
            print("Raw Metars has 2 Lines") # debug
            rmline1 = d.join(rawmetar.split()[:7])
            rmline2 = d.join(rawmetar.split()[7:])
            display.draw_red.text((COL1, LINE4+5), rmline1, fill=0, font=font16b)
            display.draw_red.text((COL1, LINE4+25), rmline2, fill=0, font=font16b)
        else:
            print("Raw Metars has 1 Lines") # debug
            display.draw_red.text((COL1, LINE4+5), rawmetar, fill=0, font=font16b)

    else:
        display.round_box(COL0, LINE4, COL3-COL0-SPACING, 470-LINE4-MARGIN, RADIUS, "r")
        display.draw_red.text((COL0+10, LINE4+10), output, fill=255, font=font36b)
        display.draw_icon(COL0+ICON_OFFSET, LINE4+10, "wr", 30, 30, icon)
        display.draw_red.text((COL0+10, LINE4+50), name[:26], fill=255, font=font14) 
        display.draw_red.text((COL0+10, LINE4+75), last_update(), fill=255, font=font16b) 

        if w/2 > 600: 
            print("Raw Metars has 3 Lines") # debug
            rmline1 = d.join(rawmetar.split()[:7])
            rmline2 = d.join(rawmetar.split()[7:14])
            rmline3 = d.join(rawmetar.split()[14:])
            display.draw_red.text((COL1, LINE4+5), rmline1, fill=255, font=font16b)
            display.draw_red.text((COL1, LINE4+25), rmline2, fill=255, font=font16b)
            display.draw_red.text((COL1, LINE4+45), rmline3, fill=255, font=font16b)
        elif w > 600: 
            print("2 Lines") # debug
            rmline1 = d.join(rawmetar.split()[:7])
            rmline2 = d.join(rawmetar.split()[7:])
            display.draw_red.text((COL1, LINE4+5), rmline1, fill=255, font=font16b)
            display.draw_red.text((COL1, LINE4+25), rmline2, fill=255, font=font16b)
        else:
            print("1 Lines") # debug
            display.draw_red.text((COL1, LINE4+5), rawmetar, fill=255, font=font16b)


############
# layout6  #
############
# Map with Flight Category
def layout6(display,metar,remarks,print_table,use_remarks,use_disp_format,interval,wind_speed_units,cloud_layer_units,visibility_units,temperature_units,pressure_units):
    decoded_airport,decoded_time,decoded_wndir,decoded_wnspd,decoded_wngust,decoded_vis,\
    decoded_alt,decoded_temp,decoded_dew,decoded_cloudlayers,decoded_weather,decoded_rvr \
    = decode_rawmessage(get_rawOb(metar))
    
    flightcategory, icon = flight_category(metar)
    airport = decoded_airport
    
    icaoid,obstime,elev,lat,lon,name = get_misc(metar)
    
    LINE0 = 40
    LINE1 = 90
    LINE2 = 5
    LINE3 = 25
    LINE4 = 85

    COL0 = 10
    COL1 = 250
    COL2 = 290
    COL3 = 810
    
    BOX_WIDTH = 295
    BOX_HEIGHT = 85
    RADIUS = 20
        
    output = airport+": "+flightcategory   
    print(lat, lon) # debug

    # Image URL is created using https://vfrmap.com/map_api.html
    url = "http://vfrmap.com/api?req=map&type=ifrlc&lat="+str(lat)+"&lon="+str(lon)+"&zoom=10&width=790&height=470&api_key=1234"
    display.show_pic(url, COL0, LINE2, "b")
    
    if flightcategory == "VFR":
        display.round_line(COL1, LINE3, BOX_WIDTH, BOX_HEIGHT, RADIUS, "b", 0, 3)
        display.draw_black.text((center_line(display,output,font48b), LINE0), output, fill=0, font=font48b)
        display.draw_black.text((center_line(display,last_update(),font16b), LINE1),last_update(), fill=0, font=font16b)
        
    elif flightcategory == "MVFR":
        display.round_box(COL1, LINE3, BOX_WIDTH, BOX_HEIGHT, RADIUS, "b", 0, 3)
        display.draw_black.text((center_line(display,output,font48b), LINE0), output, fill=255, font=font48b)
        display.draw_black.text((center_line(display,last_update(),font16b), LINE1), last_update(), fill=255, font=font16b)

    elif flightcategory == "IFR":
        display.round_line(COL1, LINE3, BOX_WIDTH, BOX_HEIGHT, RADIUS, "b", 0, 3) # Needed to blank out background
        display.round_line(COL1, LINE3, BOX_WIDTH, BOX_HEIGHT, RADIUS, "r", 0, 3)
        display.draw_red.text((center_line(display,output,font48b), LINE0), output, fill=0, font=font48b)
        display.draw_red.text((center_line(display,last_update(),font16b), LINE1), last_update(), fill=0, font=font16b)
        
    else:
        display.round_line(COL1, LINE3, BOX_WIDTH, BOX_HEIGHT, RADIUS, "b", 0, 3)
        display.round_box(COL1, LINE3, BOX_WIDTH, BOX_HEIGHT, RADIUS, "r", 0, 3)
        display.draw_red.text((center_line(display,output,font48b), LINE0), output, fill=255, font=font48b)
        display.draw_red.text((center_line(display,last_update(),font16b), LINE1), last_update(), fill=255, font=font16b)

        
############
# layout7  #
############
# Circles theme
def layout7(display,metar,remarks,print_table,use_remarks,use_disp_format,interval,wind_speed_units,cloud_layer_units,visibility_units,temperature_units,pressure_units):    
    def circle_points(r, n):
        circles = []
        for r, n in zip(r, n):
            t = np.linspace(0, 2*np.pi, n, endpoint=False)
            x = r * np.cos(t)
            y = r * np.sin(t)
            circles.append(np.c_[x, y])
        return circles
    
    def stars(x_pos, y_pos, radius, num_points, color):
        circles = circle_points([radius], [num_points])
        if color == "b":
            for circle in circles[0]:
                circle[0] = circle[0]+circle[0]+x_pos
                circle[1] = circle[1]+circle[1]+y_pos
                display.draw_black.line((x_pos, y_pos, circle[0], circle[1]), fill=0, width=2)
                display.draw_circle(circle[0], circle[1], 7, "b")
            display.draw_circle(x_pos, y_pos, 5, "b")
        else:
            for circle in circles[0]:
                circle[0] = circle[0]+circle[0]+x_pos
                circle[1] = circle[1]+circle[1]+y_pos
                display.draw_red.line((x_pos, y_pos, circle[0], circle[1]), fill=0, width=2)
                display.draw_circle(circle[0], circle[1], 7, "r")
            display.draw_circle(x_pos, y_pos, 4, "r")


    def center_text(text, font, x_pos, y_pos):
        w, h = display.draw_black.textsize(text, font=font)
        startx_pos = x_pos - (w/2)
        starty_pos = y_pos - (h/2)
        return(startx_pos, starty_pos)

    # Constants    
    HEIGHT = 480
    WIDTH = 800    
    CENTER_X = WIDTH/2
    CENTER_Y = HEIGHT/2
    
    RADIUS_OF_CIRCLES = 93
    NUM_OF_CIRCLES = 8
    OUTER_CIRCLES = []
    OUTER_CIRCLE_RADIUS = 53
    INNER_CIRCLE_RADIUS = 125
    
    CORNER_RADIUS = 75    
    CORNERS = [CORNER_RADIUS+10, CORNER_RADIUS+10,
               WIDTH-CORNER_RADIUS-20, CORNER_RADIUS+10,
               CORNER_RADIUS+10, HEIGHT-CORNER_RADIUS-10,
               WIDTH-CORNER_RADIUS-20, HEIGHT-CORNER_RADIUS-10] # 50,50, 750,50, 50,430,  750,430]
    
    decoded_airport,decoded_time,decoded_wndir,decoded_wnspd,decoded_wngust,decoded_vis,\
    decoded_alt,decoded_temp,decoded_dew,decoded_cloudlayers,decoded_weather,decoded_rvr \
    = decode_rawmessage(get_rawOb(metar)) 
    
    flightcategory, icon = flight_category(metar)
    airport = decoded_airport
    
    icaoid,obstime,elev,lat,lon,name = get_misc(metar)
    
    # Print star affectations
    stars(CORNERS[0], CENTER_Y, 12, 8, "r")
    stars(CORNERS[2], CENTER_Y, 12, 8, "r")

    # Draw outer circles
    # Routine from https://stackoverflow.com/questions/33510979/generator-of-evenly-spaced-points-in-a-circle-in-python
    r = [RADIUS_OF_CIRCLES] # Radius of outer circles
    n = [NUM_OF_CIRCLES] # Num of outer circles
    circles = circle_points(r, n)
    
    for circle in circles[0]:
        circle[0] = circle[0]+circle[0]+CENTER_X
        circle[1] = circle[1]+circle[1]+CENTER_Y
        OUTER_CIRCLES.append(circle)
        display.draw_circle_outline(circle[0], circle[1], OUTER_CIRCLE_RADIUS, 4, "r")

    # Draw Main inner circle and flight category
    if flightcategory == "VFR":
        display.draw_circle_outline(WIDTH/2, HEIGHT/2, INNER_CIRCLE_RADIUS, 4, "b")
        x_pos, y_pos = center_text(flightcategory, font96b, CENTER_X, CENTER_Y-10)
        display.draw_black.text((x_pos, y_pos), flightcategory, fill=0, font=font96b)
        
    elif flightcategory == "MVFR":
        display.draw_circle(WIDTH/2, HEIGHT/2, INNER_CIRCLE_RADIUS, "b")
        x_pos, y_pos = center_text(flightcategory, font96b, CENTER_X, CENTER_Y-10)
        display.draw_black.text((x_pos, y_pos), flightcategory, fill=255, font=font96b)

    elif flightcategory == "IFR":
        display.draw_circle_outline(WIDTH/2, HEIGHT/2, INNER_CIRCLE_RADIUS, 4, "r")
        x_pos, y_pos = center_text(flightcategory, font96b, CENTER_X, CENTER_Y-10)
        display.draw_red.text((x_pos, y_pos), flightcategory, fill=0, font=font96b)
        
    else:
        display.draw_circle(WIDTH/2, HEIGHT/2, INNER_CIRCLE_RADIUS, "r")
        x_pos, y_pos = center_text(flightcategory, font96b, CENTER_X, CENTER_Y-10)
        display.draw_red.text((x_pos, y_pos), flightcategory, fill=255, font=font96b)
    
    # Draw Corner Circles
    for i in range(0,len(CORNERS),2):
        display.draw_circle_outline(CORNERS[i], CORNERS[i+1], CORNER_RADIUS, 6, "b")    
    
    # Fill In Information
    # Airport in upper left corner
    x_pos, y_pos = center_text(airport, font48b, CORNERS[0], CORNERS[1]-5)
    display.draw_black.text((x_pos, y_pos), airport, fill=0, font=font48b)
    
    # Updated info in upper right corner
    x_pos, y_pos = center_text("Updated", font24b, CORNERS[2], CORNERS[3]-12)   
    display.draw_black.text((x_pos, y_pos), "Updated", fill=0, font=font24b)
    now = datetime.now()
    x_pos, y_pos = center_text(now.strftime("%I:%M %p"), font24b, CORNERS[2], CORNERS[3]+12)
    display.draw_black.text((x_pos, y_pos), now.strftime("%I:%M %p"), fill=0, font=font24b)
    
    # Airport name in lower left corner
    rmline1 = d.join(name.split()[:1])
    rmline2 = d.join(name.split()[1:2])
    rmline3 = d.join(name.split()[2:3])
    x_pos, y_pos = center_text(rmline1, font16b, CORNERS[4], CORNERS[5]-18)    
    display.draw_black.text((x_pos, y_pos), rmline1, fill=0, font=font16b)
    x_pos, y_pos = center_text(rmline2, font16b, CORNERS[4], CORNERS[5])    
    display.draw_black.text((x_pos, y_pos), rmline2, fill=0, font=font16b)
    x_pos, y_pos = center_text(rmline3, font16b, CORNERS[4], CORNERS[5]+18)    
    display.draw_black.text((x_pos, y_pos), rmline3, fill=0, font=font16b)
    
    # Lat/Lon of Airport in lower right corner
    x_pos, y_pos = center_text("Coordinates", font16b, CORNERS[6], CORNERS[7]-18) 
    display.draw_black.text((x_pos, y_pos), "Coordinates:", fill=0, font=font16b)
    x_pos, y_pos = center_text(str(lat), font16b, CORNERS[6], CORNERS[7]) 
    display.draw_black.text((x_pos, y_pos), str(lat), fill=0, font=font16b)
    x_pos, y_pos = center_text(str(lon), font16b, CORNERS[6], CORNERS[7]+18) 
    display.draw_black.text((x_pos, y_pos), str(lon), fill=0, font=font16b)
        
    # Display weather info in outer circles
    # Display Temperature
    tempf,dis_unit = get_temp(metar,temperature_units)
    
    x_pos, y_pos = center_text("Temp", font24b, OUTER_CIRCLES[0][0], OUTER_CIRCLES[0][1]-10) #OUTER_CIRCLES[0], OUTER_CIRCLES[1])
    display.draw_red.text((x_pos, y_pos), "Temp", fill=0, font=font24b)
    x_pos, y_pos = center_text(tempf, font24b, OUTER_CIRCLES[0][0], OUTER_CIRCLES[0][1]+10) #OUTER_CIRCLES[0], OUTER_CIRCLES[1])
    display.draw_red.text((x_pos, y_pos), tempf, fill=0, font=font24b)

    # Display Wind Direction
    winddir,winddir_raw = get_wdir(metar)
        
    x_pos, y_pos = center_text("Wind", font24b, OUTER_CIRCLES[1][0], OUTER_CIRCLES[1][1]-10)
    display.draw_red.text((x_pos, y_pos), "Wind", fill=0, font=font24b)
    x_pos, y_pos = center_text(winddir, font24b, OUTER_CIRCLES[1][0], OUTER_CIRCLES[1][1]+10)
    display.draw_red.text((x_pos, y_pos), winddir, fill=0, font=font24b)

    # Display Wind Speed
    windsp,dis_unit = get_wspd(metar,wind_speed_units)
        
    x_pos, y_pos = center_text("Speed", font24b, OUTER_CIRCLES[2][0], OUTER_CIRCLES[2][1]-10)
    display.draw_red.text((x_pos, y_pos), "Speed", fill=0, font=font24b) 
    x_pos, y_pos = center_text(windsp, font24b, OUTER_CIRCLES[2][0], OUTER_CIRCLES[2][1]+10)
    display.draw_red.text((x_pos, y_pos), windsp, fill=0, font=font24b) 
        
    # Display Wind Gust Speed
    gustsp,dis_unit = get_wgst(metar,wind_speed_units)
            
    x_pos, y_pos = center_text("Gust", font24b, OUTER_CIRCLES[3][0], OUTER_CIRCLES[3][1]-10)
    display.draw_red.text((x_pos, y_pos), "Gust", fill=0, font=font24b)
    x_pos, y_pos = center_text(gustsp+dis_unit, font24b, OUTER_CIRCLES[3][0], OUTER_CIRCLES[3][1]+10)
    display.draw_red.text((x_pos, y_pos), gustsp+dis_unit, fill=0, font=font24b)
    
    # Display Baro Pressure
    baro,dis_unit = get_altim(metar,pressure_units)
    
    x_pos, y_pos = center_text("Baro", font24b, OUTER_CIRCLES[4][0], OUTER_CIRCLES[4][1]-10)
    display.draw_red.text((x_pos, y_pos), "Baro", fill=0, font=font24b)    
    x_pos, y_pos = center_text(baro, font24b, OUTER_CIRCLES[4][0], OUTER_CIRCLES[4][1]+10)
    display.draw_red.text((x_pos, y_pos), baro, fill=0, font=font24b)    
        
    # Display Visibility
    vis,dis_unit = get_visib(metar,visibility_units)
        
    x_pos, y_pos = center_text("Vis", font24b, OUTER_CIRCLES[5][0], OUTER_CIRCLES[5][1]-10)
    display.draw_red.text((x_pos, y_pos), "Vis", fill=0, font=font24b)
    x_pos, y_pos = center_text(vis, font24b, OUTER_CIRCLES[5][0], OUTER_CIRCLES[5][1]+10)
    display.draw_red.text((x_pos, y_pos), vis, fill=0, font=font24b)
        
    # Display Metar Type
    metartype = get_metartype(metar)  
        
    if metartype == None:
        metartype = 'n/a'
        
    x_pos, y_pos = center_text("Type", font24b, OUTER_CIRCLES[6][0], OUTER_CIRCLES[6][1]-10)
    display.draw_red.text((x_pos, y_pos), "Type", fill=0, font=font24b)
    x_pos, y_pos = center_text(metartype, font24b, OUTER_CIRCLES[6][0], OUTER_CIRCLES[6][1]+10)
    display.draw_red.text((x_pos, y_pos), metartype, fill=0, font=font24b)

    # Grab the first layer of clouds being reported
    cctype_lst,ccheight_lst,dis_unit = get_clouds(metar,cloud_layer_units)
            
    ccheight = ccheight_lst[0]
    cctype = cctype_lst[0]
    
    if ccheight is None:
        ccheight = ""
    else:
        ccheight = str(ccheight) #  * 3.28084
    if cctype is None:
        cctype == "n/a"

    x_pos, y_pos = center_text(cctype, font24b, OUTER_CIRCLES[7][0], OUTER_CIRCLES[7][1]-10)
    display.draw_red.text((x_pos, y_pos), cctype, fill=0, font=font24b)
    x_pos, y_pos = center_text(ccheight, font24b, OUTER_CIRCLES[7][0], OUTER_CIRCLES[7][1]+10)
    display.draw_red.text((x_pos, y_pos), ccheight, fill=0, font=font24b)
        
    
############
# layout8  #
############
# Worst Weather by airport
def layout8(display,metar,remarks,print_table,use_remarks,use_disp_format,interval,wind_speed_units,cloud_layer_units,visibility_units,temperature_units,pressure_units):
    fc_ap_dict = {}
    vfr_dict,mvfr_dict,ifr_dict,lifr_dict = get_flightcat()

    # Data layout for layout8.
    # 0,0 in upper left hand corner. 800,480 in lower right corner
    LINE0 = 15
    LINE1 = 105
    LINE2 = 195
    LINE3 = 285
    LINE4 = 375
    LINE5 = 465

    COL0 = 20
    COL1 = 290
    COL2 = 550
    COL3 = 810
    
    RADIUS = 10
    MARGIN = 10
    SPACING = (2*RADIUS)+MARGIN
    ICON_OFFSET = COL1-COL0-65
    NUM_AIRPORTS = 15

    # Display box with airport and flight category. The box must be drawn first than the text
    # To create rounded corner box provide the following variables in this order   
    # up_left_x, up_left_y, box_width, box_height, radius, box_color    
    def print_box(flight_cat, airport, pos1_x, pos1_y, pos2_x, pos2_y):
        metar = Metar(airport)
        flightcategory = flight_cat
        icaoid,obstime,elev,lat,lon,name = get_misc(metar)
        output = airport+":"+flightcategory+" "
        w, h = display.draw_black.textsize(output, font=font36b)
        w_name, h_name = display.draw_black.textsize(name[:26], font=font14b)
        if flightcategory == "VFR":
            icon = "sun"
            display.round_line(pos1_x, pos1_y, pos2_x-pos1_x-SPACING, pos2_y-pos1_y-SPACING, RADIUS, "b", 0, 3)
            display.draw_black.text(((pos2_x-pos1_x)/2-(w/2)+(pos1_x-COL0), (pos2_y-pos1_y)/2-(h/2)+(pos1_y-LINE0)-10), output, fill=0, font=font36b)
            display.draw_icon(pos1_x+ICON_OFFSET, pos1_y, "b", 30, 30, icon)
            display.draw_black.text(((pos2_x-pos1_x)/2-(w_name/2)+(pos1_x-COL0), pos1_y+40), name[:26], fill=0, font=font14b) 
        elif flightcategory == "MVFR":
            icon = "25_clouds"
            display.round_box(pos1_x, pos1_y, pos2_x-pos1_x-SPACING, pos2_y-pos1_y-SPACING, RADIUS, "b")
            display.draw_black.text(((pos2_x-pos1_x)/2-(w/2)+(pos1_x-COL0), (pos2_y-pos1_y)/2-(h/2)+(pos1_y-LINE0)-10), output, fill=255, font=font36b)
            display.draw_icon(pos1_x+ICON_OFFSET, pos1_y, "wb", 30, 30, icon)
            display.draw_black.text(((pos2_x-pos1_x)/2-(w_name/2)+(pos1_x-COL0), pos1_y+40), name[:26], fill=255, font=font14b) 
        elif flightcategory == "IFR":
            icon = "thunder"
            display.round_line(pos1_x, pos1_y, pos2_x-pos1_x-SPACING, pos2_y-pos1_y-SPACING, RADIUS, "r")
            display.draw_red.text(((pos2_x-pos1_x)/2-(w/2)+(pos1_x-COL0), (pos2_y-pos1_y)/2-(h/2)+(pos1_y-LINE0)-10), output, fill=0, font=font36b)
            display.draw_icon(pos1_x+ICON_OFFSET, pos1_y, "r", 30, 30, icon) 
            display.draw_red.text(((pos2_x-pos1_x)/2-(w_name/2)+(pos1_x-COL0), pos1_y+40), name[:26], fill=0, font=font14b) 
        elif flightcategory == "LIFR":
            icon = "mist"
            display.round_box(pos1_x, pos1_y, pos2_x-pos1_x-SPACING, pos2_y-pos1_y-SPACING, RADIUS, "r")
            display.draw_red.text(((pos2_x-pos1_x)/2-(w/2)+(pos1_x-COL0), (pos2_y-pos1_y)/2-(h/2)+(pos1_y-LINE0)-10), output, fill=255, font=font36b)
            display.draw_icon(pos1_x+ICON_OFFSET, pos1_y, "wr", 30, 30, icon) 
            display.draw_red.text(((pos2_x-pos1_x)/2-(w_name/2)+(pos1_x-COL0), pos1_y+40), name[:26], fill=255, font=font14b) 
        else:
            display.round_line(pos1_x, pos1_y, pos2_x-pos1_x-SPACING, pos2_y-pos1_y-SPACING, RADIUS, "b")
            display.draw_red.text(((pos2_x-pos1_x)/2-(w/2)+(pos1_x-COL0), (pos2_y-pos1_y)/2-(h/2)+(pos1_y-LINE0)-10), output, fill=255, font=font36b)
            display.draw_icon(pos1_x+ICON_OFFSET, pos1_y, "wr", 30, 30, icon) 
            display.draw_red.text(((pos2_x-pos1_x)/2-(w_name/2)+(pos1_x-COL0), pos1_y+40), name[:26], fill=255, font=font14b) 

    # build dictionary
    if len(lifr_dict) > 0:
        for key, value in lifr_dict.items(): 
            fc_ap_dict[key] = value
        
    if len(ifr_dict) > 0:            
        for key, value in ifr_dict.items(): 
            fc_ap_dict[key] = value
        
    if len(mvfr_dict) > 0:                                
        for key, value in mvfr_dict.items(): 
            fc_ap_dict[key] = value
        
    if len(fc_ap_dict) < NUM_AIRPORTS:
        for key, value in vfr_dict.items():
            fc_ap_dict[key] = value
            if len(fc_ap_dict) >= NUM_AIRPORTS:
                break
    
    fc_ap_dict = dict(list(fc_ap_dict.items())[:NUM_AIRPORTS]) # Trim dict
    
    keys_ap = list(fc_ap_dict.keys())
    values_ap = list(fc_ap_dict.values())

    # Column 1
    airport, flight_cat = keys_ap[0], values_ap[0]    
    print_box(flight_cat, airport, COL0, LINE0, COL1, LINE1)
    airport, flight_cat = keys_ap[1], values_ap[1]    
    print_box(flight_cat, airport, COL0, LINE1, COL1, LINE2)
    airport, flight_cat = keys_ap[2], values_ap[2]    
    print_box(flight_cat, airport, COL0, LINE2, COL1, LINE3)    
    airport, flight_cat = keys_ap[3], values_ap[3]    
    print_box(flight_cat, airport, COL0, LINE3, COL1, LINE4)
    airport, flight_cat = keys_ap[4], values_ap[4]    
    print_box(flight_cat, airport, COL0, LINE4, COL1, LINE5)

    # Column 2
    airport, flight_cat = keys_ap[5], values_ap[5]    
    print_box(flight_cat, airport, COL1, LINE0, COL2, LINE1)
    airport, flight_cat = keys_ap[6], values_ap[6]
    print_box(flight_cat, airport, COL1, LINE1, COL2, LINE2)
    airport, flight_cat = keys_ap[7], values_ap[7]
    print_box(flight_cat, airport, COL1, LINE2, COL2, LINE3)
    airport, flight_cat = keys_ap[8], values_ap[8]
    print_box(flight_cat, airport, COL1, LINE3, COL2, LINE4)
    airport, flight_cat = keys_ap[9], values_ap[9]
    print_box(flight_cat, airport, COL1, LINE4, COL2, LINE5)

    # Column 3
    airport, flight_cat = keys_ap[10], values_ap[10]
    print_box(flight_cat, airport, COL2, LINE0, COL3, LINE1)
    airport, flight_cat = keys_ap[11], values_ap[11]
    print_box(flight_cat, airport, COL2, LINE1, COL3, LINE2)
    airport, flight_cat = keys_ap[12], values_ap[12]
    print_box(flight_cat, airport, COL2, LINE2, COL3, LINE3)
    airport, flight_cat = keys_ap[13], values_ap[13]
    print_box(flight_cat, airport, COL2, LINE3, COL3, LINE4)
    airport, flight_cat = keys_ap[14], values_ap[14]
    print_box(flight_cat, airport, COL2, LINE4, COL3, LINE5)
    
#    now = datetime.now()
#    next_update = now + timedelta(0,int(interval)) # days, seconds
#    next_update_text = "Next Update at "+next_update.strftime("%I:%M %p, %m/%d/%Y")
#    w_upd, h_upd = display.draw_black.textsize(next_update_text, font=font20b)       
    display.draw_black.text((center_line(display,last_update(),font20b), 460), last_update(), fill=0, font=font20b)


################
#   Layout 9   #
################
# Metar with Large Winds Icons
def layout9(display,metar,remarks,print_table,use_remarks,use_disp_format,interval,wind_speed_units,cloud_layer_units,visibility_units,temperature_units,pressure_units):    
    # Get metar data along with flightcategory and related icon
    decoded_airport,decoded_time,decoded_wndir,decoded_wnspd,decoded_wngust,decoded_vis,\
    decoded_alt,decoded_temp,decoded_dew,decoded_cloudlayers,decoded_weather,decoded_rvr \
    = decode_rawmessage(get_rawOb(metar)) 
    
    flightcategory, icon = flight_category(metar)
    airport = decoded_airport
    icaoid,obstime,elev,lat,lon,name = get_misc(metar)
   
    # Data layout for layout9 using pixels.
    # 0,0 in upper left hand corner. 800,480 in lower right corner
    LINE0 = 50
    LINE1 = 10
    LINE2 = 20
    LINE3 = 463
    LINE4 = 450
    LINE5 = 110
    
    COL1 = 5
    COL2 = 405
    
    ICON_OFFSET = 45
    ICON_SIZE = 300
    
    # Create Grid box
    display.draw_red.rectangle((5, 5, 795, 460), fill=255, outline=0, width=5)
    display.draw_red.line((5, 100, 795, 100), fill=0, width=5)  
    display.draw_red.line((400, 100, 400, 460), fill=0, width=5)  

    # Flight Category
    print(flightcategory) # debug
    display.draw_black.text((center_line(display,last_update(),font16b), LINE3), last_update(), fill=0, font=font16b)

    # Display Raw METAR
    rawmetar = get_metartype(metar)+': '+ get_rawOb(metar) 
    w, h = display.draw_black.textsize(rawmetar, font=font24)

    if w/3 > 770:
        print("Raw Metars has 4 Lines") # debug
        rmline1 = d.join(rawmetar.split()[:9])
        rmline2 = d.join(rawmetar.split()[9:18])
        rmline3 = d.join(rawmetar.split()[18:27])
        rmline4 = d.join(rawmetar.split()[27:])
        display.draw_black.text((COL1+10, LINE1), rmline1, fill=0, font=font20)
        display.draw_black.text((COL1+10, LINE1+20), rmline2, fill=0, font=font20)
        display.draw_black.text((COL1+10, LINE1+40), rmline3, fill=0, font=font20)
        display.draw_black.text((COL1+10, LINE1+60), rmline4, fill=0, font=font20)
    elif w/2 > 770: # and w/3 > 770
        print("Raw Metars has 3 Lines") # debug
        rmline1 = d.join(rawmetar.split()[:8])
        rmline2 = d.join(rawmetar.split()[8:16])
        rmline3 = d.join(rawmetar.split()[16:])
        display.draw_black.text((COL1+10, LINE1), rmline1, fill=0, font=font24)
        display.draw_black.text((COL1+10, LINE1+30), rmline2, fill=0, font=font24)
        display.draw_black.text((COL1+10, LINE1+60), rmline3, fill=0, font=font24)
    elif w > 770: # w/2 < 770 and 
        print("Raw Metars has 2 Lines") # debug
        rmline1 = d.join(rawmetar.split()[:8])
        rmline2 = d.join(rawmetar.split()[8:])
        display.draw_black.text((COL1+10, LINE1+15), rmline1, fill=0, font=font24)
        display.draw_black.text((COL1+10, LINE1+45), rmline2, fill=0, font=font24)
    else:
        print("Raw Metars has 1 Lines") # debug
        display.draw_black.text((COL1+10, LINE1+30), rawmetar, fill=0, font=font24)

    # Display Wind Direction
    winddir,winddir_raw = get_wdir(metar)

    wind_txt = "Wind Direction:"+winddir
    display.draw_black.text((center_line(display,wind_txt,font24b,600), LINE4-25), wind_txt, fill=0, font=font24b)
    display.draw_icon(COL2+ICON_OFFSET, LINE5, "r", ICON_SIZE, ICON_SIZE, wind_arrow(winddir_raw))  

    # Display Wind Speed
    windsp,dis_unit = get_wspd(metar,wind_speed_units)

    if windsp == "Calm" or windsp == "n/a" or float(windsp) < 5.0:
        display.draw_icon(COL1+ICON_OFFSET, LINE5, "r", ICON_SIZE, ICON_SIZE, "windvanelow")
    elif float(windsp) >= 5.0 and float(windsp) < 15.0:
        display.draw_icon(COL1+ICON_OFFSET, LINE5, "r", ICON_SIZE, ICON_SIZE, "windvanemed")
    elif float(windsp) >= 15.0: 
        display.draw_icon(COL1+ICON_OFFSET, LINE5, "r", ICON_SIZE, ICON_SIZE, "windvanehigh")
        
    # Display Wind Gust Speed
    gustsp,dis_unit = get_wgst(metar,wind_speed_units)
    if gustsp == 'n/a':
        gustsp = ''
        windsp,dis_unit = get_wspd(metar,wind_speed_units)
    else:
        windsp = windsp + ' G'
            
    windsp_txt = "Speed:"+windsp+gustsp+dis_unit
    display.draw_black.text((center_line(display,windsp_txt,font24b,200), LINE4-25), windsp_txt, fill=0, font=font24b)

#################
# test layout10 #
#################
# used for testing/playing. Not part of the available layouts
def layout10(display,metar,remarks,print_table,use_remarks,use_disp_format,interval,wind_speed_units,cloud_layer_units,visibility_units,temperature_units,pressure_units):
    # Get metar data along with flightcategory and related icon
    decoded_airport,decoded_time,decoded_wndir,decoded_wnspd,decoded_wngust,decoded_vis,\
    decoded_alt,decoded_temp,decoded_dew,decoded_cloudlayers,decoded_weather,decoded_rvr \
    = decode_rawmessage(get_rawOb(metar))   
    flightcategory, icon = flight_category(metar)
    airport = decoded_airport
    icaoid,obstime,elev,lat,lon,name = get_misc(metar)
    print(lat,lon)

    chart_url = "https://forecast.weather.gov/meteograms/Plotter.php?lat=37.431&lon=-122.253&wfo=MTR&zcode=CAZ508&gset=18&gdiff=3&unit=0&tinfo=PY8&ahour=0&pcmd=11011111000000000000000000000000000000000000000000000000000&lg=en&indu=1!1!1!&dd=1&bw=1&hrspan=48&pqpfhr=6&psnwhr=6"
    display.show_pic(chart_url, 2, 2, "b") # COL0, LINE2, "b")

