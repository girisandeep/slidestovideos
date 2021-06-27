from googleapiclient.discovery import build
from common import get_credentials
import requests
import argparse

def get_slide_objectids(service, presentationId):
    presentation = service.presentations().get(presentationId=presentationId).execute()
    slides_ids = [slide['objectId'] for slide in presentation['slides']]
    return slides_ids

def save_thumbnail(filename, res, exception):
    print("filename: ", filename)
    print("Response: ", res)
    response = requests.get(res['contentUrl'])
    file = open(filename, "wb")
    file.write(response.content)
    file.close()

def take_screen_shots(presentationId, outdir):
    # if creds == None:
    #     print("Creating credentials.")
    creds = get_credentials()
    service = build('slides', 'v1', credentials=creds)
    slides_ids = get_slide_objectids(service, presentationId)
    br = service.new_batch_http_request(save_thumbnail)
    for i, slideId in enumerate(slides_ids):
        br.add(service.presentations().pages().getThumbnail(presentationId = presentationId,pageObjectId=slideId, thumbnailProperties_mimeType="PNG",thumbnailProperties_thumbnailSize="LARGE"), request_id=outdir + "/" + str(i+1) + ".png")
    br.execute()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Export notes from google slides. The files will be created per slide. The name will n.txt where n starts from 0.')
    parser.add_argument('slidesid', metavar='SlideId', type=str, help='The id of the Google Slide.')#, nargs=1)
    parser.add_argument('dir', metavar='Output Directory', type=str, help='The directory in which these screenshots will be saved.')
    
    args = parser.parse_args()
    take_screen_shots(args.slidesid, args.dir)
