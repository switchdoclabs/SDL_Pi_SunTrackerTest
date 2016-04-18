
"""
doAllGraphs.py
JCS 4/17/2016 Version 1.0
This program runs the data collection, graph preperation, housekeeping and actions
"""

from datetime import datetime, timedelta
import sys
import time


import SunCurrent 
import SunPower 
import SunVoltage 

SunVoltage.sunvoltagesupplygraph("test","Apr 1",1,11274,12679)
SunVoltage.sunvoltagesupplygraph("test","Mar 31",1,9536,11275)
SunVoltage.sunvoltagesupplygraph("test","Mar 30",1,8134,9537)


#SunCurrent.suncurrentsupplygraph("test","Apr 1",1,11274,12679)
#SunCurrent.suncurrentsupplygraph("test","Mar 31",1,9536,11275)
#SunCurrent.suncurrentsupplygraph("test","Mar 30",1,8134,9537)

#SunPower.sunpowersupplygraph("test","Apr 1",1,11274,12679)
#SunPower.sunpowersupplygraph("test","Mar 31",1,9536,11275)
#SunPower.sunpowersupplygraph("test","Mar 30",1,8134,9537)


