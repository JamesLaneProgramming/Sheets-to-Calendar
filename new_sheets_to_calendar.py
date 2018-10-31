from __future__ import print_function
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools

import psycopg2

# If modifying these scopes, delete the file token.json.
SCOPES = 'https://www.googleapis.com/auth/spreadsheets.readonly'

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
    SPREADSHEET_ID = '1U3yzTCYoC2dGMGdgy1wTU-v0vbcobBp8kMSVoABMxis'
    RANGE_NAME = 'Date of Birth by Location!A2:D'
    result = service.spreadsheets().values().get(spreadsheetId=SPREADSHEET_ID,
                                                range=RANGE_NAME).execute()
    values = result.get('values', [])
    one_tested = False
    if not values:
        print('No data found.')
    else:
        print('Name, Major:')
        for row in values:
            #Print columns A and E, which correspond to indices 0 and 4.
            full_name = row[0]
            birthday = row[1].split("/")
            print(full_name)
            print(birthday)
            if(one_tested == False):
                create_calendar_event(calendar_service, full_name, birthday)
                one_tested = True

def create_calendar_event(service, full_name, birthday):
    event = {
            'summary': 'It\'s {0} \'s Birthday today'.format(full_name),
            'location': 'Coder Academy',
            'description': 'It\'s a students birthday :)',
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

             'attendees': [
                           {'email': 'Test@email.com'},
                          ],
             'reminders': {
                           'useDefault': False,
                           'overrides': [
                                         {'method': 'email', 'minutes': 24 * 60},
                                         {'method': 'popup', 'minutes': 10},
                                        ],
                          },
             }
    event = service.events().insert(calendarId='primary', body=event).execute()
if __name__ == '__main__':
    main()
