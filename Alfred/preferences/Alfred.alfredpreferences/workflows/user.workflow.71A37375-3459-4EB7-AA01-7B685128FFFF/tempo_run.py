#MARK: LIBRARIES
import argparse
import json
import re
from lib import requests
import os
from datetime import datetime
from datetime import date
from datetime import timedelta
from lib.icalevents.icalevents import events

#MARK: CUSTOM LIBRARIES
from lib import utils

#MARK: PARSER
parser = argparse.ArgumentParser(description='My tool')
parser.add_argument('--date', type=date.fromisoformat, required=True)

#MARK: GLOBALS
args = parser.parse_args()
calendar_url = 'webcal://p103-caldav.icloud.com/published/2/ODA5NjY1Mjg2NDgwOTY2NQo_4ou_e9iiE7Pyt-cF1X-yjyW3oimOA_IaeSb_ziTEeuUDoYlCqGRj28g4HHwNaxQrSNyaxDZXM6_KC6CWy7w'

#MARK: FUNCTIONS
def get_events(date):
    start = datetime(date.year, date.month, date.day, 0, 0)
    end = datetime(date.year, date.month, date.day, 23, 59)
    es  = events(calendar_url, fix_apple=True, start= start, end= end)
    for event in es:
        print(event.summary)
        print(event.description)
        print(event.start)
        print(event.end)
        delta = event.end - event.start
        seconds = delta.seconds
    return es


def is_ticket_number(value):
    return 'IT' in value or 'AVIO' in value or 'AM' in value or 'SYS' in value

def create_tempo_event(event):
    is_avio_ticket = True if 'avio' in event.summary.lower() else False
    ticket_number = event.summary.split(' ')[0]
    if is_avio_ticket is False and is_ticket_number(ticket_number) is False:
        return None
    tempo_event = {}
    tempo_event['issueKey'] = ticket_number
    tempo_event['timeSpentSeconds'] = int((event.end - event.start).total_seconds())
    tempo_event['startDate'] = utils.date_to_string(event.start, format='%Y-%m-%d')
    tempo_event['startTime'] = utils.date_to_string(event.start, format='%H:%M:%S')
    tempo_event['description'] = event.description if event.description is not None else "Working on {}".format(ticket_number)
    tempo_event['authorAccountId'] = '70121:973e8096-498a-4a77-88b3-abb188b7ebaa'
    return tempo_event

def upload_event(event):
    url = 'https://api.tempo.io/core/3/worklogs'
    headers = { 'Authorization': 'Bearer S07FB600NbvRDSSVH4FLrlSHdupwvO', 'Content-type': 'application/json'}
    x = requests.post(url, json=event, headers=headers)

#MARK: MAIN
def main():
    events = get_events(args.date)
    print('Calendar items found: {}'.format(len(events)))
    time_logs_added = 0
    for event in events:
        tempo_event = create_tempo_event(event)
        if tempo_event is not None:
            upload_event(tempo_event)
            time_logs_added += 1

    print('Tempo items added: {}'.format(time_logs_added))

if __name__ == "__main__":
    print('---------------------------------')
    print('Start Running')
    print('---------------------------------')
    main()
    print('---------------------------------')
    print('That is all, thank you!')
    print('---------------------------------\n')
