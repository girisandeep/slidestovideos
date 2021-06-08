from common import get_credentials
import httplib2
from googleapiclient.discovery import build
from common import save_items_as_files

import os

import argparse

SCOPES = ['https://www.googleapis.com/auth/presentations.readonly']

def set_notes_in_googleslide(presentationId, notes, creds=None):
    if creds == None:
        print "Creating credentials."
        creds = get_credentials()
    # http = credentials.authorize(httplib2.Http())
    service = build('slides', 'v1', credentials=creds)
    presentation = service.presentations().get(presentationId=presentationId).execute()
    slides = presentation.get('slides')
    print("Total Slides: " + str(len(slides)))
    print("Total Notes: " + str(len(notes)))
    requests = []
    i = 0
    start_at = 115
    for slide in slides:
        if i < start_at:
            i += 1
            continue;
        o = slide['slideProperties']['notesPage']['notesProperties']['speakerNotesObjectId']
        if i < len(notes):
            replacementText = notes[i]
        else:
            print("Notes finished before the slides. Stopping.");
            break;
        requests = []
        print("notes object is: ", o)
        print("Appedning Deletion...")
        requests.append({
          "deleteText": {
            "objectId": o,
            "textRange": {
              "type": 'ALL'
            }
          }
        })
        if len(replacementText.strip()) > 0:
            print("Appedning insert...")
            print("replacementText", replacementText)
            requests.append({
              "insertText": {
                "objectId": o,
                "insertionIndex": 0,
                "text": replacementText
              }
            });
        print("About to update %s requests." % len(requests))
        print("SlideCount: ", i)
        #Execute the requests.
        body = {
            'requests': requests
        }
        response = service.presentations().batchUpdate(
            presentationId=presentationId, body=body).execute()
        print("Response:", response)
        
        i += 1
    return notes

def get_notes_from_googleslide(presentationId, credentials=None):
    notes = []
    if credentials == None:
        print "Creating credentials."
        credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('slides', 'v1', http=http)
    presentation = service.presentations().get(presentationId=presentationId).execute()
    slides = presentation.get('slides')
    print("Total Slides: " + str(len(slides)))
    for slide in slides:
        o = slide['slideProperties']['notesPage']['notesProperties']['speakerNotesObjectId']
        slide_notes = ""
        for pe in slide['slideProperties']['notesPage']['pageElements']:
            if pe['objectId'] == o:
                if 'text' in pe['shape']:
                    for te in pe['shape']['text']['textElements']:
                        #print(te)
                        if 'textRun' in te:
                            slide_notes += te['textRun']['content'] + "\n"
        notes.append(slide_notes)
    return notes

def export_notes(presentationId, dir=None, credentials=None):
    if dir == None:
        dir = presentationId
    if not os.path.exists(dir):
        os.mkdir(dir)
    else:
        raise ValueError("Path '" + dir + "' already exists.")
    notes = get_notes_from_googleslide(presentationId, credentials);
    print(notes)
    save_items_as_files(notes, dir)

import regex as re
def ismarker(line):
    return re.match("^===+ *[0-9]+.txt *===+$", line)

def load_notes(scriptfile):
    print("Reading file: %s" % scriptfile)
    f = open(scriptfile)
    notes = []
    isFirst = True
    current_slide_notes = ""
    for line in f:
        if ismarker(line):
            if isFirst:
                isFirst = False
            else:
                notes.append(current_slide_notes.strip())
                current_slide_notes = ""
        else:
           current_slide_notes += line
    notes.append(current_slide_notes)
    return notes;

if __name__ == "__main__":
    # all_notes = get_notes_from_googleslide('11bF5Qfqnz0NGyJ3cCv4Lwtj48s5AyAjWG7J4T6QkbzU')
    # # all_notes = get_notes_from_googleslide('11bF5Qfqnz0NGyJ3cCv4Lwtj48s5AyAjWG7J4T6QkbzU', get_credentials())
    # for notes in all_notes:
    #     print(notes)
    parser = argparse.ArgumentParser(description='Update notes in google slides from script. Script file should have the notes separted by ======= NNN.txt =======. The number doesnt matter the order does')
    parser.add_argument('slidesid', metavar='SlideId', type=str, help='The id of the Google Slide.')#, nargs=1)
    parser.add_argument('scriptfile', metavar='scriptfile', type=str, help='The file having === num.txt === separator', nargs='?')
    
    args = parser.parse_args()

    set_notes_in_googleslide(args.slidesid, load_notes(args.scriptfile))
    #export_notes('11bF5Qfqnz0NGyJ3cCv4Lwtj48s5AyAjWG7J4T6QkbzU', 'notes-out')
    #export_notes('1SHpt66tDkypD4CDg_tRWgtE3auHcHMITOIpl0pWp0as', 'underpinning_tom.txt')
