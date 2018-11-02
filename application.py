from __future__ import print_function
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools

import psycopg2

# If modifying these scopes, delete the file token.json.
SCOPES = 'https://www.googleapis.com/auth/spreadsheets.readonly https://www.googleapis.com/auth/calendar'

brisbane_attendees_emails = [
        'ashleigh.wilson@coderacademy.edu.au', 
        'janel.brandon@coderacademy.edu.au', 
        'matt.etherington@coderacademy.edu.au'
        ]
sydney_attendees_emails = [
        'garret.blankenship@coderacademy.edu.au',
        'saad.saeed@coderacademy.edu.au',
        'mel.redding@coderacademy.edu.au',
        'steph.schaffer@coderacademy.edu.au',
        'gemma.thompson@coderacademy.edu.au',
        'pauline.futeran@coderacademy.edu.au'
        ]
melbourne_attendees_emails = [
        'matt.mckenzie@coderacademy.edu.au', 
        'ruegen.aschenbrenner@coderacademy.edu.au', 
        'gretchen.scott@coderacademy.edu.au', 
        'samara.jesney@coderacademy.edu.au', 
        'harrison.malone@coderacademy.edu.au'
        ]

def main():
    """Shows basic usage of the Sheets API.
    Prints values from a sample spreadsheet.
    """
    store = file.Storage('token.json')
    creds = store.get()
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets('credentials.json', SCOPES)
        creds = tools.run_flow(flow, store)
    service = build('sheets', 'v4', http=creds.authorize(Http()))
    calendar_service = build('calendar', 'v3', http=creds.authorize(Http()))
    # Call the Sheets API
    SPREADSHEET_ID = '1AChP79VYiq06pqJVMnnv-Tvgy7ePMmvza1CG06CAyuA'
    RANGE_NAME = 'Date of Birth by Location!A2:D'
    result = service.spreadsheets().values().get(spreadsheetId=SPREADSHEET_ID,
                                                range=RANGE_NAME).execute()
    values = result.get('values', [])

    if not values:
        print('No data found.')
    else:
        print('Name, Major:')
        for row in values:
            #Print columns A and E, which correspond to indices 0 and 4.
            full_name = row[0]
            birthday = row[1].split("/")
            campus = row[3]
            if(campus == 'Coder Academy (Melbourne)'):
                attendees = create_attendees_object(melbourne_attendees_emails)
                create_calendar_event(calendar_service, full_name, birthday, attendees)
            if(campus == 'Coder Academy (Sydney)'):
                attendees = create_attendees_object(sydney_attendees_emails)
                create_calendar_event(calendar_service, full_name, birthday, attendees)
            if(campus == 'Coder Academy (Brisbane)'):
                attendees = create_attendees_object(brisbane_attendees_emails)
                create_calendar_event(calendar_service, full_name, birthday, attendees)

def create_attendees_object(attendees):
    '''
    Takes a list of attendees email addresses and returns an object for use in a calendar event.
    '''
    attendees_object = []
    for attendee in attendees:
        attendees_object.append({'email': str(attendee)})
    return attendees_object

def create_calendar_event(service, full_name, birthday, attendees):
    event = {
            'summary': 'It\'s {0} \'s birthday today'.format(full_name),
            'location': 'Coder Academy',
            'description': 'It\'s a student\'s birthday :)',
            'start': {
                'dateTime':
                '2018-{0}-{1}T09:00:00+10:00'.format(birthday[1], birthday[0]),
                'timeZone': 'Australia/Sydney',
                },
            'end': {
                'dateTime':
                '2018-{0}-{1}T10:00:00+10:00'.format(birthday[1], birthday[0]),
                'timeZone': 'Australia/Sydney',
                },
            'attendees': attendees,
            'reminders': {
                'useDefault': False,
                'overrides': [
                        {'method': 'email', 'minutes': 24 * 60},
                        {'method': 'popup', 'minutes': 10},
                    ],
                },
             }
    print(event)
    event = service.events().insert(calendarId='primary', body=event).execute()
if __name__ == '__main__':
    main()
