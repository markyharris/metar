# metar_display.py
# Metar Display - Mark Harris
# Altered from https://github.com/aerodynamics-py/WEATHER_STATION_PI
#
# Added a number of bold fonts
# Added a number of drawing routines for rounded corners, etc.

# Imports
from PIL import Image, ImageDraw, ImageFont, ImageOps
import requests
import urllib.request

# Setup fonts that could be chosen. Default font_choice is #5
# Look in '/usr/share/fonts/truetype/' to see what is installed on 
# specific system and change as necessary. 
font_choice = 5
if font_choice == 1:
    project_font = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
elif font_choice == 2:
    project_font = "/usr/share/fonts/truetype/droid/DroidSansFallbackFull.ttf"
elif font_choice == 3:
    project_font = "/usr/share/fonts/truetype/freefont/FreeMonoBoldOblique.ttf" 
elif font_choice == 4:
    project_font = "/usr/share/fonts/truetype/liberation2/LiberationMono-Bold.ttf" 
elif font_choice == 5:
    project_font = "/usr/share/fonts/truetype/noto/NotoMono-Regular.ttf" 
elif font_choice == 6:
    project_font = "/usr/share/fonts/truetype/piboto/Piboto-Bold.ttf" 
elif font_choice == 7:
    project_font = "/usr/share/fonts/truetype/quicksand/Quicksand-Bold.ttf" 
else:
    project_font = "font/Open_Sans/OpenSans-SemiBold.ttf"
    
font8 = ImageFont.truetype(project_font, 8)
font12 = ImageFont.truetype(project_font, 12)
font14 = ImageFont.truetype(project_font, 14)
font16 = ImageFont.truetype(project_font, 16)
font20 = ImageFont.truetype(project_font, 20)
font24 = ImageFont.truetype(project_font, 24)
font36 = ImageFont.truetype(project_font, 36)
font48 = ImageFont.truetype(project_font, 48)
font96 = ImageFont.truetype(project_font, 96)
font196 = ImageFont.truetype(project_font, 196)
font296 = ImageFont.truetype(project_font, 296)

project_fontbold = "/usr/share/fonts/truetype/liberation2/LiberationMono-Bold.ttf" 
font8b = ImageFont.truetype(project_fontbold, 8)
font12b = ImageFont.truetype(project_fontbold, 12)
font14b = ImageFont.truetype(project_fontbold, 14)
font16b = ImageFont.truetype(project_fontbold, 16)
font20b = ImageFont.truetype(project_fontbold, 20)
font24b = ImageFont.truetype(project_fontbold, 24)
font36b = ImageFont.truetype(project_fontbold, 36)
font48b = ImageFont.truetype(project_fontbold, 48)
font96b = ImageFont.truetype(project_fontbold, 96)
font196b = ImageFont.truetype(project_fontbold, 196)
font296b = ImageFont.truetype(project_fontbold, 296)


class Metar:
    def __init__(self, airport):
        self.data = requests.get(
            f"https://api.weather.gov/stations/"+airport+"/observations/latest", timeout=5).json()
        self.data2 = requests.get(
            f"https://api.weather.gov/stations/"+airport, timeout=5).json()
        requests.session().close()
        pass

    def update(self, airport):
        self.data = requests.get(
            f"https://api.weather.gov/stations/"+airport+"/observations/latest", timeout=5).json()
        self.data2 = requests.get(
            f"https://api.weather.gov/stations/"+airport, timeout=5).json()
        requests.session().close()
        return self.data, self.data2


class Display:
    def __init__(self):
        self.im_black = Image.new('1', (800, 480), 255)
        self.im_red = Image.new('1', (800, 480), 255)
        self.draw_black = ImageDraw.Draw(self.im_black)
        self.draw_red = ImageDraw.Draw(self.im_red)


    def draw_text_centered(self, ypos, text, font):
        w, h = self.draw_black.textsize(text)
        #print(w,h) # debug
        self.draw_black.text(((800-w-100)/2, ypos), text, fill=0, font=font) 


    def draw_circle(self, x, y, r, c):
        if c == "b":
            self.draw_black.ellipse((x - r, y - r, x + r, y + r), fill=0)
        elif c == "wb":
            self.draw_black.ellipse((x - r, y - r, x + r, y + r), fill=255)
        elif c == "wr":
            self.draw_red.ellipse((x - r, y - r, x + r, y + r), fill=255)
        else:
            self.draw_red.ellipse((x - r, y - r, x + r, y + r), fill=0)
 
 
    def draw_circle_outline(self, x, y, r, w, c):
        r2 = r - w
#        print(r,r2) # debug
        if c == "b":            
            self.draw_black.ellipse((x - r, y - r, x + r, y + r), fill=0)
            self.draw_black.ellipse((x - r2, y - r2, x + r2, y + r2), fill=255)
        else:            
            self.draw_red.ellipse((x - r, y - r, x + r, y + r), fill=0)
            self.draw_red.ellipse((x - r2, y - r2, x + r2, y + r2), fill=255)

    
    def draw_icon(self, x, y, c, l, h, icon):
        im_icon = Image.open("/home/pi/metar/icons/" + icon + ".png")
        im_icon = im_icon.convert("RGBA") #"LA"
        im_icon = im_icon.resize((l, h))

        if c == "b":
            self.im_black.paste(im_icon, (x, y), im_icon)
        elif c=="wb": # Invert black image if necessary
            if im_icon.mode == 'RGBA':
                r,g,b,a = im_icon.split()
                rgb_image = Image.merge('RGB', (r,g,b))
                inverted_image = ImageOps.invert(rgb_image)
                r2,g2,b2 = inverted_image.split()
                final_transparent_image = Image.merge('RGBA', (r2,g2,b2,a))
            else:
                inverted_image = ImageOps.invert(im_icon)
            self.im_black.paste(inverted_image, (x, y), im_icon)            
        elif c=="wr":# Invert red image if necessary
            if im_icon.mode == 'RGBA':
                r,g,b,a = im_icon.split()
                rgb_image = Image.merge('RGB', (r,g,b))
                inverted_image = ImageOps.invert(rgb_image)
                r2,g2,b2 = inverted_image.split()
                final_transparent_image = Image.merge('RGBA', (r2,g2,b2,a))
            else:
                inverted_image = ImageOps.invert(im_icon)
            self.im_red.paste(inverted_image, (x, y), im_icon)
        else:
            self.im_red.paste(im_icon, (x, y), im_icon)


    def round_box(self, up_left_x, up_left_y, box_width, box_height, radius, box_color="b", box_fill=0, line_width=5):      
        up_right_x = up_left_x + box_width 
        up_right_y = up_left_y 
        low_left_x = up_left_x 
        low_left_y = up_left_y + box_height 
        low_right_x = up_right_x 
        low_right_y = low_left_y 
        
        if box_color == "b":
            # longest/shortest box 
            self.draw_black.rectangle((up_left_x-radius, up_left_y, low_right_x+radius, low_right_y), fill=box_fill, outline=0, width=line_width)
            # skinniest/tallest box 
            self.draw_black.rectangle((up_left_x, up_left_y-radius, low_right_x, low_right_y+radius), fill=box_fill, outline=0, width=line_width)
            if line_width == 0:
                cir_color = "wb"
            else:
                cir_color = "b"
            # Upper Left corner circle
            self.draw_circle(up_left_x, up_left_y, radius, cir_color)  
            # Upper Right corner circle
            self.draw_circle(up_right_x, up_right_y, radius, cir_color)  
            # Lower Left corner circle
            self.draw_circle(low_left_x, low_left_y, radius, cir_color)      
            # Lower Right corner circle
            self.draw_circle(low_right_x, low_right_y, radius, cir_color)   
        else:
            # longest/shortest box 
            self.draw_red.rectangle((up_left_x-radius, up_left_y, low_right_x+radius, low_right_y), fill=box_fill, outline=0, width=line_width)
            # skinniest/tallest box 
            self.draw_red.rectangle((up_left_x, up_left_y-radius, low_right_x, low_right_y+radius), fill=box_fill, outline=0, width=line_width)
            if line_width == 0:
                cir_color = "wr"
            else:
                cir_color = "r"
            # Upper Left corner circle
            self.draw_circle(up_left_x, up_left_y, radius, cir_color)    
            # Upper Right corner circle
            self.draw_circle(up_right_x, up_right_y, radius, cir_color)      
            # Lower Left corner circle
            self.draw_circle(low_left_x, low_left_y, radius, cir_color)      
            # Lower Right corner circle
            self.draw_circle(low_right_x, low_right_y, radius, cir_color)     


    def round_line(self, up_left_x, up_left_y, box_width, box_height, radius, box_color="b", box_fill=0, line_width=5): # -SPACING, box_width-SPACING-(line_width*2)
        self.round_box(up_left_x, up_left_y, box_width, box_height, radius, box_color, 0, line_width)
        self.round_box(up_left_x+line_width, up_left_y+line_width, box_width-(line_width*2), box_height-(line_width*2), radius/2, box_color, 255, 0)


    def show_pic(self, url, pos_x, pos_y, color="b"):
        urllib.request.urlretrieve(url, "temp_pic.png")
  
        im_pic = Image.open("temp_pic.png")
        
        if color == "b":
            self.im_black.paste(im_pic, (pos_x, pos_y))                        
        elif color == "wb": # Invert black image if necessary
            if im_pic.mode == 'RGBA':
                r,g,b,a = im_pic.split()
                rgb_image = Image.merge('RGB', (r,g,b))
                inverted_image = ImageOps.invert(rgb_image)
                r2,g2,b2 = inverted_image.split()
                final_transparent_image = Image.merge('RGBA', (r2,g2,b2,a))
            else:
                inverted_image = ImageOps.invert(im_pic)
            self.im_black.paste(inverted_image, (pos_x, pos_y))        
        elif color == "wr": # Invert red image if necessary
            if im_pic.mode == 'RGBA':
                r,g,b,a = im_pic.split()
                rgb_image = Image.merge('RGB', (r,g,b))
                inverted_image = ImageOps.invert(rgb_image)
                r2,g2,b2 = inverted_image.split()
                final_transparent_image = Image.merge('RGBA', (r2,g2,b2,a))
            else:
                inverted_image = ImageOps.invert(im_pic)
            self.im_red.paste(inverted_image, (pos_x, pos_y))                     
        else:
            self.im_red.paste(im_pic, (pos_x, pos_y))
