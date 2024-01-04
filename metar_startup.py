from metar_layouts import *
from metar_routines import *
import time

# epd7in5b_V2 = 3-color 7 by 5 display. Change this based on the display used.
# find 'epd = epd7in5b_V2.EPD()' towards bottom and change also if needed.
# These are located in the directory 'waveshare_epd'
from waveshare_epd import epd7in5b_V2

    
if __name__ == "__main__":
    epd = epd7in5b_V2.EPD() # Instantiate instance for display.
    epd.init()
    epd.Clear()
    display = Display() # pass to routines

    disp_ip(display, get_ip_address())
     
    # Print to e-Paper - This is setup to display on 7x5 3 color waveshare panel. epd7in5b_V2
    print("Updating screen...")
    try:
        epd.init()          
        time.sleep(1)
        print("Printing METAR Data to E-Paper")
        epd.display(epd.getbuffer(display.im_black), epd.getbuffer(display.im_red))
        print("Done")
        time.sleep(2)

    except Exception as e:
        print("Printing error", e)
        
    print("------------")
    print("Done")

