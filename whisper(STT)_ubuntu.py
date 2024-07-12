from fastapi import FastAPI, File, UploadFile
import whisper
import requests
from pydantic import BaseModel

app = FastAPI()

# Whisper의 라지 모델 로드
model = whisper.load_model("large")

class TextResponse(BaseModel):
    text: str

@app.post("/transcribe/", response_model=TextResponse)
async def transcribe(file: UploadFile = File(...)):
    audio = await file.read()
    with open("temp.wav", "wb") as f:
        f.write(audio)
    result = model.transcribe("temp.wav", language="ko")  
    text = result["text"]


    response = requests.post("http://3.39.170.111:8000/bark/", json={"text": text})

    return TextResponse(text=text)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5000)