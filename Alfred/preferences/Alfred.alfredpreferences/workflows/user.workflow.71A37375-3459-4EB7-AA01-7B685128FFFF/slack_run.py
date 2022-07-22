#MARK: LIBRARIES
import argparse
import json
import re
import requests
import os
import sys
from datetime import datetime
from datetime import date
from datetime import timedelta
from icalevents.icalevents import events

#MARK: CUSTOM LIBRARIES
from lib import utils

#MARK: PARSER
parser = argparse.ArgumentParser(description='My tool')
parser.add_argument('--date', type=date.fromisoformat, required=False)

#MARK: GLOBALS
args = parser.parse_args()
calendar_url = 'webcal://p44-caldav.icloud.com/published/2/ODA5NjY1Mjg2NDgwOTY2NQo_4ou_e9iiE7Pyt-cF1X-yjyW3oimOA_IaeSb_ziTEeuUDoYlCqGRj28g4HHwNaxQrSNyaxDZXM6_KC6CWy7w'

#MARK: FUNCTIONS
def get_events(date):
    start = datetime(date.year, date.month, date.day, 0, 0)
    end = datetime(date.year, date.month, date.day, 23, 59)
    es  = events(calendar_url, fix_apple=True, start= start, end= end)
    return es

def is_ticket_number(value):
    return 'IT' in value or 'AVIO' in value or 'AM' in value

def create_event(event):
    is_avio_ticket = True if 'avio' in event.summary.lower() else False
    ticket_number = event.summary.split(' ')[0]
    if is_avio_ticket is False and is_ticket_number(ticket_number) is False:
        return None
    if ticket_number == "IT-19":
        ticket_number = "Meeting"
    if ticket_number == "AM-1":
        ticket_number = "Analysis"
    return ticket_number + " " + event.description if event.description.strip() is not None else ""

def get_events_string(day, events):
    events_print = "{}: \n".format(day)
    created_events = []
    for event in events:
        created_events.append(create_event(event))

    for created_event in list(set(created_events)):
        if created_event is not None:
            events_print += "* {} \n".format(created_event.strip())
    return events_print
#MARK: MAINa
def main():
    today = date.today()
    yesterday = today - timedelta(days=1)
    yesterday_events = get_events(yesterday)
    today_events = get_events(today)
    yesterday_events_print = get_events_string("Yesterday", yesterday_events)
    today_events_print = get_events_string("Today", today_events)
    path = sys.path[0] + "/.temp/output.txt"
    with open(path, "w") as text_file:
        text_file.write(yesterday_events_print + today_events_print)

if __name__ == "__main__":
    print('---------------------------------')
    print('Start Running')
    print('---------------------------------')
    main()
    print('---------------------------------')
    print('That is all, thank you!')
    print('---------------------------------\n')
