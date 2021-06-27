from __future__ import print_function
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/presentations.readonly']

def get_credentials():
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    return creds

def save_as_file(txt, file, overwrite=False):
    # print ("Saving: ",txt)
    # print ("To file: ", file)
    # if not overwrite:
    #     if os.path.exists(file):
    #         raise FileExistsError("Path '" + file + "' already exists.")
    tmpfile = file + "._tmp"
    with open(tmpfile, "wb+") as f:
        f.write(txt)
    move_tmp_to_actual(tmpfile, file)

def move_tmp_to_actual(tmpfile, file):
    if os.path.exists(file):
        # Find diff
        cmd = "md5sum %s %s|awk '{print $1}'|sort|uniq" %(tmpfile, file)
        if len(os.popen(cmd).read().split()) == 1:
            print("Same content exists. Removing newly downloaded file.")
            print(os.popen("rm %s" %tmpfile).read())
            return
    print(os.popen("mv %s %s" %(tmpfile, file)).read())


def save_items_as_files(lst, dir):
    for i in range(len(lst)):
        save_as_file(lst[i].encode('utf-8'), dir + "/" + "{:03d}".format(i) + ".txt");

if __name__ == "__main__":
    print(get_credentials())

