import requests
import time
from lib.secret import API_KEY

upload_endpoint = 'https://api.assemblyai.com/v2/upload'
transcript_endpoint = 'https://api.assemblyai.com/v2/transcript'

header_auth_only = {'authorization': API_KEY}

headers = {
    'authorization': API_KEY,
    'Content-type': "application/json"
}

CHUNK_SIZE = 2_242_880


def upload(filename):
    def read_file(filename):
        with open(filename, 'rb') as f:
            while True:
                data = f.read(CHUNK_SIZE)
                if not data:
                    break
                yield data

    upload_response = requests.post(
        upload_endpoint, headers=header_auth_only, data=read_file(filename))
    return upload_response.json()['upload_url']


def transcribe(audio_url):
    transcribe_request = {
        "audio_url": audio_url
    }
    transcribe_response = requests.post(
        transcript_endpoint, json=transcribe_request, headers=headers)
    return transcribe_response.json()['id']


def poll(transcript_id):
    polling_endpoint = transcript_endpoint + '/' + (transcript_id)
    polling_response = requests.get(polling_endpoint, headers=headers)
    return polling_response.json()


def get_transcription_result_url(url):
    transcribe_id = transcribe(url)
    while True:
        data = poll(transcribe_id)
        if data['status'] == 'completed':
            return data, None
        elif data['status'] == "error":
            return data, None
        print("Wait 10 sec.")
        time.sleep(10)


def save_transcript(url, title):
    data, error = get_transcription_result_url(url)

    if data:
        filename = title + '.txt'
        with open(filename, 'w') as f:
            f.write(data['text'])
        print('Transcript saved')
    elif error:
        print("Error!!!", error)
