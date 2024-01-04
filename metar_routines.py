# metar_routines.py
# Metar Decoding Routines - Mark Harris
# Version 2.1
# UPDATED FAA API 12-2023, https://aviationweather.gov/data/api/

# Imports
from metar_remarks import *
from metar_settings import *
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
        
        
# Conversion routines   
def knots_to_kmh(knots):
    return (float(knots) * 1.852,' km/h')

def knots_to_ms(knots):
    return (float(knots) * 0.5144444444444444, ' m/s')

def knots_to_mph(knots):
    return (float(knots) * 1.151, ' mph')

def cel_to_fahren(celsius): # Celsius to Fahrenheit
    fahrenheit = (float(celsius) * 9 / 5) + 32
    return (fahrenheit, ' '+chr(176)+'F')

def miles_to_kil(miles): # Statute Miles to Kilometers
    return (miles * 1.609344, ' km')

def hpa_to_inHg(hpa): # hectoPascals to in/hg
    hpa = round(float(hpa) * 0.02953,2)
    return (str(hpa),' inHg')

def feet_to_meters(feet): # feet to meters
    feet =  round(feet * 0.3048,0)
    return (str(feet),' m')


# API Get Routines used to extract data from the METAR json string.
def get_metartype(metar): # "Type of encoding" string
    metartype = metar.data[0]["metarType"]
    print('metartype:',metartype)
    return(metartype)

def get_clouds(metar,cloud_layer_units):
    cctype_lst = []   # "Cloud layer - Cover coverage" string
    ccheight_lst = [] # "Cloud base in feet" integer
    dis_unit = ' ft'
    print("metar.data[0]['clouds']:",metar.data[0]['clouds']) # debug
    for i in range(len(metar.data[0]['clouds'])):
        if i == 3:
            break 
            
        cctype = metar.data[0]['clouds'][i]['cover']
        ccheight = metar.data[0]['clouds'][i]['base']
        
        if ccheight is None:
            ccheight = " "
            dis_unit = ' '
        else:
            if cloud_layer_units == 1:
                ccheight,dis_unit = feet_to_meters(ccheight)
            else:
                ccheight = '{0:.0f}'.format(ccheight)
            
        if cctype is None:
            cctype == " "
            dis_unit = ' '
            
        cctype_lst.append(cctype)
        ccheight_lst.append(ccheight)
            
    print('cctype_lst:',cctype_lst,', ccheight_lst:',ccheight_lst,'dis_unit:',dis_unit)
    return(cctype_lst,ccheight_lst,dis_unit)

def get_altim(metar,pressure_units): # "Altimeter setting in hectoPascals" number
    print('metar.data[0]["altim"]:', metar.data[0]["altim"]) # debug
    dis_unit = ' hPa'
    if metar.data[0]["altim"] != None:
        baro = '{0:.0f}'.format(metar.data[0]["altim"])
        if pressure_units == 1:
            baro,dis_unit = hpa_to_inHg(baro)
            baro = '{0:.2f}'.format(float(baro))
    else:
        baro = 'n/a'
    print('baro:',baro,'dis_unit:',dis_unit) # debug
    return(baro,dis_unit)

def get_temp(metar,temperature_units): # "Temperature in Celcius" number
    print('metar.data[0]["temp"]:',metar.data[0]["temp"]) # debug
    dis_unit = ' '+chr(176)+'C'
    if metar.data[0]["temp"] != None:
        tempf = '{0:.1f}'.format((metar.data[0]["temp"]))
    else:
        temp1 = float(decoded_temp)
        tempfloat = (temp1*1.8)+32
        tempf = '{0:.1f}'.format(tempfloat)
    if temperature_units == 1:
        tempf,dis_unit = cel_to_fahren(tempf)
    print('tempf:', tempf,'dis_unit:',dis_unit) # debug
    return(str(tempf),dis_unit)

def get_visib(metar,visibility_units): # "Visibility in statute miles, 10+ is greater than 10 sm" number
    print('metar.data[0]["visib"]:',metar.data[0]["visib"]) # debug
    dis_unit = ' miles'
    if metar.data[0]["visib"] != None:
        if type(metar.data[0]["visib"]) == int or type(metar.data[0]["visib"]) == float:
            tmp_vis = float(metar.data[0]["visib"])
        else:
#            print('metar.data[0]["visib"]',metar.data[0]["visib"]) # debug
            tmp_vis = metar.data[0]["visib"].strip('+')
#            print(tmp_vis) # debug
            tmp_vis = float(tmp_vis)
        vis = '{0:.1f}'.format(tmp_vis)
        if visibility_units == 1:
            vis,dis_unit = miles_to_kil(tmp_vis)
            vis = str(round(vis,1))
    else:
        vis = "n/a"
    print('vis:',vis,'dis_unit:',dis_unit) # debug
    return(vis,dis_unit)

def get_wxstring(metar): # "Encoded present weather string" string
    if metar.data[0]["wxString"] != None:
        descript = metar.data[0]["wxString"]
    else:
        descript = "n/a"
    print('descript:',descript) # debug
    return(descript)

def get_rawOb(metar): # "Raw text of observation" string
    if metar.data[0]['rawOb'] != None:
        rawmetar = metar.data[0]['rawOb']
    else:
        rawmetar = 'n/a'
#    print ('rawmetar:',rawmetar) # debug
    return(rawmetar)

def get_wdir(metar): # "Wind direction in degrees or VRB for variable winds" integer
    print('metar.data[0]["wdir"]:',metar.data[0]["wdir"]) # debug
    if metar.data[0]["wdir"] == 'VRB':
        winddir = 'VRB'        
    elif metar.data[0]["wdir"] != None:
        winddir = '{0:.0f}'.format(metar.data[0]["wdir"])
    else:
        winddir = 'n/a'
        
    if len(winddir) == 2:
        winddir = "0"+winddir
        
    if len(winddir) == 1:
        winddir = "00"+winddir
    winddir_raw = winddir
    
    if winddir == "VRB":
        pass
    else:
        winddir = winddir + chr(176) # chr(176) is the degree symbol
        
    if winddir == "000"+chr(176):
        winddir = "Calm"
        
    print('winddir:',winddir) # debug
    return(winddir,winddir_raw)

def get_wspd(metar,wind_speed_units): # "Wind speed in knots" integer
    print('metar.data[0]["wspd"]:',metar.data[0]["wspd"]) # debug
    dis_unit = ''
    if metar.data[0]["wspd"] != None:
        windsp = '{0:.1f}'.format(metar.data[0]["wspd"])
        dis_unit = ' kt'
        if wind_speed_units == 0:
            windsp,dis_unit = knots_to_kmh(windsp)
            windsp = str(round(float(windsp),1))
        elif wind_speed_units == 1:
            windsp,dis_unit = knots_to_ms(windsp)
            windsp = str(round(float(windsp),1))
        elif wind_speed_units == 3:
            windsp,dis_unit = knots_to_mph(windsp)
            windsp = str(round(float(windsp),1))
        else:
            pass # Knots, default from API
    else:
        windsp = "n/a"
        
    if windsp == "00" or windsp == "0.0":
        windsp = "Calm"

    print('windsp:',windsp,'dis_unit:',dis_unit) # debug
    return(windsp,dis_unit)

def get_wgst(metar,wind_speed_units): # "Wind gusts in knots" integer
    print('metar.data[0]["wgst"]:',metar.data[0]["wgst"]) # debug
    dis_unit = ''
    if metar.data[0]["wgst"] != None:
        gustsp = '{0:.1f}'.format(metar.data[0]["wgst"])
        dis_unit = ' kt'
        if wind_speed_units == 0:
            gustsp,dis_unit = knots_to_kmh(gustsp)
            gustsp = str(round(float(gustsp),1))
        elif wind_speed_units == 1:
            gustsp,dis_unit = knots_to_ms(gustsp)
            gustsp = str(round(float(gustsp),1))
        elif wind_speed_units == 3:
            gustsp,dis_unit = knots_to_mph(gustsp)
            gustsp = str(round(float(gustsp),1))
        else:
            pass # Knots, default from API

    else:
        gustsp = 'n/a'
        
    print('gustsp:',gustsp,'dis_unit:',dis_unit) # debug
    return(gustsp,dis_unit)

def get_misc(metar): # icaoid,obstime,elev,lat,lon,name = get_misc(metar)
    icaoid = metar.data[0]["icaoId"]   # "ICAO identifier" string
    obstime = metar.data[0]["obsTime"] # "The observation time (unix timestamp)" integer
    elev = metar.data[0]["elev"]       # "Elevation of site in meters" integer
    lat = metar.data[0]["lat"]         # "Latitude of site in degrees" number
    lon = metar.data[0]["lon"]         # "Longitude of site in degrees" number
    name = metar.data[0]["name"]       # "Full name of the site" string
    print(icaoid,obstime,elev,lat,lon,name) 
    return(icaoid,obstime,elev,lat,lon,name)


# Get RPi IP address to display on Boot up.
def get_ip_address():
    ip_address = '';
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8",80))
    ip_address = s.getsockname()[0]
    s.close()
    return ip_address




# Get Flight Categories for Class B and Class C airports
def get_flightcat():
    # api url
#    url = "https://www.aviationweather.gov/adds/dataserver_current/httpparam?dataSource=metars&requestType=retrieve&format=xml&mostRecentForEachStation=constraint&hoursBeforeNow=2.5&stationString="
    url = "https://aviationweather-cprk.ncep.noaa.gov/adds/dataserver_current/httpparam?dataSource=metars&requestType=retrieve&format=xml&mostRecentForEachStation=constraint&hoursBeforeNow=2.5&stationString="

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
#    print(root) # debug
    
    for data in root.iter('data'):
            num_results = data.attrib['num_results']
            print(num_results)
            
    for metar in root.iter('METAR'):
        stationId = metar.find('station_id').text
        if metar.find('flight_category') == None: ##! FAA API CHANGE
            flightcategory = "NA"
        else:
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
    # set defaults
    flightcategory = "VFR"
    icon = "sun"
    
    # Get Visibility
    try:
        vis_in_miles = float(metar.data[0]['visib'].strip("+"))
    except:
        vis_in_miles = 1 # Set an assumed default
        
    print("vis_in_miles: ",vis_in_miles) # debug
    print("num_clouds layers:",len(metar.data[0]['clouds'])) # debug
      
    # Get Cloud Cover
    for i in range(len(metar.data[0]['clouds'])): #["properties"]["cloudLayers"])):
        sky_condition = metar.data[0]['clouds'][i]['cover'] #["properties"]["cloudLayers"][i]["amount"]
        sky_ceiling = metar.data[0]['clouds'][i]['base'] #["properties"]["cloudLayers"][i]["amount"]
            
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
    
    print('flightcategory=',flightcategory,', icon=',icon) # debug
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
    if decode[2] == "VCTS":
        decoded_wndir = 0 # set default winds direction
        decoded_wnspd = 0 # set default wind speed
    else:        
        decoded_wndir = decode[2][:3] # get winds direction
        decoded_wnspd = decode[2][3:5] # get wind speed
    if len(decode[2]) == 10:
        decoded_wngust = decode[2][6:8] # get wind gusts if present

    # Get Visibility    NEEDS WORK
    for i in range(len(decode)):
#        print("i: ",i) # debug
        
        if len(decode[i]) == 1 and i < len(decode): 
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

