from __future__ import print_function
import httplib2
import os

from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage

import datetime

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

SCOPES = 'https://www.googleapis.com/auth/calendar https://www.googleapis.com/auth/spreadsheets'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'Sheets-to-Calendar'


def get_credentials():
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,
                                   'credentials.json')

    store = Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else: # Needed only for compatibility with Python 2.6
            credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials

def main():
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    calendarService = discovery.build('calendar', 'v3', http=http)
    
    discoveryUrl = ('https://sheets.googleapis.com/$discovery/rest?'
                    'version=v4')
    sheetsService = discovery.build('sheets', 'v4', http=http,
                              discoveryServiceUrl=discoveryUrl)
    '''
    SpreadsheetID and sheetRange should be interchanged with your individual
    Spreadsheet's ID and your sheet name as well as range for firstName,
    LastName and Birthday(DD/MM/YY)
    '''
    spreadsheetId = '<SpreadsheetID>'
    sheetRange= '<Sheet_Name>!<Range>'
    #e.g. spreadsheetID = 'ASDfasdf23jase9234jlas9ASDF239'
    #e.g. sheetRange = 'Sheet1!B2:D28'
    results = sheetsService.spreadsheets().values().get(
        spreadsheetId=spreadsheetId, range=sheetRange).execute()
    dataArray = results.get('values', [])

    #Split birthday. If array[0] is 4 characters, assign year. 
    #If array[1] or array[2] is greater than 12,
    #Suggest swappping format for days and months.
    if not dataArray:
        print('No data found.')
    else:
        for row in dataArray:
            #Format fullname and birthday event syntax
            fullname = row[0] + " " + row[1]
            birthday = row[2]
            birthday = birthday.split('/')
            birthday = birthday[1] + "-" + birthday[0]
            event = {
                     'summary': 'It\'s {0} \'s Birthday today'.format(fullname),
                     'location': 'Coder Academy',
                     'description': 'It\'s a students birthday :)',
                     'start': {
                               'dateTime':
                               '2018-{0}T09:00:00+10:00'.format(birthday),
                               'timeZone': 'Australia/Sydney',
                              },
                     'end': {
                             'dateTime':
                             '2018-{0}T17:00:00+10:00'.format(birthday),
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
            event = calendarService.events().insert(calendarId='primary', body=event).execute()

if __name__ == '__main__':
    main()

