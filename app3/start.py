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

URL = "WSS://api.assemblyai.com/v2/realtime/ws?sample_rate=16000"


async def send_resive():
    print("Connecting...")
    async with websockets.connect(
        URL,
        extra_headers=(("Authorization", API_KEY_ASSEMBLY),),
        ping_interval=5,
        ping_timeout=20
    ) as ws:
        await asyncio.sleep(0.1)
        print("Start session...")
        session_begins = await ws.resv()
        print(session_begins)

        async def send():
            while True:
                try:
                    data = stream.read(FRAMES_PER_BUFFER,
                                       exception_on_overflow=False)
                    data = base64.b64encode(data).decode("utf-8")
                    json_data = json.dumps({"audio_data": str(data)})
                    await ws.send(json_data)
                except websockets.exceptions.ConnectionClosedError as e:
                    print(e)
                    assert e.code == 4008
                    break
            return True

        async def recive():
            while True:
                try:
                    result_str = await ws.recv()
                    result = json.loads(result_str)
                    prompt = result["text"]
                    if prompt and result['message_type'] == 'FinalTranscript':
                        print("Human: ", prompt)
                        answer = ask(prompt)
                        print("AI: ", answer)

                except websockets.exceptions.ConnectionClosedError as e:
                    print(e)
                    assert e.code == 4008
                    break
        send_result, resive_result = await asyncio.gather(send(), recive())


asyncio.run(send_resive())
