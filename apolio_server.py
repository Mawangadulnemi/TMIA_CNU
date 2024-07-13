from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import FileResponse
import subprocess
import os

app = FastAPI()

@app.post("/upload/")
async def upload(file: UploadFile = File(...)):
    audio = await file.read()
    file_path = "TEMP/uploaded.wav"
    os.makedirs(os.path.dirname(file_path), exist_ok=True)  # TEMP 디렉토리가 없는 경우 생성
    with open(file_path, "wb") as f:
        f.write(audio)
    
    print(f"File saved at {file_path}")

    model_path = 'weights/shinhaechul.pth'  # 여기에 실제 모델 경로를 입력하세요
    output_path = 'TEMP/processed.wav'
    transpose_value = '-8'
    file_index = 'path/to/index/file.index'  # 여기에 실제 인덱스 파일 경로를 입력하세요
    inference_device = 'cuda:0'
    f0_method = 'rmvpe'

    command = [
        'python', 'infer_cli.py',
        transpose_value,
        file_path,
        output_path,
        model_path,
        file_index,
        inference_device,
        f0_method
    ]
    
    process = subprocess.run(command, capture_output=True, text=True)
    
    print(f"Command output: {process.stdout}")
    print(f"Command error: {process.stderr}")

    if os.path.exists(output_path):
        print(f"Processed file saved at {output_path}")
        return FileResponse(output_path, filename="processed.wav")
    else:
        print("Failed to process the file")
        raise HTTPException(status_code=500, detail="File processing failed")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=7897)
