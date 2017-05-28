from extract_notes import get_notes_from_googleslide

def init(presentation_id, output_dir):

    url = "https://docs.google.com/presentation/d/" + presentation_id + "/"

    call(["mkdir", "-p", output_dir])
    dr = webdriver.Chrome()
    dr.get(url);
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


def take_screen_shots(presentation_id, total_slides=-1, output_dir):
    if total_slides = -1:
        total_slides = len(get_notes_from_googleslide());

    dr = init(presentation_id, output_dir)
    for i in range(total_slides):
            ii = str(i)
            pref = output_dir + ii
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

if __name__ == "__main__":
    # all_notes = get_notes_from_googleslide('11bF5Qfqnz0NGyJ3cCv4Lwtj48s5AyAjWG7J4T6QkbzU')
    # # all_notes = get_notes_from_googleslide('11bF5Qfqnz0NGyJ3cCv4Lwtj48s5AyAjWG7J4T6QkbzU', get_credentials())
    # for notes in all_notes:
    #     print(notes)
    parser = argparse.ArgumentParser(description='Export notes from google slides. The files will be created per slide. The name will n.txt where n starts from 0.')
    parser.add_argument('slidesid', metavar='SlideId', type=str, help='The id of the Google Slide.')#, nargs=1)
    parser.add_argument('total_slides', metavar='total_slides', type=str, help='Total Number of slides', nargs='?')#, nargs=1)
    parser.add_argument('dir', metavar='Directory', type=str, help='The directory in which these screenshots will be saved.', nargs='?')
    
    args = parser.parse_args()
    take_screen_shots(args.slidesid, args.total_slides, args.dir)
    # export_notes('11bF5Qfqnz0NGyJ3cCv4Lwtj48s5AyAjWG7J4T6QkbzU', 'notes-out')
