from __future__ import print_function

from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import time
from subprocess import call
import httplib2
import os

from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage

#PRESENTATION_ID = '1qLFjf7_tXY1S8WTycuukirbHDaJ6CEso6aTG47tYg1o'
PRESENTATION_ID = '11bF5Qfqnz0NGyJ3cCv4Lwtj48s5AyAjWG7J4T6QkbzU'
#https://docs.google.com/presentation/d/11bF5Qfqnz0NGyJ3cCv4Lwtj48s5AyAjWG7J4T6QkbzU/edit?usp=sharing

URL = "https://docs.google.com/presentation/d/" + PRESENTATION_ID + "/"
TOTAL_SLIDES = 13
OUTPUT = "output/"
FINAL = "final.mp4" 
LIST = "mylist.txt"

# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/slides.googleapis.com-python-quickstart.json
SCOPES = 'https://www.googleapis.com/auth/presentations.readonly'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'Google Slides API Python Quickstart'


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
                                   'slides.googleapis.com-python-quickstart.json')
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

def create_notes_api(presentationId):
	notes = []
	credentials = get_credentials()
	http = credentials.authorize(httplib2.Http())
	service = discovery.build('slides', 'v1', http=http)
	presentation = service.presentations().get(presentationId=presentationId).execute()
	slides = presentation.get('slides')
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

def concat(list, output):
	call(["ffmpeg","-y", "-loglevel", "quiet", "-f", "concat", "-safe", "0", "-i", list, "-c", "copy", output])


def extract_notes(dr):
	ws = dr.find_element_by_id("speakernotes-workspace")
	contents = ws.find_elements_by_class_name("sketchy-text-content-text")
	para = ""
	for content in contents:
	    s = content.text.replace("\n", " ");
	    para = para + s + "\n"
	return para;


def savetxt(dr, file):
	with open(file, "w+") as f:
		f.write(dr.page_source.encode('utf-8'))


def create_audio(text, filename):
	# call(["say", "-v","tom","-r","170", text, "-o", filename])
	call(["say", "-v","tom", text, "-o", filename])

def merge_audio_video(image, audio, output):
	call(["ffmpeg","-y","-loglevel", "quiet","-loop", "1", "-i", image, "-i", audio, "-c:v", "libx264", "-tune", "stillimage", "-c:a", "aac", "-b:a", "192k", "-pix_fmt", "yuv420p", "-shortest", output])


def init():
	call(["mkdir", "-p", OUTPUT])
	dr = webdriver.Chrome()
	dr.get(URL);
	dr.implicitly_wait(1)
	
	#Slideshow
	ActionChains(dr).key_down(Keys.COMMAND).send_keys(Keys.ENTER).key_up(Keys.ENTER).key_up(Keys.COMMAND).perform();
	
	#Wait for elements to disappear
	wait = WebDriverWait(dr, 10)
	try:
		element = wait.until(EC.element_to_be_clickable((By.ID, 'someid')))
	except:
		pass
	return dr


def main():
	notes_all = create_notes_api(PRESENTATION_ID)
	print("Notes: ")
	print(notes_all)
	TOTAL_SLIDES = len(notes_all)
	print("Total Slides: ")
	print(TOTAL_SLIDES)
	dr = init()
	
	with open(LIST, "w") as mylist:
		for i in range(TOTAL_SLIDES):
			print("Taking screenshot")
			ii = str(i)
			pref = OUTPUT + ii
			#Screenshot
			img = pref + ".jpg"
			dr.save_screenshot(img);
			print("Saved screenshot " + img)
				
			#Extract Notes
			#savetxt(dr, pref + ".html")
			notes = extract_notes(dr)
	
			#Save Audio
			audio = pref + ".aiff"
			create_audio(notes_all[i], audio)
			
			#Merge Audio + image
			video = pref + ".mp4"
			merge_audio_video(img, audio, video)
			mylist.write("file " + video + "\n")
		
			#Go to next slide
			ActionChains(dr).send_keys(Keys.ARROW_RIGHT).perform()
			print("Moving to next.")
			
			#wait for 2 seconds
			try:
				myDynamicElement = dr.find_element_by_id("myDynamicElement")
			except:
				pass
	concat(LIST, OUTPUT + FINAL)
	dr.close()

main()

#slides[1]['slideProperties']['notesPage']['pageElements'][1]['shape']['text']['textElements'][1]['textRun']['content']
#slides[1]['slideProperties']['notesPage']['notesProperties']['speakerNotesObjectId']
# i = 0	# 
	# i += 1
	# 	