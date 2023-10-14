from lib.spetcher import *

filename = "output.wav"
audio_url = upload(filename)
save_transcription(audio_url, 'file_title')
