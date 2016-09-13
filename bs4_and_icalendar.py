#I wrote this in 2016 to grab the TA office hours off the website and import them
#into icalendar.  Took a few hours to write this which probably spend more time
#than if I had just manually written them in, but hey, I got some practice

from icalendar import Calendar, Event
from bs4 import BeautifulSoup

from icalendar import vCalAddress, vText

# cal is the base object that everything else gets added onto
cal = Calendar()

#python time zones
import pytz


cal.add('prodid', '-//Created in Python//')
cal.add('version', '2.0')

from datetime import datetime, timedelta

with open ("160oh.html") as f:
	html_doc = f.read()


def parsedate():
	pass

#Python classes are more like elaborate hash tables
#which is why the code below looks object oriented
#and this code looks like hash tables
#Note, this function wasn't needed by the end of everything
def fill_and_add(event, name, start, end):
	event['SUMMARY'] = '380 OH' + name
	event['RRULE'] = 'FREQ-WEEKLY'
	event['UNTIL'] = TERMINATION_DATE
	event['DTEND'] = 'TZID=America/New_York:' + end
	event['TRANSP'] = 'OPAQUE'
	event['X-APPLE-TRAVEL-ADVISORY-BEHAVIOR'] = 'AUTOMATIC'
	event['DTSTART'] = 'TZID=America/New_York:' + start
	event['DTSTAMP'] = '20160912T182350Z' #Date object was created
	event['SEQUENCE'] = 0
	event['END'] = 'VEVENT'
	event['BEGIN'] = 'VEVENT'
	event['CREATED'] = '20160912T182402Z'
	cal.add_component(event)

#I downloaded the website first and saved it.  Future versions should
#just pull from the web server
soup = BeautifulSoup(html_doc, 'html.parser')

#b ends up being a list of all the portions of the site of interest
b = soup.find_all(attrs={'staff-info'})

#all of these little staff info boxes looked the same so I could just
#iterate through them and pull out the relevant data
for staff_info_entry in b:

	raw_name = str(staff_info_entry.h1)
	trimmed_name = raw_name[4:-5] 	#trim off the html code
									#but I think there is some better code
									#that can do that.

	#find the date entry by working backwards from the last line in the box
	raw_date = str(staff_info_entry.contents[-2])
	trimmed_date = raw_date[7:-4]  #trim off the html code
	splitted_date_and_time = trimmed_date.split() #splits based on whitespace

	#day_of_week serves two functions, one as the keys in the hash table for
	#september month days.  Two, the first two characters get used to generate
	#the RRULE
	day_of_week = splitted_date_and_time[0]
	start_and_end_time = splitted_date_and_time[1].split('-')
	start_time = int(start_and_end_time[0])+12
	end_time = int(start_and_end_time[1])+12

	day_hashtable = {	'Monday':12,'Tuesday':13,
						'Wednesday':14,'Thursday':15,
						'Friday':16,'Saturday':17,'Sunday':18}

	formated_summary = trimmed_name + ' OH'
	a = datetime(2016,9,day_hashtable[day_of_week],start_time,0,0,tzinfo=pytz.est)
	b = datetime(2016,9,day_hashtable[day_of_week],end_time,0,0,tzinfo=pytz.est)
	c = datetime(2015,8,day_hashtable[day_of_week],0,0,tzinfo=pytz.est)

	#sadly, after all this work I found out that icalendar doesn't suppert
	#repeated events, so I had to create these manually

	for x in range(14):
		a = a + timedelta(7,0)
		b = b + timedelta(7,0)
		event = Event()
		event.add('summary', formated_summary)
		event.add('dtstart', a)
		event.add('dtend', b)
		event.add('dtstamp', c)
		cal.add_component(event)

def display(cal):
	return cal.to_ical().replace('\r\n', '\n').strip()

print(display(cal))

import tempfile, os
directory = '/Users/chrisoaks/Documents'
with open(os.path.join(directory, 'TAofficehours2.ics'), 'wb') as f:
	f.write(cal.to_ical())
