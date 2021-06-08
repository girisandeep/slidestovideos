import os
# from oauth2client.file import Storage
# from oauth2client import client

from oauth2client import file, client, tools

# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/slides.googleapis.com-python-quickstart.json
SCOPES = ['https://www.googleapis.com/auth/presentations']
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'Google Slides API Python Quickstart'
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

import pickle

def get_credentials():
    store = file.Storage('token.json')
    creds = store.get()
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets('credentials.json', SCOPES)
        creds = tools.run_flow(flow, store)
    return creds

def get_credentials_old():
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
                                   'slides.googleapis.com-python-quickstart.json.old')
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

def get_credentials_older():
    store = file.Storage('token.json')
    creds = store.get()
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets('credentials.json', SCOPES)
        creds = tools.run_flow(flow, store)
    return creds

def get_credentials_olderest():
    creds = None
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server()
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)
    return creds

def save_as_file(txt, file, overwrite=False):
    print ("Saving: " + txt)
    print ("To file: "  + file)
    if not overwrite:
        if os.path.exists(file):
            raise FileExistsError("Path '" + file + "' already exists.")
    with open(file, "w+") as f:
        f.write(txt)

def save_items_as_files(lst, dir):
    for i in range(len(lst)):
        save_as_file(lst[i].encode('utf-8'), dir + "/" + "{:03d}".format(i) + ".txt");

if __name__ == "__main__":
    print(get_credentials())

