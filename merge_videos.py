from subprocess import call
import os
import argparse

def concat(lst, output):
    print "output: " + output
    call(["ffmpeg","-y", "-loglevel", "quiet", "-f", "concat", "-safe", "0", "-i", lst, "-c", "copy", output])

def concat_all(videos_dir, output_filename):
    videos = os.listdir(videos_dir)
    videos.sort();
    LIST = "to_merge.lst"
    with open(LIST, "w") as mylist:
        for video in videos:
            mylist.write("file " + videos_dir + "/" + video + "\n")
    concat(LIST, output_filename)

if __name__ == "__main__":
    # all_notes = get_notes_from_googleslide('11bF5Qfqnz0NGyJ3cCv4Lwtj48s5AyAjWG7J4T6QkbzU')
    # # all_notes = get_notes_from_googleslide('11bF5Qfqnz0NGyJ3cCv4Lwtj48s5AyAjWG7J4T6QkbzU', get_credentials())
    # for notes in all_notes:
    #     print(notes)
    parser = argparse.ArgumentParser(description='Create Audio')
    parser.add_argument('videodir', metavar='text', type=str, help='The directory having all videos')#, nargs=1)
    parser.add_argument('outputfilename', metavar='output', type=str, help='The file in which these merged video will be saved.')
    
    args = parser.parse_args()
    concat_all(args.videodir, args.outputfilename)

    # export_notes('11bF5Qfqnz0NGyJ3cCv4Lwtj48s5AyAjWG7J4T6QkbzU', 'notes-out')
