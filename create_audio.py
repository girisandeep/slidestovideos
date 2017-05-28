from subprocess import call

def create_audio(text, filename):
    # call(["say", "-v","tom","-r","170", text, "-o", filename])
    call(["say", "-v","tom", text, "-o", filename])

###TODO:
# def create_audio_files(text_files, directory, prefix):
#     # call(["say", "-v","tom","-r","170", text, "-o", filename])
#     call(["say", "-v","tom", text, "-o", filename])

# def create_audio_dir(dir, filename):
#     # call(["say", "-v","tom","-r","170", text, "-o", filename])
#     call(["say", "-v","tom", text, "-o", filename])

if __name__ == "__main__":
    # all_notes = get_notes_from_googleslide('11bF5Qfqnz0NGyJ3cCv4Lwtj48s5AyAjWG7J4T6QkbzU')
    # # all_notes = get_notes_from_googleslide('11bF5Qfqnz0NGyJ3cCv4Lwtj48s5AyAjWG7J4T6QkbzU', get_credentials())
    # for notes in all_notes:
    #     print(notes)
    parser = argparse.ArgumentParser(description='Create Audio')
    parser.add_argument('text', metavar='text', type=str, help='The input Text')#, nargs=1)
    parser.add_argument('outputfilename', metavar='output', type=str, help='The file in which these audio will be saved.')
    
    args = parser.parse_args()

    create_audio(args.text, args.output)

    # export_notes('11bF5Qfqnz0NGyJ3cCv4Lwtj48s5AyAjWG7J4T6QkbzU', 'notes-out')
