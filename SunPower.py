
# power graph generation 
# filename: powersupplygraph.py
# Version 1.3
#
#

import sys
import time
import RPi.GPIO as GPIO

import gc
from datetime import datetime
from datetime import timedelta

import matplotlib
# Force matplotlib to not use any Xwindows backend.
matplotlib.use('Agg')

from matplotlib import pyplot
from matplotlib import dates

import pylab

import MySQLdb as mdb


def sunpowersupplygraph(source,days,delay,start,end):


		print("sunpower running now")
	

		# now we have to get the data, stuff it in the graph 

		print("trying database")
    		db = mdb.connect('localhost', 'root', 'password', 'SunTracker');

    		cursor = db.cursor()

		query = "SELECT timestamp, deviceid, currentDegrees, battery_load_voltage, battery_current, solarcell_load_voltage, solarcell_current, id FROM SolarPowerData where id > %i AND id < %i " % (start, end)

		print "query=", query

		cursor.execute(query)
		result = cursor.fetchall()

		t = []   # time
		s = []   # rotating panel
		u = []   # stationary panel

		totalTrackedPower = 0
		totalUnTrackedPower = 0
		
		for record in result:
			deviceid = record[1]
  			if (deviceid == 0):
				# convert to PST

				#UTCObject = datetime.strptime(record[0],"%Y-%m-%d %H:%M:%S")
				UTCObject = record[0]
				TimePST = UTCObject - timedelta(seconds=7*60*60)

				#TimeStringPST = TimePST.strftime('%Y-%m-%d %H:%M:%S')
				t.append(TimePST)
  				s.append(record[6]*record[5])
				totalTrackedPower = totalTrackedPower + record[6]*record[5]
			else: 
				u.append(record[6]*record[5])
				totalUnTrackedPower = totalUnTrackedPower + record[6]*record[5]

		print ("count of t=",len(t))

		fds = dates.date2num(t) # converted
		# matplotlib date format object
		hfmt = dates.DateFormatter('%m/%d-%H')

		fig = pyplot.figure()
		fig.set_facecolor('white')
		ax = fig.add_subplot(111,axisbg = 'white')
		ax.vlines(fds, -200.0, 1000.0,colors='w')

		ax.xaxis.set_major_locator(dates.HourLocator(interval=1))
		ax.xaxis.set_major_formatter(hfmt)
		ax.set_ylim(bottom = -200.0)
		pyplot.xticks(rotation='45')
		pyplot.subplots_adjust(bottom=.3)
		pylab.plot(t, s, color='b',label="Sun Tracked Power",linestyle="-",marker=".")
		pylab.plot(t, u, color='r',label="Fixed Power",linestyle="-",marker=".")
		pylab.xlabel("Hours")
		pylab.ylabel("Power mW")
		pylab.legend(loc='lower center')

		print "totalTrackedPower=", totalTrackedPower
		print "totalUnTrackedPower=", totalUnTrackedPower
		totalTrackedPower = totalTrackedPower/(60.0*1000.0)
		totalUnTrackedPower = totalUnTrackedPower/(60.0*1000.0)

		percentIncrease = ((totalTrackedPower/totalUnTrackedPower -1.0)*100.0)

		pylab.axis([min(t), max(t), 0, max(s)+20])
		pylab.figtext(.5, .05, ("SunTracker %s (TP=%6.2fWh, UP=%6.2fWh +%3.1f%%)" %(days,totalTrackedPower, totalUnTrackedPower,percentIncrease)),fontsize=18,ha='center')

		pylab.grid(True)

		pyplot.show()
		pyplot.savefig("/var/www/SunPower-%i.png" % start,facecolor=fig.get_facecolor())	

		cursor.close()       	 
        	db.close()

		del cursor
		del db

		fig.clf()
		pyplot.close()
		pylab.close()
		gc.collect()
		print "finished now"
