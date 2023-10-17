import pyaudio
import websockets
import asyncio
import base64
import json
from openai import ask
from api_secret import API_KEY_ASSEMBLY

FRAMES_PER_BUFFER = 3200
FORMAT = pyaudio.paInt16
CHANNEL = 1
RATE = 16000

p = pyaudio.PyAudio()

stream = p.open(
    format=FORMAT,
    channels=CHANNEL,
    input=True,
    frames_per_buffer=FRAMES_PER_BUFFER,
    rate=RATE
)

print(p.get_default_input_device_info())
