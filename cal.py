#!/usr/bin/env python3
## https://github.com/zylai/ical-fake-meetings-generator/blob/master/iCal_Fake_Events_Generator.py
from pathlib import Path
import os.path
from os import path
import sys
from calendar import monthrange
from datetime import datetime,timedelta
import uuid
import random
import re

##### User-definable options, start editing here #####

file_location = str(Path.home()) + "/calendar.ics"
break_length_options = [-90,-60,-30,0,0,0,15,15,15,30,30,60,90]
event_length_options = [15,15,30,30,30,30,30,45,45,60,60,60,60,60,60,60,60,90,90,90,120,120,120,240]

def getArgs():
	import argparse
	parser = argparse.ArgumentParser("Calendar Creation")
	parser.add_argument("-y","--year", help="The year", nargs="*", default=["2023"])
	parser.add_argument("-m","--month", help="The month", nargs="*", default=["10"])
	args,unknown = parser.parse_known_args()
	return args

argz = getArgs()

##### Start of script, stop editing here #####

if path.exists(file_location):
	print("\033[91mAn existing iCalendar file is already at: " + file_location + "\033[0m")
	print("\033[91mDelete this file to generate another one. Aborting...\033[0m")
	sys.exit(1)

user_input_year = argz.year
user_input_month = argz.month

regex_time = "^(([0-9])|([0-1][0-9])|([2][0-3]))([0-5][0-9])$"

user_input_begin_time = "0800"
user_input_end_time = "1700"

day_begin_hour = user_input_begin_time[0:2]
day_begin_minute = user_input_begin_time[2:4]
day_end_hour = user_input_end_time[0:2]
day_end_minute = user_input_end_time[2:4]

days_in_month = monthrange(int(user_input_year), int(user_input_month))[1]

utc_offset = str(datetime.now().astimezone().isoformat())[26:33]

calendar_template_begin = """BEGIN:VCALENDAR
PRODID:-//ZYLAI//iCal Fake Events Generator//EN
VERSION:2.0
METHOD:PUBLISH
"""

ics_file = open(file_location, "a")
ics_file.write(calendar_template_begin)

for day in range(1, days_in_month + 1):
	day_date = datetime(int(user_input_year), int(user_input_month), day)

	if ((day_date.strftime('%A') == "Saturday") or (day_date.strftime('%A') == "Sunday")):
		continue

	day_begin_utc = datetime.strptime("" + user_input_year + user_input_month.zfill(2) + str(day).zfill(2) + day_begin_hour + day_begin_minute + "00" + utc_offset, '%Y%m%d%H%M%S%z').utctimetuple()
	day_end_utc = datetime.strptime("" + user_input_year + user_input_month.zfill(2) + str(day).zfill(2) + day_end_hour + day_end_minute + "00" + utc_offset, '%Y%m%d%H%M%S%z').utctimetuple()

	day_begin = datetime(day_begin_utc.tm_year, day_begin_utc.tm_mon, day_begin_utc.tm_mday, day_begin_utc.tm_hour, day_begin_utc.tm_min, 0)
	day_end = datetime(day_end_utc.tm_year, day_end_utc.tm_mon, day_end_utc.tm_mday, day_end_utc.tm_hour, day_end_utc.tm_min, 0)

	event_end = day_begin

	while (event_end < day_end):
		break_length = timedelta(minutes = random.choice(break_length_options))
		event_end = event_end + break_length
		event_begin = event_end
		event_length = timedelta(minutes = random.choice(event_length_options))
		event_end = event_begin + event_length

		event_template = """BEGIN:VEVENT
CLASS:PRIVATE
DESCRIPTION:
DTSTAMP:{}
DTSTART:{}
DTEND:{}
PRIORITY:9
SEQUENCE:0
TRANSP:OPAQUE
UID:{}
END:VEVENT
""".format(datetime.utcnow().strftime('%Y%m%dT%H%M%SZ'), event_begin.strftime('%Y%m%dT%H%M%SZ'), event_end.strftime('%Y%m%dT%H%M%SZ'), str(uuid.uuid4()))

		ics_file.write(event_template)

calendar_template_end = "END:VCALENDAR"

ics_file.write(calendar_template_end)

ics_file.close

print("\033[92miCalendar file generated successfully and has been saved to: " + file_location + "\033[0m")

sys.exit(0)