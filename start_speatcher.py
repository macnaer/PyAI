from lib.spetcher import *

filename = "output.wav"
audio_url = upload(filename)
save_transcript(audio_url, 'file_title')
