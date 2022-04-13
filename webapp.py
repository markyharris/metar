# webapp.py - Mark Harris
# for E-Paper display
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
rem_data = "0"

# Routes for flask
@app.route("/", methods=["GET", "POST"])
@app.route("/index", methods=["GET", "POST"])
@app.route("/metar", methods=["GET", "POST"])
def metar():
    data_field1, data_field2, data_field3, rem_data = airport, use_disp_format, interval, use_remarks
    data_field1, data_field2, data_field3, rem_data = get_data()

    if request.method == "POST":
        display = request.form['display']
        data_field1 = request.form['data_field1']
        data_field2 = request.form['data_field2']
        data_field3 = request.form['data_field3']        
        rem_data = request.form['rem_data']
        
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
            os.system('sudo python3 ' + PATH + 'metar_main.py '+ data_field1+' '+data_field2+' '+data_field3+' '+rem_data+' &')
            flash("Running E-Paper Metar Airport ID = " + data_field1)
            if data_field2 != "":
                flash("Display Layout = " + data_field2)
                               
        print(data_field1) # debug
        write_data(data_field1, data_field2, data_field3, rem_data)
        return render_template("metar.html", data_field1=data_field1, data_field2=data_field2, data_field3=data_field3, rem_data=rem_data)
    else:
        return render_template("metar.html", data_field1=data_field1, data_field2=data_field2, data_field3=data_field3, rem_data=rem_data)

 
# Functions
def write_data(data_field1, data_field2, data_field3, rem_data):
    f= open(PATH + "data.txt","w+")
    f.write(data_field1+"\n")
    f.write(data_field2+"\n")
    f.write(data_field3+"\n")
    f.write(rem_data+"\n")
    f.close()
    return (True)
    
def get_data():
    f=open(PATH + "data.txt", "r")
    Lines = f.readlines() 
    data_field1 = Lines[0].strip()
    data_field2 = Lines[1].strip()
    data_field3 = Lines[2].strip()
    rem_data = Lines[3].strip()
    f.close()
    return (data_field1, data_field2, data_field3, rem_data)


# Start of Flask
if __name__ == '__main__':
#    error = 1/0 # Force webapp to stop executing for debug purposes
    data_field1, data_field2, data_field3, rem_data = "KFLG","-3","60","0" #get_data()  # read what is in data.txt to get last run
    
    os.system('sudo python3 ' + PATH + 'metar_main.py ' + data_field1 + ' ' + data_field2 + ' ' + data_field3 + " " + rem_data + ' &')        
    app.run(debug=True, use_reloader=False, host='0.0.0.0') # use use_reloader=False to stop double loading
             