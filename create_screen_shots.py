from extract_notes import get_notes_from_googleslide
import argparse
import os
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import pickle
from selenium.webdriver.support.ui import WebDriverWait
from os.path import expanduser
import hashlib
import sys
import time
from subprocess import call
def hash(s):
    m = hashlib.md5()
    m.update(s)
    return m.hexdigest()

cookie_dir = expanduser("~") + "/.seleniumsessions"
cookie_file = cookie_dir + "/cookies"

def gen_cookie_file(url, cookie_file_name=None):
    
    if not os.path.exists(cookie_dir):
        os.mkdir(cookie_dir)
    if cookie_file_name == None:
        cookie_file_name = hash(url)
    cookie_file = cookie_dir + "/" + cookie_file_name
    return cookie_file;

def loadcookies(driver, url, cookie_file_name=None):
     #gen_cookie_file(url, cookie_file_name)
    if os.path.exists(cookie_file):
        # for cookie in pickle.load(open(cookie_file, "rb")):
        #     driver.add_cookie(cookie)
        return (cookie_file, True)
    else:
        return (cookie_file, False)

def savecookies(driver, url, cookie_file_name=None):
    # cookie_file = gen_cookie_file(url, cookie_file_name)
    pickle.dump(driver.get_cookies() , open(cookie_file,"wb"))

def fullscreen(dr):
    dr.implicitly_wait(1)

    #Slideshow
    ActionChains(dr).key_down(Keys.COMMAND).send_keys(Keys.ENTER).key_up(Keys.ENTER).key_up(Keys.COMMAND).perform();
    
    time.sleep(10)
    #Wait for elements to disappear
    wait = WebDriverWait(dr, 20)
    try:
        element = wait.until(EC.element_to_be_clickable((By.ID, 'someid')))
    except:
        pass


def init(url, output_dir=None):
    if output_dir == None:
        output_dir = hash(url)
    if not os.path.exists(output_dir):
        os.mkdir(output_dir)
    else:
        raise ValueError("Path '" + output_dir + "' already exists.")
    dr = webdriver.Chrome()
    dr.get(url)
    (cookie_file, cookie_exists) = loadcookies(dr, url)
    dr.implicitly_wait(1)
    
    return (dr, cookie_file, cookie_exists)

def query_yes_no(question, default="yes"):
    """Ask a yes/no question via raw_input() and return their answer.

    "question" is a string that is presented to the user.
    "default" is the presumed answer if the user just hits <Enter>.
        It must be "yes" (the default), "no" or None (meaning
        an answer is required of the user).

    The "answer" return value is True for "yes" or False for "no".
    """
    valid = {"yes": True, "y": True, "ye": True,
             "no": False, "n": False}
    if default is None:
        prompt = " [y/n] "
    elif default == "yes":
        prompt = " [Y/n] "
    elif default == "no":
        prompt = " [y/N] "
    else:
        raise ValueError("invalid default answer: '%s'" % default)

    while True:
        sys.stdout.write(question + prompt)
        choice = input().lower()
        if default is not None and choice == '':
            return valid[default]
        elif choice in valid:
            return valid[choice]
        else:
            sys.stdout.write("Please respond with 'yes' or 'no' "
                             "(or 'y' or 'n').\n")

def take_screen_shots(presentation_id, output_dir=None, total_slides=None):
    url = "https://docs.google.com/presentation/d/" + presentation_id + "/"

    if total_slides == None:
        total_slides = len(get_notes_from_googleslide(presentation_id));

    (dr,cookie_file, cookie_exists)  = init(url, output_dir)
    
    if not query_yes_no("Have you logged-in in chrome. Should we continue?", default="yes"):
        print("Exiting...")
        return

    # if query_yes_no("Do you want to save the session?", default="yes"):
    #     savecookies(dr, url)
    
    fullscreen(dr);

    for i in range(total_slides):
            ii = "{:03d}".format(i)
            pref = output_dir + "/" + ii
            img_file_name = pref + ".jpg"

            dr.save_screenshot(img_file_name);
            print("Saved screenshot " + img_file_name)

            ActionChains(dr).send_keys(Keys.ARROW_RIGHT).perform()
            print("Moving to next.")
            
            #wait for 2 seconds
            try:
                myDynamicElement = dr.find_element_by_id("myDynamicElement")
            except:
                pass
    call(["say", "Finished taking screenshot. You can press escape to exit fullscreen"]);
    if query_yes_no("Do you want to save the session?", default="yes"):
        savecookies(dr, url)

if __name__ == "__main__":
    # all_notes = get_notes_from_googleslide('11bF5Qfqnz0NGyJ3cCv4Lwtj48s5AyAjWG7J4T6QkbzU')
    # # all_notes = get_notes_from_googleslide('11bF5Qfqnz0NGyJ3cCv4Lwtj48s5AyAjWG7J4T6QkbzU', get_credentials())
    # for notes in all_notes:
    #     print(notes)
    parser = argparse.ArgumentParser(description='Export notes from google slides. The files will be created per slide. The name will n.txt where n starts from 0.')
    parser.add_argument('slidesid', metavar='SlideId', type=str, help='The id of the Google Slide.')#, nargs=1)
    parser.add_argument('dir', metavar='Directory', type=str, help='The directory in which these screenshots will be saved.', nargs='?')
    parser.add_argument('total_slides', metavar='total_slides', type=int, help='Total Number of slides', nargs='?')#, nargs=1)
    
    args = parser.parse_args()
    take_screen_shots(args.slidesid, args.dir, args.total_slides )
    # export_notes('11bF5Qfqnz0NGyJ3cCv4Lwtj48s5AyAjWG7J4T6QkbzU', 'notes-out')
