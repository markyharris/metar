# E-Paper METAR Display
This software will display various layouts of METAR data on a 7 by 5 inch 3-color E-Paper. Specifically the 7.5inch e-Paper HAT (B) by Waveshare. See https://www.waveshare.com/7.5inch-e-paper-hat-b.htm for more information and pricing from Waveshare.

This software is very specific to the size and 3-color nature of this display. However, the layouts are in a separate module and can be modified to fit other sizes of display if the desire was there.

<b><H2>Installation Steps</H2></b>

<b>DOWNLOAD NEEDED APPS:</b></br>
Download Balena Etcher - https://www.balena.io/etcher/</br>
Download Berrylan Unix Bullseye Image - https://berrylan.org/</br>
Download Berrylan App from either Apple App Store or Android Play Store to your phone</br>
<i>NOTE: The Berrylan image is not strictly required. It provides an easy way to setup the WiFi and enable SSH on a headless RPi system such as this. There are other ways to do this such as temporarily connecting a keyboard and monitor to the RPi to start. However, if you choose to give this to a friend then having the ability to change the WiFi network through the Berrylan phone app can be very handy. If Berrylan is not desired, visit; https://www.raspberrypi.com/software/operating-systems/ to download the latest image.</i></br>

<b>WRITE IMAGE TO SD CARD:</b></br>
Using Balena Etcher, write Image to Micro SD Card</br>
Put SD card into RPi and boot-up completely</br>

<b>SETUP WIFI USING BERRYLAN:</b></br>
Open Berrylan app on phone and select for 'BT WLAN setup' or 'BT WLAN' or 'raspberrypi' depending on what is displayed. The most common is 'BT WLAN'. If you see more than one, then pick the first one and go through the steps. If it ends up not being this particular RPi, then run it again and select the next one. You may have to give the app alittle time to find it however, so don't be too impatient.</br>
  Select WiFi SSID to use</br>
  Enter the WiFi password</br>
  Write down the IP address that is displayed. You'll need this later. You can tap it and copy it to clipboard</br>

<b>LOGIN USING SSH CLIENT:</b></br>
Open a SSH Client and enter the 'pi@IP address' to start the login process, i.e. 'pi@192.163.86.71'</br>
Login using username 'pi' and password 'raspberry'. If a normal image was used, then SSH must be enabled before these clients will work. Berrylan automatically enables SSH. Otherwise use raspi-config to do so.</br>
<i>Note: There are a number of SSH Clients. A few of the more popular are;
<ul>
  <li>KiTTY.</br>
  <li>PuTTY and other PuTTY versions</br>
  <li>MobaXterm</br>
  <li>WinSCP</br>
  <li>SmarTTY</br>
  <li>Bitvise SSH Client</br>
  <li>Terminal (for Mac)</br>
  <li>Chrome SSH extension</br>
</ul> </i>

<b>SETUP SPI INTERFACE:</b></br>
At the cmd line prompt; 'pi@raspberrypi:~ $' enter the following;</br>
  sudo raspi-config</br>
  3 - Interface Options</br>
  I4 SPI Enable this? Yes </br>
<i>Note: You can change the hostname and password if desired at this point, but its optional</i></br>
Answer 'Yes' when you exit raspi-config to Reboot the RPi </br>

<b>SETUP GITHUB ON RPI:</b></br>
After RPi boots up and you login through your SSH client, enter;</br>
  sudo apt update</br>
  sudo apt-get install git</br>
  git --version </br>
If you receive a git version number than you are good to go.</br>

<b>COPY FILES FROM GITHUB:</b></br>
Enter;</br>
  sudo git clone https://github.com/markyharris/metar.git</br>
  cd metar</br>
  ls -la </br>
This should list the files copied from github to verify it worked properly</br>

<b>DEPENDENCIES:</b></br>
Install necessary dependencies needed for the software;</br>
  sudo apt-get install python3-setuptools</br>
  sudo apt install python3-pil</br>
  sudo apt-get install python3-numpy</br>
  sudo pip3 install Flask</br>
    
<b>FONTS:</b></br>
The code is written with 'NotoMono-Regular.ttf' and 'LiberationMono-Bold.ttf' in used, so at minimum these need to be installed. If not enter;</br>
  cd /usr/share/fonts/truetype/</br>
  sudo mkdir noto</br>
  sudo mkdir liberation2</br>
  cd noto</br>
  sudo wget https://github.com/markyharris/metar/raw/f1858d85ad3b79864fb6e082cd083346828661ef/fonts/noto/NotoMono-Regular.ttf</br>
  cd ..</br>
  cd liberation2</br>
  sudo wget https://github.com/markyharris/metar/raw/f1858d85ad3b79864fb6e082cd083346828661ef/fonts/liberation2/LiberationMono-Bold.ttf</br>

<b>TEST RUN METAR DISPLAY:</b></br>
Enter;</br>
  cd ~</br>
  cd metar</br>
  sudo python3 metar_main.py</br>
If all is well the cmd line will display debug data including a raw metar string. Watch your e-paper display to see if it starts to blink as it updates. The full refresh can take a number of seconds so be patient. After a bit a layout should be displayed showing the default airport from metar_settings.py</br>
If so, you are good to go!</br>

Now edit the metar_settings.py file as you wish. These values are defaults that the script falls back on.</br>
  Default User Settings</br>
  airport = "KFLG" # enter default airport identifier to display. Be sure to use quotes</br>
  interval = 1800  # enter default time in seconds between METAR updates - 3600 = 1 hour, no quotes</br>
  use_disp_format = 7 # Choose which display layout to use. -1 = Random layout, -2 = Cycle layouts</br>
  use_remarks = 1  # 0 = display airport information, 1 = display metar remarks info </br>
  random_airports = ["KEYW","KDFW","KSEA","KORD", "KLAS","KCMR","KABQ","KDEN", \</br>
                   "KPHX","KNBC","KBKV","KTTS"]</br>
				   
<b>TEST CMD LINE CONTROL:</b></br>
The script was written to except up to 4 cmd line arguments;</br>
  1st argument - airport identifier - must be 4 character ICAO format</br>
  2nd argument - layout number - will accept -2, -1, and 0-7</br>
  3rd argument - update interval in seconds - 60 = 1 minute, 3600 = 1 hour</br>
  4th argument - use remarks - 1 = display metar remarks key info, 0 = display airport information</br>
They must be in the order shown, but not all of them are required. For instance only the Airport ID can be used, and the others will be filled in using the default settings in metar_settings.py</br>
For example enter;</br>
  sudo python3 metar_main.py kflg 7 60 0</br>
The display will show the Flagstaff Airport using Layout 7 for 60 seconds before updating using airport info.</br>
Assuming this is works properly, then using the webapp.py and metar.html scripts below should work just fine.</br>

<b>TEST WEBAPP.PY:</b></br>
From the metar directory enter;</br>
  sudo python3 webapp.py</br>
This will run a Flask module that will start metar_main.py in last save configuration. Flask sets up a web server so we can also run an html file to control the display from any computer, tablet or phone that is on the same wifi network.</br>
If all is good your display should be showing a layout of information.</br>
Make note that when webapp.py starts, information will be displayed in your SSH client. You will need the URL that it provides. For instance; '* Running on http://192.168.86.71:5000/ (Press CTRL+C to quit)'</br>

<b>TEST METAR.HTML:</b></br>
Using the URL from the previous step, open a web browser and enter it in the URL. If all is well you will see a web page that allows for easy configuration and change to the display.</br>

<b>SETUP RC.LOCAL FOR STARTUP:</b></br>
This is optional, but if you would like the display to restart automatically after a shutdown, or accidental power outage then this is a good way to go. Also, the webapp.py must be running for the web interface to work properly. </br>
Enter;</br>
  cd ~</br>
  cd /etc</br>
  sudo nano rc.local</br>
Before the 'Exit' statement add;</br>
  sudo python3 /home/pi/metar/webapp.py &</br>
Then to save and reboot;</br>
  ctrl-x</br>
  y</br>
  sudo reboot now</br>
<i>Note: There may be times when you don't want webapp.py to startup automatically, so simply open up rc.local again and comment out the line that was added then resave and reboot.</i></br>

<b>SETUP POWEROFF.SERVICE FOR SHUTDOWN:</b></br>
This is optional as well, but its nice to blank the epaper display when the unit is shutdown. A power outage won't blank the screen, but once the power comes back on it will reset the display if you setup rc.local above.</br>

Power Off Service installation:</br>
Copy 'poweroff.service' into /lib/systemd/system; </br>
  cd ~</br>
  cd /lib/systemd/system </br>
  sudo wget https://raw.githubusercontent.com/markyharris/metar/main/poweroff.service</br>

Enable the service by entering;</br>
  sudo systemctl enable poweroff.service</br>

Copy the python script 'metar_poweroff.py' into /opt/metar_poweroff;</br>
  cd ~  </br>
  cd /opt</br>
  sudo mkdir metar_poweroff</br>
  cd metar_poweroff</br>
  sudo wget https://raw.githubusercontent.com/markyharris/metar/main/metar_poweroff.py</br>
  
  
