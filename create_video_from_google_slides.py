from __future__ import print_function

from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import time

import httplib2
import os

from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage
from extract_notes import get_notes_from_googleslide
from create_audio import create_audio

#PRESENTATION_ID = '1qLFjf7_tXY1S8WTycuukirbHDaJ6CEso6aTG47tYg1o'
PRESENTATION_ID = '11bF5Qfqnz0NGyJ3cCv4Lwtj48s5AyAjWG7J4T6QkbzU'
#https://docs.google.com/presentation/d/11bF5Qfqnz0NGyJ3cCv4Lwtj48s5AyAjWG7J4T6QkbzU/edit?usp=sharing

URL = "https://docs.google.com/presentation/d/" + PRESENTATION_ID + "/"
TOTAL_SLIDES = 13
OUTPUT = "output/"
FINAL = "final.mp4" 
LIST = "mylist.txt"

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
	notes_all = get_notes_from_googleslide(PRESENTATION_ID)
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
			#save_as_file(dr.page_source.encode('utf-8'), pref + ".html")
			# notes = extract_notes(dr)
	
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