import requests

url = "http://3.39.170.111:7897/upload"
files = {
    'file': ('recording.wav', open('test.wav', 'rb')),
}
data = {
    'voice_model': 'weights/shinhaechul.pth',
    'transpose': '-8',
    'pitch_algorithm': 'rmvpe'
}

try:
    response = requests.post(url, files=files, data=data)
    response.raise_for_status()
    with open('processed.wav', 'wb') as f:
        f.write(response.content)
    print("File successfully processed and saved as processed.wav")
except requests.exceptions.RequestException as e:
    print("Request failed:", e)
