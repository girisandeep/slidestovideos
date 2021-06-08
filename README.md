## Install dependencies
pip install -r requirements.txt

To get started with slides credentials, 

* Please follow this https://developers.google.com/slides/quickstart/python
* Then run: python common.py
* And complete the sign in process

## Slides -> Notes
You can extract the notes from slides using this script:
    python extract_notes.py "presentation id" <folder>

This will generate notes in the folder one txt per file.

You can contatenate the notes using the following command:
    ./concat_notes.sh <folder containing txt files>

It generates all.txt having all text and a copy of it for backups.

## Screenshots
You can generate screenshots of a given google presentation using:
    python create_screen_shots.py <the slide id shown in url> <output folder> <number of slides>

It will open the google slide inside the webbrowser and then you can login and open the slides. Once you have open the slides, press enter on console.

The first argument is the presentation id that you see in the browser url of any google slide.

The second argument is the name of folder in which it is going to save the screenshots.

The last argument is optional. If you don't provide the last argument, it will probe the google presentation to find number of slides.


## Create Video
You can merge a screenshot with and audio file to create video using this python function:
    from create_videos import create_videos_dirs
    create_videos_dirs("audio_dir", "screenshots_dir", "output_videos");

It takes 1.mp3 from audio_dir and combines it with 1.jpg from screenshots_dir and saves it as 1.avi in output_videos. It does the same for all audio files. Note that it matches the name of image with the name of audio file.

# Merge Multiple videos
You can merge multiple videos to form a single video.
Here is the example command:
    python ../merge_videos.py videos multi_videos loadingxml:2-5 avro:6-9 datasources:10-14 hivetables:15-18 jdbc:19-21 dist_sql:22-25 

It assumes that the input videos are named using numbers. In the example above, it is merging videos located in multi_videos and saving the result in videos. It is going to merge 2.avi, 3. avi, 4.avi and 5.avi into loadingxml.avi. Similarly, it is going to merge 6.avi, 7.avi, 8.avi and 9.avi into avro.avi. And so on.

