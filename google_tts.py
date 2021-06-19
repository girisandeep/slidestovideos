
# https://console.cloud.google.com/apis/dashboard?authuser=3&project=sonorous-sign-317010&supportedpurview=project&cloudshell=true

# My API Project
# sonorous-sign-317010
# 260903127911

# created key [b6338f3897e79ef2d42fa021dc6d2837999f4b2a] of type [json] as [/home/admin_/key.json] for [my-tts-sa@sonorous-sign-317010.iam.gserviceaccount.com
# pip3 install --user --upgrade google-cloud-texttospeech
# en-US-Standard-A

import google.cloud.texttospeech as tts
import argparse
from create_silent_audio import create_silent_audio
import os
import re

def unique_languages_from_voices(voices):
    language_set = set()
    for voice in voices:
        for language_code in voice.language_codes:
            language_set.add(language_code)
    return language_set

def list_languages():
    client = tts.TextToSpeechClient()
    response = client.list_voices()
    languages = unique_languages_from_voices(response.voices)
    print(f" Languages: {len(languages)} ".center(60, "-"))
    for i, language in enumerate(sorted(languages)):
        print(f"{language:>10}", end="\n" if i % 5 == 4 else "")

def list_voices(language_code=None):
    client = tts.TextToSpeechClient()
    response = client.list_voices(language_code=language_code)
    voices = sorted(response.voices, key=lambda voice: voice.name)
    print(f" Voices: {len(voices)} ".center(60, "-"))
    for voice in voices:
        languages = ", ".join(voice.language_codes)
        name = voice.name
        gender = tts.SsmlVoiceGender(voice.ssml_gender).name
        rate = voice.natural_sample_rate_hertz
        print(f"{languages:<8} | {name:<24} | {gender:<8} | {rate:,} Hz")

def text_to_wav(voice_name: str, text: str, filename):
    language_code = "-".join(voice_name.split("-")[:2])
    text_input = tts.SynthesisInput(text=text)
    voice_params = tts.VoiceSelectionParams(
        language_code=language_code, name=voice_name
    )
    audio_config = tts.AudioConfig(audio_encoding=tts.AudioEncoding.LINEAR16)
    client = tts.TextToSpeechClient()
    response = client.synthesize_speech(
        input=text_input, voice=voice_params, audio_config=audio_config
    )
    # filename = f"{voice_name}.wav"
    with open(filename, "wb") as out:
        out.write(response.audio_content)
        print(f'Generated speech saved to "{filename}"')

# txt = "On top of every node what you see is a ZX ID or zookeeper transaction ID. It is essentially a number that represents how new is the content in a particular node. The node which got the latest update would have the highest ZX ID. This ID keeps increasing as we update the content. Using this ID, we quickly identify which of the machines are left behind and which of the Machines have caught up with the leader. The leader would always be a node with highest ID. There might be other followers having same ZX ID as the leader."
# for lang in "en-US-Wavenet-A": #, "en-US-Wavenet-B", "en-US-Wavenet-C", "en-US-Wavenet-D", "en-US-Wavenet-E", "en-US-Wavenet-F", "en-US-Wavenet-G", "en-US-Wavenet-H", "en-US-Wavenet-I", "en-US-Wavenet-J", :
#     text_to_wav(lang, txt, "en-US-Wavenet-A.wav")

def getfiles(indir, pat, create=False):
    if not os.path.exists(indir):
        if not create:
            print("The %s directory does not exist" % indir)
            exit(1)
        else:
            print("Creating %s directory as it does not exist" % indir)
            os.makedirs(indir)
            return []
    if not os.path.isdir(indir):
        print("The %s is not a valid directory " % indir)
        exit(2)
    ret = []
    for fname in os.listdir(indir):
        if fname.startswith("."):
            continue
        res = re.match(pat, fname)
        if res:
            ret.append((res[1], res[1]))
    return ret

def create_audio_file(infile, outfile):
    with open(infile, "r") as f:
        txt = f.read().strip()
        if len(txt) == 0:
            create_silent_audio(1, outfile)
        else:
            text_to_wav("en-US-Wavenet-A", txt, outfile)
            print(outfile, ":", txt)

def create_audio_dir(indir, outdir):
    infiles = getfiles(indir, "(.+)\.(txt)")
    # print("infiles: ", infiles)
    if not infiles:
        return;
    infileset = set([f for f, _ in infiles])
    outfiles =  getfiles(outdir, "(.+)\.(wav)", True)
    outfilesset = set([f for f, _ in outfiles])
    left = sorted(infileset - outfilesset)
    
    print("Starting to create audio for: ", left)
    for f in left:
        create_audio_file(indir + "/" + f + ".txt", outdir + "/" + f + ".wav")
        print("Finished ", f)
    
# os.system("cloudshell download en-US-Standard-A.wav")
# os.system("cloudshell download en-US-Wavenet-A.wav")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Create Audio')
    parser.add_argument('indir', metavar='indir', type=str, help='The input directory.')#, nargs=1)
    parser.add_argument('outdir', metavar='output', type=str, help='The output directory.')
    args = parser.parse_args()
    create_audio_dir(args.indir, args.outdir)

    # Since transcription is going to be costly, we need to skip creating audio if it is already there.
    # Also, since in some cases the audio is manually recorded, we should avoid overwriting
    # The way it is going to be used is with the directories.
    # Check the output directory.
    # Check the input directory
    # Input - output files need to be re-recorded.
    # If the file is empty, consider the duration of slide to be 0.5s selience.
    # If the file starts with #x, consider x many millis for silence.
