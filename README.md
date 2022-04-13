# E-Paper METAR Display
This project is explained and amplified on Instructables.com. See; https://www.instructables.com/7x5-E-Paper-METAR-Display/<p>

If you would like to update to the latest version of this software enter;
<pre><code>
cd metar
sudo git reset --hard
sudo git pull
</code></pre>
	
This software will display various layouts of METAR data on a 7 by 5 inch 3-color E-Paper. Specifically the 7.5inch e-Paper HAT (B) by Waveshare. See https://www.waveshare.com/7.5inch-e-paper-hat-b.htm for more information and pricing from Waveshare.

<p align="center"><img src=https://github.com/markyharris/metar/raw/main/static/metar_collage.jpg width="400"></p>

This software is written specifically to the size and 3-color nature of this display. However, the layouts are in a separate module and can be modified to fit other sizes of display if the desire is there. Theoretically a 2 color 7x5 could be used as well. See script 'metar_main.py' for comments on this.

For specific info on using e-paper display with RPi, see;<br>
  https://www.waveshare.com/wiki/Template:Raspberry_Pi_Guides_for_SPI_e-Paper<br>
For information on the specific display used for this project see;<br>
  https://www.waveshare.com/wiki/7.5inch_e-Paper_HAT_(B)<br><br>

<b><H2>Installation Steps</H2></b>

<b>DOWNLOAD NEEDED APPS:</b></br>
Download Balena Etcher - https://www.balena.io/etcher/</br>
Download Berrylan Unix Bullseye Image - https://berrylan.org/</br>
Download Berrylan App from either Apple App Store or Android Play Store to your phone<br><br>
<i>NOTE: The Berrylan image is not strictly required. It provides an easy way to setup the WiFi and enable SSH on a headless RPi system such as this. There are other ways to do this such as temporarily connecting a keyboard and monitor to the RPi to start. However, if you choose to give this to a friend then having the ability to change the WiFi network through the Berrylan phone app can be very handy. If Berrylan is not desired, visit; https://www.raspberrypi.com/software/operating-systems/ to download the latest image.<p> 
https://desertbot.io/blog/headless-raspberry-pi-4-ssh-wifi-setup provides steps to follow to setup WiFi on a headless system if Berrylan is not used.</i><br>

<b>WRITE IMAGE TO SD CARD:</b></br>
Using Balena Etcher, write Image to Micro SD Card.<br>
Put SD card into RPi and boot-up completely. This will take a minute or two. Watch the access LED on RPi for feedback.<br>

<b>SETUP WIFI USING BERRYLAN:</b><br>
Open Berrylan app on phone and select for 'BT WLAN setup' or 'BT WLAN' or 'raspberrypi' depending on what is displayed. The most common is <b>'BT WLAN'</b>. If you see more than one, then pick the first one and go through the steps. If it ends up not being this particular RPi, then run it again and select the next one. You may have to give the app alittle time to find it however, so don't be too impatient.</br>
  <ul>
  <li>Select WiFi SSID to use</br>
  <li>Enter the WiFi password</br>
  <li>Write down the IP address that is displayed. You'll need this later. You can tap it and copy it to clipboard</br>
  </ul>
  
<b>LOGIN USING SSH CLIENT:</b></br>
Open a SSH Client and enter the 'pi@IP address' to start the login process, i.e. 'pi@192.163.86.71'<br>
Login using username 'pi' and password 'raspberry'. If a normal image was used, then SSH must be enabled before these clients will work. Berrylan automatically enables SSH. Otherwise use 'raspi-config' to do so. See https://www.raspberrypi.com/documentation/computers/configuration.html for info on using 'raspi-config'<p>
<i>Note: There are a number of SSH Clients. A few of the more popular are;
<ul>
  <li>KiTTY.
  <li>PuTTY and other PuTTY versions
  <li>MobaXterm
  <li>WinSCP
  <li>SmarTTY
  <li>Bitvise SSH Client
  <li>Terminal (for Mac)
  <li>Chrome SSH extension
</ul> </i>

<b>SETUP SPI INTERFACE:</b><br>
At the cmd line prompt; 'pi@raspberrypi:~ $' enter the following;
  <pre><code>
  sudo raspi-config
  3 - Interface Options
  I4 SPI Enable this? Yes </code></pre><br>
<i>Note: You can change the hostname and password if desired at this point, but its optional</i></br>
Answer 'Yes' when you exit raspi-config to Reboot the RPi </br>

<b>SETUP GITHUB ON RPI:</b></br>
After RPi boots up and you login through your SSH client, enter;</br>
  <pre><code>
  sudo apt update
  sudo apt-get install git
  git --version </pre></code>
If you receive a git version number than you are good to go.</br>

<b>COPY FILES FROM GITHUB:</b><br>
Enter;
  <pre><code>
  sudo git clone https://github.com/markyharris/metar.git
  cd metar
  ls -la </pre></code>
This should list the files copied from github to verify it worked properly</br>

<b>DEPENDENCIES:</b></br>
Install necessary dependencies needed for the software;</br>
<pre><code>
  sudo apt-get install python3-setuptools
  sudo apt install python3-pil
  sudo apt-get install python3-numpy
  sudo pip3 install Flask</pre></code>
    
<b>FONTS:</b></br>
The code is written with 'NotoMono-Regular.ttf' and 'LiberationMono-Bold.ttf' used, so at minimum these need to be installed. So enter;</br>
  <pre><code>
  cd /usr/share/fonts/truetype/
  sudo mkdir noto
  sudo mkdir liberation2
  cd noto
  sudo wget https://github.com/markyharris/metar/raw/f1858d85ad3b79864fb6e082cd083346828661ef/fonts/noto/NotoMono-Regular.ttf
  cd ..
  cd liberation2
  sudo wget https://github.com/markyharris/metar/raw/f1858d85ad3b79864fb6e082cd083346828661ef/fonts/liberation2/LiberationMono-Bold.ttf</pre></code>

<b>TEST RUN METAR DISPLAY:</b></br>
Enter;
<pre><code>
  cd ~
  cd metar
  sudo python3 metar_main.py</pre></code>
If all is well the cmd line will display debug data including a raw metar string. Watch your e-paper display to see if it starts to blink as it updates. The full refresh can take a number of seconds so be patient. After a bit a layout should be displayed showing the default airport from metar_settings.py</br>
If so, you are good to go!</br>

Now edit the 'metar_settings.py' file as you wish. These values are defaults that the script falls back on.</br>
  <pre><code>
  # Default User Settings
  airport = "KFLG" # enter default airport identifier to display. Be sure to use quotes
  interval = 1800  # enter default time in seconds between METAR updates - 3600 = 1 hour, no quotes
  use_disp_format = 7 # Choose which display layout to use. -1 = Random layout, -2 = Cycle layouts
  use_remarks = 1  # 0 = display airport information, 1 = display metar remarks info 
  random_airports = ["KEYW","KDFW","KSEA","KORD", "KLAS","KCMR","KABQ","KDEN", \
                   "KPHX","KNBC","KBKV","KTTS"]</pre></code>
				   
<b>TEST CMD LINE CONTROL:</b></br>
The script was written to except up to 4 cmd line arguments;</br>
<blockquote>
  1st argument - airport identifier - must be 4 character ICAO format</br>
  2nd argument - layout number - will accept -2, -1, and 0-7</br>
  3rd argument - update interval in seconds - 60 = 1 minute, 3600 = 1 hour</br>
  4th argument - use remarks - 1 = display metar remarks key info, 0 = display airport information</blockquote>
They must be in the order shown, but not all of them are required. For instance you can enter only the Airport ID and the default settings will be used for the last 3 args<br>
<p align="center"><img src=https://github.com/markyharris/metar/raw/main/static/metar_cmdline.jpg width="400"></p>
For example enter;
<pre><code>
  sudo python3 metar_main.py kflg 7 60 0</pre></code>
The display will show the Flagstaff Airport using Layout 7 for 60 seconds before updating using airport info.<br>
Assuming this is works properly, then using the 'webapp.py' and metar.html scripts below will work just fine.<br>
<br>
<b>TEST WEBAPP.PY:</b><br>
From the metar directory enter;<br>
<pre><code>
  sudo python3 webapp.py</pre></code>
This will run a Flask module that will run 'metar_main.py'. Flask sets up a web server so we can also run an html file to control the display from any computer, tablet or phone that is on the same WiFi network.<br>
<br>
When first run, your E-Paper display will show a screen providing the proper URL to use to access the admin web page. This screen will stay for on 60 seconds then will start to cycle through each display layout from there. Each time the RPi is restarted, the admin URL will be displayed. This will help if the in the future a new IP is assigned to your RPi. <br>
<br>
Make note that when webapp.py starts, admin web page information will also be displayed in your SSH client. You will need the URL that it provides. For instance; '* Running on http://192.168.86.71:5000/ (Press CTRL+C to quit)'. This is an example, yours will be different.</b><br>
<br>
<b>TEST METAR.HTML:</b><br>
Using the URL from the previous step, open a web browser and enter it in the URL. If all is well you will see a web page that allows for easy control of the E-Paper display.<br>
<p align="center"><img src=https://github.com/markyharris/metar/raw/main/static/metar_html.jpg width="400"></p>
<i>Note: The html file must be run from a computer, tablet or phone that is connected to the same WiFi network using the URL provided when WiFi was originally setup. The URL must have ':5000' appended to the IP Address, ie. http://192.168.86.71:5000/ (Your IP will be different, this is just an example).</i><br>
<br>
<b>SETUP RC.LOCAL FOR STARTUP:</b><br>
This is optional, but if you would like the display to restart automatically after a shutdown, or accidental power outage then this is a good way to go. Also, the webapp.py must be running for the web interface to work properly. <br>
<br>
Enter;<br>
<pre><code>
  cd ~
  cd /etc
  sudo nano rc.local</pre></code>
  <p align="center"><img src=https://github.com/markyharris/metar/raw/main/static/metar_rclocal.jpg width="400"></p>
Before the 'Exit' statement add;<br>
<pre><code>
  sudo python3 /home/pi/metar/webapp.py &</pre></code>
Then to save and reboot;<br>
<pre><code>
  ctrl-x
  y
  sudo reboot now</pre></code><br>
<i>Note: There may be times when you don't want 'webapp.py' to startup automatically, so simply open up rc.local again and comment out the line that was added then resave and reboot.</i><br>
<br>
<b>SETUP POWEROFF.SERVICE FOR SHUTDOWN:</b><br>
This is optional as well, but its nice to blank the epaper display when the unit is shutdown. A power outage won't blank the screen, but once the power comes back on it will reset the display if you setup rc.local above.<br>
<br>
Copy 'poweroff.service' into /lib/systemd/system; <br>
<pre><code>
  cd ~
  cd /lib/systemd/system 
  sudo wget https://raw.githubusercontent.com/markyharris/metar/main/poweroff.service</pre></code>

Enable the service by entering;<br>
<pre><code>
  sudo systemctl enable poweroff.service</pre></code>

Copy the python script 'metar_poweroff.py' into /opt/metar_poweroff;<br>
<pre><code>
  cd ~  
  cd /opt
  sudo mkdir metar_poweroff
  cd metar_poweroff
  sudo wget https://raw.githubusercontent.com/markyharris/metar/main/metar_poweroff.py</pre></code>
<br>
<b>MISC:</b><br>
At this point the installation is complete, however it is suggested that the image on the SD Card is backed up to your computer in case something goes wrong, rather than going through this installation process again.<br> 
To do so;
<ul>
  <li>Download Win32DiskImager from; https://sourceforge.net/projects/win32diskimager/
  <li>Insert SD Card into your computer's card reader.
  <li>Click the folder icon and locate a directory to store the image and provide a name, ie. metar_display.img<br>
  <li>Click 'Read Only Allocated Partitions'
  <li>Click 'Read' and let it do its thing.
  <li>Once complete eject SD Card and re-install in the RPi
</ul>
Mount the display and RPi in the frame of your choice and enjoy. - Mark
