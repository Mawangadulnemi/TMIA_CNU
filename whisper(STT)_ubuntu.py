from fastapi import FastAPI, File, UploadFile, HTTPException
from pydantic import BaseModel
import whisper
import os

app = FastAPI()

# Whisper 모델을 서버 시작 시 미리 로드합니다.
print("Loading Whisper model...")
model = whisper.load_model("large")
print("Whisper model loaded.")

class TextResponse(BaseModel):
    text: str

@app.post("/transcribe/", response_model=TextResponse)
async def transcribe(file: UploadFile = File(...)):
    file_location = "temp.wav"
    with open(file_location, "wb") as f:
        f.write(await file.read())
    
    # 이미 로드된 모델을 사용하여 변환을 수행합니다.
    result = model.transcribe(file_location, language="ko")
    text = result["text"]
    
    os.remove(file_location)  # 임시 파일 삭제
    
    return TextResponse(text=text)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5000)
