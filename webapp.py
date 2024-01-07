# webapp.py - Mark Harris
# for E-Paper display
# Version 2.1
# Part of Epaper Display project found at; https://github.com/markyharris/metar/
#
# UPDATED FAA API 12-2023, https://aviationweather.gov/data/api/
#
# This will provide a web interface to control the e-Paper display. 

from flask import Flask, render_template, request, flash, redirect, url_for, send_file, Response
import os
import sys
from metar_poweroff import *
from metar_settings import *

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

# variables
PATH = '/home/pi/metar/'
data_field4 = "0"
dis_select = [
    'Cycle Through All Layouts',
    'Display Random Layouts',
    'Large Flight Category and METAR',
    'METAR with Data Display',
    'Data Display with Icons',
    'Basic Large Flight Category',
    '3 Area Display with METAR',
    'Multiple Airport Flight Categories',
    'Airport Map and Flight Category',
    'Flight Category In Circles',
    'Worst Class B & C Airport Weather',
    'Metar and Large Wind Icons'
    ]

# Routes for flask
@app.route("/", methods=["GET", "POST"])
@app.route("/index", methods=["GET", "POST"])
@app.route("/metar", methods=["GET", "POST"])
def metar():
    # Grab default settings from 'metar_settings.py' used if web admin is not used.
    data_field1,data_field2,data_field3,data_field4, \
    data_field5,data_field6,data_field7,data_field8,data_field9,data_field10 \
    = airport,use_disp_format,interval,use_remarks, \
    wind_speed_units,cloud_layer_units,visibility_units,temperature_units,pressure_units,preferred_layouts
    
    # Now read 'data.txt' and populate these fields with the settings stored from web admin.
    data_field1, data_field2, data_field3, data_field4, \
    data_field5,data_field6,data_field7,data_field8,data_field9,data_field10 \
    = get_data()
    
    ndata1 = ""

    if request.method == "POST":
        display = request.form['display']
        data_field1 = request.form['data_field1'] # airport
        data_field2 = request.form['data_field2'] # use_disp_format
        data_field3 = request.form['data_field3'] # interval      
        data_field4 = request.form['data_field4'] # use_remarks        
        data_field5 = request.form['data_field5'] # wind_speed_units
        data_field6 = request.form['data_field6'] # cloud_layer_units
        data_field7 = request.form['data_field7'] # visibility_units
        data_field8 = request.form['data_field8'] # temperature_units
        data_field9 = request.form['data_field9'] # pressure_units
        data_field10 = request.form.getlist('data_field10') #
        
        if len(data_field10) == 0:
            print('nothing selected') # debug
            data_field10 = 'na'
        
        # format data_field10 to pass to command line
        for j in range(len(data_field10)):
            new = str(data_field10[j])
            ndata1 = ndata1 + new
        print(ndata1) # debug
        data_field10 = ndata1
        print('>>>>>>>>>>',data_field10,type(data_field10),'///') # debug
        
        if display == "powerdown":
            shutdown() 
            print("Powering Off RPi")
            os.system('sudo shutdown -h now')
 
        elif display == "reboot":
            os.system("ps -ef | grep 'metar_main.py' | awk '{print $2}' | xargs sudo kill")
            os.system('sudo reboot now')
            flash("Rebooting RPi - One Moment...")
            
        elif display == "off":
            os.system("ps -ef | grep 'metar_main.py' | awk '{print $2}' | xargs sudo kill")
            os.system('sudo python3 ' + PATH + 'metar_poweroff.py &')
            flash("Turning Off E-Paper Display - One Moment...")

        else:
            os.system("ps -ef | grep 'metar_main.py' | awk '{print $2}' | xargs sudo kill")
            os.system('sudo python3 ' + PATH + 'metar_main.py ' + ' ' + data_field1 + ' ' + data_field2 + ' ' + data_field3 + " " + data_field4 \
          + " " + data_field5 + ' ' + data_field6 + ' ' + data_field7 + " " + data_field8 + " " + data_field9 + " " + str(data_field10) +' &')        
 

            flash("Running E-Paper Metar Airport ID = " + data_field1.upper())
#            if data_field2 != "":
#                flash("Display Layout = " + dis_select[int(data_field2)+2])
                               
        print('Writing to Data:',data_field1,data_field2,data_field3,data_field4,data_field5,data_field6,data_field7,data_field8,data_field9,data_field10) # debug
        write_data(data_field1,data_field2,data_field3,data_field4,data_field5,data_field6,data_field7,data_field8,data_field9,data_field10)
        return render_template("metar.html",data_field1=data_field1,data_field2=data_field2,data_field3=data_field3,data_field4=data_field4, \
                               data_field5=data_field5,data_field6=data_field6,data_field7=data_field7,data_field8=data_field8,data_field9=data_field9,data_field10=data_field10)
    else:
        return render_template("metar.html", data_field1=data_field1,data_field2=data_field2,data_field3=data_field3,data_field4=data_field4, \
                               data_field5=data_field5,data_field6=data_field6,data_field7=data_field7,data_field8=data_field8,data_field9=data_field9,data_field10=data_field10)

 
# Functions
def write_data(data_field1,data_field2,data_field3,data_field4,data_field5,data_field6,data_field7,data_field8,data_field9,data_field10):
    f= open(PATH + "data.txt","w+")
    f.write(data_field1+"\n") # airport
    f.write(data_field2+"\n") # use_disp_format
    f.write(data_field3+"\n") # interval 
    f.write(data_field4+"\n") # use_remarks
    f.write(data_field5+"\n") # wind_speed_units
    f.write(data_field6+"\n") # cloud_layer_units
    f.write(data_field7+"\n") # visibility_units
    f.write(data_field8+"\n") # temperature_units
    f.write(data_field9+"\n") # pressure_units
    f.write(data_field10+"\n") # preferred_layouts (list)
    f.close()
    return (True)
    
def get_data():
    f=open(PATH + "data.txt", "r")
    Lines = f.readlines() 
    data_field1 = Lines[0].strip() # airport
    data_field2 = Lines[1].strip() # use_disp_format
    data_field3 = Lines[2].strip() # interval 
    data_field4 = Lines[3].strip() # use_remarks
    data_field5 = Lines[4].strip() # wind_speed_units
    data_field6 = Lines[5].strip() # cloud_layer_units
    data_field7 = Lines[6].strip() # visibility_units
    data_field8 = Lines[7].strip() # temperature_units
    data_field9 = Lines[8].strip() # pressure_units
    data_field10 = Lines[9].strip() #preferred_layouts (list)
    f.close()
    return (data_field1,data_field2,data_field3,data_field4,data_field5,data_field6,data_field7,data_field8,data_field9,data_field10)


# Start of Flask
if __name__ == '__main__':
#    error = 1/0 # Force webapp to stop executing for debug purposes

    # airport,use_disp_format,interval,use_remarks,wind_speed_units,cloud_layer_units,visibility_units,temperature_units,pressure_units
    # Example: kabe,1,60,1,2,0,0,1,1
    data_field1,data_field2,data_field3,data_field4, \
    data_field5,data_field6,data_field7,data_field8,data_field9,data_field10 = get_data()  
    
    # create cmdline command to start the main program using the 'data.txt' variables to kick things off.     
    print('sudo python3 ' + PATH + 'metar_main.py ' + ' ' + data_field1 + ' ' + data_field2 + ' ' + data_field3 + ' ' + data_field4 \
          + ' ' + data_field5 + ' ' + data_field6 + ' ' + data_field7 + " " + data_field8 + ' ' + data_field9 +  ' ' + data_field10 + ' &\n')  # debug
    
    # first run at startup. display web admin ip url for 60 seconds
    os.system('sudo python3 ' + PATH + 'metar_main.py ' + ' ' + data_field1 + ' ' + data_field2 + ' ' + data_field3 + ' ' + data_field4 \
          + ' ' + data_field5 + ' ' + data_field6 + ' ' + data_field7 + ' ' + data_field8 + ' ' + data_field9 + ' ' + data_field10 + ' &')
    
    app.run(debug=True, use_reloader=False, host='0.0.0.0') # use use_reloader=False to stop double loading
              