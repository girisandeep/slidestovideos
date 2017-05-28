from subprocess import call 
import argparse

def create_silent_audio(seconds, outputfilename):
    print "Seconds: " + str(seconds)
    print "output: " + outputfilename
    #call(["ffmpeg", "-ar", "48000", "-t", str(seconds), "-f", "s16le", "-acodec", "pcm_s16le", "-ac", "2", "-i", "/dev/zero", "-acodec", "copy", outputfilename])
    call(["ffmpeg", "-ar", "48000", "-t", str(seconds), "-f", "s16le", "-acodec", "pcm_s16le", "-ac", "2", "-i", "/dev/zero", "-acodec", "libmp3lame", "-aq", "4", outputfilename])

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Create Audio')
    parser.add_argument('seconds', metavar='seconds', type=int, help='Silence duration in seconds')#, nargs=1)
    parser.add_argument('outputfilename', metavar='output', type=str, help='The file in which these audio will be saved. eg. x.wav')

    args = parser.parse_args()
    create_silent_audio(args.seconds, args.outputfilename)
    # export_notes('11bF5Qfqnz0NGyJ3cCv4Lwtj48s5AyAjWG7J4T6QkbzU', 'notes-out')

