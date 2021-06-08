from common import get_credentials
import httplib2
from apiclient import discovery
from common import save_items_as_files
from googleapiclient.discovery import build
from httplib2 import Http

import os

import argparse

def get_notes_from_googleslide(presentationId, credentials=None):
    notes = []
    if credentials == None:
        print("Creating credentials.")
        credentials = get_credentials()
    service = build('slides', 'v1', http=credentials.authorize(Http()))
    # http = credentials.authorize(httplib2.Http())
    # service = discovery.build('slides', 'v1', http=http)
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

if __name__ == "__main__":
    # all_notes = get_notes_from_googleslide('11bF5Qfqnz0NGyJ3cCv4Lwtj48s5AyAjWG7J4T6QkbzU')
    # # all_notes = get_notes_from_googleslide('11bF5Qfqnz0NGyJ3cCv4Lwtj48s5AyAjWG7J4T6QkbzU', get_credentials())
    # for notes in all_notes:
    #     print(notes)
    parser = argparse.ArgumentParser(description='Export notes from google slides. The files will be created per slide. The name will n.txt where n starts from 0.')
    parser.add_argument('slidesid', metavar='SlideId', type=str, help='The id of the Google Slide.')#, nargs=1)
    parser.add_argument('dir', metavar='Directory', type=str, help='The directory in which these notes will be saved.', nargs='?')
    
    args = parser.parse_args()

    export_notes(args.slidesid, args.dir)

    # export_notes('11bF5Qfqnz0NGyJ3cCv4Lwtj48s5AyAjWG7J4T6QkbzU', 'notes-out')
