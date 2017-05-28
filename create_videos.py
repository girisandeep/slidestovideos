import os
from subprocess import call

def merge_audio_video(image, audio, output):
    call(["ffmpeg","-y","-loglevel", "quiet","-loop", "1", "-i", image, "-i", audio, "-c:v", "libx264", "-tune", "stillimage", "-c:a", "aac", "-b:a", "192k", "-pix_fmt", "yuv420p", "-shortest", output])


def create_videos_dirs(audio_dir, screenshot_dir, videos_dir):
    create_videos_files(audio_dir, os.listdir(audio_dir), screenshot_dir, os.listdir(screenshot_dir), videos_dir)

def get_file_name(f):
    return f.split(".")[0]

def are_equal(audio_files, screenshot_files):
    audio_names = map(get_file_name, audio_files)
    screenshot_names = map(get_file_name, screenshot_files)
    s1 = set(audio_names)
    s2 = set(screenshot_names)
    l1 = list(s1 - s2)
    l2 = list(s2 - s1)
    are_eq = True
    if len(l1) > 0:
        print("Following audios are extra: ")
        print(l1)
        are_eq = False
    if len(l2) > 0:
        print("Following screenshots are extra: ")
        print(l2)
        are_eq = False
    if are_eq:
        print "Both are equal"
    return are_eq

def to_dict(l):
    o = {}
    for e in l:
        o[get_file_name(e)] = e;
    return o

def create_videos_files(audio_dir, audio_files, screenshot_dir, screenshot_files, videos_dir):
    if os.path.exists(videos_dir):
        print "Output directory " + videos_dir + " exists. Please remove the directory."
    else:
        os.mkdir(videos_dir)
    if are_equal(audio_files, screenshot_files):
        print "Found eq"
        audio_dict = to_dict(audio_files)
        screenshot_dict = to_dict(screenshot_files)
        for ai in audio_dict:
            audio_file = audio_dict[ai]
            screenshot_file = screenshot_dict[ai]
            output = videos_dir + "/" + ai + ".mp4"
            
            print "Trying to create: " + output
            merge_audio_video(screenshot_dir + "/" + screenshot_file, audio_dir + "/" + audio_file, output)

if __name__ == "__main__":
    create_videos_dirs("audio", "screenshots", "videos");