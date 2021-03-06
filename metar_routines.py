# metar_routines.py
# Metar Decoding Routines - Mark Harris

# Imports
from metar_remarks import *
import urllib.request, urllib.error, urllib.parse
import xml.etree.ElementTree as ET
import socket

# Misc Variables
decode = []      # used to decode the raw metar
print_table = [] # Store decoded remark definitions to display
remarks = ""     # Build remarks string to display

# Class Bravo airports used to find bad weather to display on Multiple Airports Layout5
class_b = ["KPHX", "KLAX", "KNKX", "KSAN", "KSFO", "KDEN", "KMCO", "KMIA", "KTPA", "KATL", \
           "PHNL", "KORD", "KCVG", "KMSY", "KADW", "KBWI", "KBOS", "KDTW", "KMSP", "KMCI", \
           "KSTL", "KLAS", "KLSV", "KEWR", "KJFK", "KLGA", "KCLT", "KCLE", "KPHL", "KPIT", \
           "KMEM", "KDAL", "KDFW", "KHOU", "KIAH", "KSLC", "KDCA", "KIAD", "KSEA"]

# Class Charlie airports used to find bad weather to display on Multiple Airports Layout5
class_c = ['KBHM', 'KHSV', 'KMOB', 'PANC', 'KDMA', 'KTUS', 'KLIT', 'KXNA', 'KBAB', 'KBUR', \
           'KFAT', 'KMRY', 'KOAK', 'KONT', 'KRIV', 'KSBA', 'KSJC', 'KSMF', 'KSNA', 'KCOS', \
           'KBDL', 'KDAB', 'KFLL', 'KJAX', 'KNDZ', 'KNPA', 'KNSE', 'KPBI', 'KPNS', 'KRSW', \
           'KSFB', 'KSRQ', 'KTLH', 'KSAV', 'PHOG', 'KBOI', 'KCMI', 'KMDW', 'KMLI', 'KPIA', \
           'KSPI', 'KEVV', 'KFWA', 'KIND', 'KSBN', 'KCID', 'KDSM', 'KICT', 'KLEX', 'KSDF', \
           'KBAD', 'KBTR', 'KLFT', 'KSHV', 'KBGR', 'KPWM', 'KFNT', 'KGRR', 'KLAN', 'KCBM', \
           'KJAN', 'KSGF', 'KBIL', 'KLNK', 'KOFF', 'KOMA', 'KRNO', 'KMHT', 'KACY', 'KABQ', \
           'KALB', 'KBUF', 'KISP', 'KROC', 'KSYR', 'KAVL', 'KFAY', 'KGSO', 'KPOB', 'KRDU', \
           'KCAK', 'KCMH', 'KDAY', 'KTOL', 'KOKC', 'KTIK', 'KTUL', 'KPDX', 'KABE', 'KPVD', \
           'KCAE', 'KCHS', 'KGSP', 'KMYR', 'KSSC', 'KBNA', 'KCHA', 'KTYS', 'KABI', 'KAMA', \
           'KAUS', 'KCRP', 'KDLF', 'KDYS', 'KELP', 'KHRL', 'KLBB', 'KMAF', 'KSAT', 'KBTV', \
           'KORF', 'KRIC', 'KROA', 'KGEG', 'KNUW', 'KSKA', 'KCRW', 'KGRB', 'KMKE', 'KMSN', \
           'TJSJ', 'TIST']
        
# Get RPi IP address to display on Boot up.
def get_ip_address():
    ip_address = '';
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8",80))
    ip_address = s.getsockname()[0]
    s.close()
#    print(ip_address) # debug
    return ip_address

# Get Flight Categories for Class B and Class C airports
def get_flightcat():
    # api url
    url = "https://www.aviationweather.gov/adds/dataserver_current/httpparam?dataSource=metars&requestType=retrieve&format=xml&mostRecentForEachStation=constraint&hoursBeforeNow=2.5&stationString="

    fc_dict = {}
    vfr_dict = {}
    mvfr_dict = {}
    ifr_dict = {}
    lifr_dict = {}

    # Build URL with class b and class c airports
    for ap in class_b:
        url = url+ap+","
    for ap in class_c:
        url = url+ap+","
        
    content = urllib.request.urlopen(url).read()
    root = ET.fromstring(content) #Process XML data returned from FAA
    for data in root.iter('data'):
            num_results = data.attrib['num_results']
            print(num_results)
            
    for metar in root.iter('METAR'):
        stationId = metar.find('station_id').text
        flightcategory = metar.find('flight_category').text
        fc_dict[stationId] = flightcategory
        
    for key in fc_dict:
        if "MVFR" in fc_dict[key]:
            mvfr_dict[key] = "MVFR"
        elif "IFR" in fc_dict[key]:
            ifr_dict[key] = "IFR"
        elif "LIFR" in fc_dict[key]:
            lifr_dict[key] = "LIFR"
        else:
            vfr_dict[key] = "VFR"

    return(vfr_dict,mvfr_dict,ifr_dict,lifr_dict)
    
    
# Decodes the flight category from the raw metar string
def flight_category(metar):
    flightcategory = "VFR"
    icon = "sun"
    vis_in_miles = round(metar.data["properties"]["visibility"]["value"]*3.28084/5280, 1)
#    print(vis_in_miles) # debug
      
    for i in range(len(metar.data["properties"]["cloudLayers"])):
        sky_condition = metar.data["properties"]["cloudLayers"][i]["amount"]
#        print("sky_condition: "+sky_condition) # debug
        
        if metar.data["properties"]["cloudLayers"][i]["base"]["value"] != None:
            sky_ceiling = metar.data["properties"]["cloudLayers"][i]["base"]["value"]*3.28084
        else:
            sky_ceiling = 0
            
        if sky_condition == "OVC" or sky_condition == "BKN" or sky_condition == "OVX" or sky_condition == "VV":                 
            if sky_ceiling < 500:
                flightcategory = "LIFR"
                icon = "mist"
            elif sky_ceiling >= 500 and sky_ceiling < 1000:
                flightcategory = "IFR"
                icon = "thunder"
            elif sky_ceiling >= 1000 and sky_ceiling <= 3000:
                flightcategory = "MVFR"
                icon = "25_clouds"                
            elif sky_ceiling > 3000:
                flightcategory = "VFR"
                icon = "sun"
            if flightcategory != "VFR":
                break                               
        
    if flightcategory != "LIFR":
        if vis_in_miles < 1:
            flightcategory = "LIFR"
            icon = "mist"
        elif vis_in_miles >= 1.0 and vis_in_miles < 3.0:
            flightcategory = "IFR"
            icon = "thunder"
        elif vis_in_miles >= 3.0 and vis_in_miles <= 5.0:
            flightcategory = "MVFR" 
            icon = "25_clouds"      

    return (flightcategory, icon)  


# Decode Remarks
def decode_remarks(rawmessage):
    rmk = 0
    test_decode = []
    print_table_tmp = []
    remarks_tmp = "REMARKS:"  # Build remarks string to display

    test_decode = rawmessage.split() # separate metar into a list

    for i in range(len(test_decode)): # Find the start of the remarks section
        if test_decode[i] == "RMK":
            rmk = i
            break
     
    for i in range(rmk+1,len(test_decode)):
        remarks_tmp = remarks_tmp + " " + test_decode[i]
            
    for key in metar_remarks: # Check each remark code available 
        for i in range(rmk+1,len(test_decode)):
            if test_decode[i].startswith(key):
       
                if len(key) == len(test_decode[i]) or test_decode[i][len(key):].isdigit(): # Grab 1 field remarks for key
                    key1 = test_decode[i].strip()+":"
                    data1 = metar_remarks[key].strip()
                    print_table_tmp.append(key1+" "+data1)
                    
#    print(remarks_tmp, print_table) # Debug
    return (remarks_tmp, print_table_tmp)



# Provides the proper icon to display depending on wind direction
def wind_arrow(deg):
    if deg == "000" or deg == "VRB":
        arrow = "compass"
        return arrow
    deg = int(deg)
    if deg < 30 or deg >= 330:
        arrow = "north"
    elif 30 <= deg < 60: 
        arrow = "northeast"
    elif 60 <= deg < 120:
        arrow = "east"
    elif 120 <= deg < 150:
        arrow = "southeast"
    elif 150 <= deg < 210:
        arrow = "south"
    elif 210 <= deg < 240:
        arrow = "southwest"
    elif 240 <= deg < 300:
        arrow = "west"
    elif 300 <= deg < 330:
        arrow = "northwest"
    else:
        arrow = ""
        
    return (arrow)



# decodes raw metar string to grab wind direction wind speed, gusts, temperature and baro
# This info is used as backup if the api does not provide this data in its normal response.
def decode_rawmessage(airport_name):
    decoded_wngust = "Not Present"
    decoded_alt = "n/a"
    decoded_tmp = "n/a"
    decoded_rvr = []
    decoded_cloudlayers = []
    decoded_weather = []
    cloud_types = ["SKC", "FEW", "SCT", "BKN", "OVC", "VV", "CLR"]
    weather_types = ["DZ","GR","GS","IC","PL","RA","SG","SN", \
                     "UP","BR","DU","FG","FU","HZ","PY","SA", \
                     "VA","DS","FC","PO","SQ","SS"]
    
    # use either live metar or test_metar from above.
    try:
        decode = airport_name.split()
#        print("***",decode) # debug
    except:
        print("*decode try failed") # debug
        decoded_airport,decoded_time,decoded_wndir,decoded_wnspd,decoded_wngust,decoded_vis,\
           decoded_alt,decoded_temp,decoded_dew,decoded_cloudlayers,decoded_weather,decoded_rvr \
           = "0","0","0","0","0","0","0","0","0","0","0","0"
        return decoded_airport,decoded_time,decoded_wndir,decoded_wnspd,decoded_wngust,decoded_vis,\
           decoded_alt,decoded_temp,decoded_dew,decoded_cloudlayers,decoded_weather,decoded_rvr

    # Get Airport ID 
    decoded_airport = decode[0]
    
    # Get Zulu time of Metar
    decoded_time = decode[1] 

    # Get Wind Direction, Wind Speed and Wind Gust    
    if decode[2] == "AUTO" or decode[2] == "COR": # check for AUTO or COR in 3rd postion
        decode[2], decode[3] = decode[3], decode[2] # switch AUTO and Windspeed to put wind speed into decode[2]
    decoded_wndir = decode[2][:3] # get winds direction
    decoded_wnspd = decode[2][3:5] # get wind speed
    if len(decode[2]) == 10:
        decoded_wngust = decode[2][6:8] # get wind gusts if present

    # Get Visibility    NEEDS WORK
    for i in range(len(decode)):
        if len(decode[i]) == 1: 
            decode[i] = decode[i]+" "+decode[i+1]
            
        if "SM" in decode[i] and i != 0:
            decoded_vis = decode[i]
            break
        else:
            decoded_vis = "n/a"

    # Grab altimeter/baro reading
    for i in range(len(decode)): 
        if len(decode[i]) == 5 and decode[i][0] == "A":
            decoded_z = decode[i][1:]
            decoded_alt = decoded_z[:2]+"."+decoded_z[2:]
            
    # Grab temperature and dewpoint reading
    for i in range(len(decode)): 
        if "/" in decode[i] and ("SM" not in decode[i] and "FT" not in decode[i]):
            decoded_z = decode[i][:3] # Temperature
            if decoded_z[0] == "M":
                decoded_temp = "-"+decoded_z[1:3]
            else:
                decoded_temp = decoded_z[:2]

            decoded_z = decode[i][-3:] # Dewpoint
            if decoded_z[0] == "M":
                decoded_dew = "-"+decoded_z[1:3]
            else:
                decoded_dew = decoded_z[-2:]  
            break
        
    # Get RVR if present
    for i in range(len(decode)):
        if "R" in decode[i] and "FT" in decode[i]:
            decoded_rvr = decode[i].split("/")
    
    # Get Weather Conditions  NEEDS WORK
    for i in range(len(decode)):
        if i > 2:
            if decode[i] == "RMK":
                break
            for j in weather_types:
                if j in decode[i]:
                    decoded_weather.append(decode[i])
            
    # Get Cloud Layers
    for i in range(len(decode)):
        for j in cloud_types:
            if j in decode[i]:
                decoded_cloudlayers.append(decode[i])
    
    return (decoded_airport,decoded_time,decoded_wndir,decoded_wnspd,decoded_wngust,decoded_vis,\
           decoded_alt,decoded_temp,decoded_dew,decoded_cloudlayers,decoded_weather,decoded_rvr)

