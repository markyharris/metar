# metar_settings.py
# Metar Display Settings - Mark Harris
#
# These settings will be used if script is run with no cmd line arguments

# Default User Settings
airport = "KFLG" # enter default airport identifier to display
interval = 1800  # enter default time in seconds between METAR updates - 3600 = 1 hour
use_disp_format = 7 # Choose which display layout to use. -1 = Random layout, -2 = Cycle layouts
use_remarks = 1  # 0 = display airport information, 1 = display metar remarks info

# Random Airports Choices (Layout5):
# This is the only layout that doesn't use cmd line arguments
# For the same airports in the same locations on screen, place 12 airports in list. The 13th will be the default airport
# For randomly selected airports, put more than 12 in list. 12 will randomly be displayed, 13th will be default
# If you put less than 12 airports in list, it will pad the missing spots with the default airport above.
random_airports = ["KEYW","KFVE","KSEA","KCVG", "KLAS","KCMR","KGRR","KMSN", \
                   "KLAX","KNBC","KFVE","KBUF"] #, "KTPA", "KLAS","KGEU","KOLS", \
                  # "KSAN", "KPDX", "KBOI", "KMSP", "KSTL", "KBNA", "KTYS"] 

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
           