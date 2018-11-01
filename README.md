Welcome to the Sheets-to-Calendar script. To use this script there are a few things that we need to setup in order for Google to give us permission to use their service.

Please login to https://console.developers.google.com/apis/credentials and download the credentials file. You will need to do this everytime you clone the repository as pushing the credentials to Github is a security risk(Both the 'credentials.json' and 'token.json' files have been added to the '.gitignore' file so they are excluded from git commits)

Once downloaded you will need to move the file into the working directory and rename to 'credentials.json'

Using the 'mv' command is useful for accomplishing this step on unix-based systems. Documentation on use can be found by running 'man mv'.

Use 'Python3 application.py' to run the script. You will need to have python3 installed in order for the google-client module to work. Python2 will not be sufficient.

Running the script for the first time will read the 'credentials.json' file and authenticate using google's OATH2 workflow(This wil open the default browser).

Accepting the OATH2 workflow will create a 'token.json' file which contains your access token. This will be used everytime we send a request to a Google API.

If the scope of the project changes, you will need to delete your 'token.json' file and run the workflow again.
