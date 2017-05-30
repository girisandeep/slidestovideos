from subprocess import call
import os
import argparse

def concat(lst, output):
    print "lst: " + lst
    print "output: " + output
    call(["ffmpeg","-y", "-loglevel", "quiet", "-f", "concat", "-safe", "0", "-i", lst, "-c", "copy", output])

# def concat_all(videos_dir, output_filename):
#     videos = os.listdir(videos_dir)
#     videos.sort();

#       LIST = "to_merge.lst"
#     with open(LIST, "w") as mylist:
#         for video in videos:
#             mylist.write("file " + videos_dir + "/" + video + "\n")
#     concat(LIST, output_filename)

def concat_multi(videos_dir, range_arr, output_dirname, output_filename, extn):
    #print "videos_dir: " + videos_dir
    #print "range_arr: " + str(range_arr)

    if not os.path.exists(output_dirname):
        os.mkdir(output_dirname)

    outputfile_fullname = output_dirname + "/" + output_filename + extn;
    print "outputfile_fullname: " + outputfile_fullname

    allvideos = os.listdir(videos_dir)
    allvideos.sort();

    to_be_merged = []
    
    LIST = output_filename + "_to_merge.lst"
    with open(LIST, "w") as mylist:
        for n in range_arr:
            mylist.write("file " + videos_dir + "/" + allvideos[n-1] + "\n")
    concat(LIST, outputfile_fullname)

def concat_multi_seq(videos_dir, seqs, output_dirname):
    for v in seqs:
        print v
        (name, nums) = v.split(':');
        range_arr = []
        for ranges in nums.split(','):
            if "-" in ranges:
                (st, end) = ranges.split("-")
                range_arr.extend(range(int(st), int(end)+1))
            else:
                range_arr.append(int(ranges))
        concat_multi(videos_dir, range_arr, output_dirname, name, ".mp4")
if __name__ == "__main__":
    # all_notes = get_notes_from_googleslide('11bF5Qfqnz0NGyJ3cCv4Lwtj48s5AyAjWG7J4T6QkbzU')
    # # all_notes = get_notes_from_googleslide('11bF5Qfqnz0NGyJ3cCv4Lwtj48s5AyAjWG7J4T6QkbzU', get_credentials())
    # for notes in all_notes:
    #     print(notes)
    parser = argparse.ArgumentParser(description='Create Audio')
    parser.add_argument('videodir', metavar='text', type=str, help='The directory having all videos')#, nargs=1)
    parser.add_argument('outputdirname', metavar='output', type=str, help='The directory in which these merged videos will be saved.')
    parser.add_argument('seq', metavar='Sequence', type=str, help='This should be in the form of Name:1-5,6', nargs='*')
    
    args = parser.parse_args()
    concat_multi_seq(args.videodir,args.seq, args.outputdirname)

    # export_notes('11bF5Qfqnz0NGyJ3cCv4Lwtj48s5AyAjWG7J4T6QkbzU', 'notes-out')
