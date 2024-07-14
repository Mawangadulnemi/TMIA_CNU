from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import subprocess
import os
from fastapi.responses import FileResponse
import logging
import shutil

logging.basicConfig(level=logging.INFO)

app = FastAPI()

class TextRequest(BaseModel):
    text: str

def clear_folder(folder_path):
    if os.path.exists(folder_path):
        for file in os.listdir(folder_path):
            file_path = os.path.join(folder_path, file)
            try:
                if os.path.isfile(file_path):
                    os.unlink(file_path)
                    logging.info(f"Deleted file: {file_path}")
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
                    logging.info(f"Deleted directory: {file_path}")
            except Exception as e:
                logging.error(f"Failed to delete {file_path}. Reason: {e}")

@app.post("/generate_audio")
async def generate_audio(request: TextRequest):
    try:
        # samples 폴더 정리
        clear_folder("bark_samples")
        
        text = request.text
        # 환경 변수 설정
        env = os.environ.copy()
        env["PYTHONIOENCODING"] = "utf-8"

        # Bark TTS를 실행하여 텍스트를 음성으로 변환합니다.
        command = [
            "python", "bark_perform.py",
            "--text_prompt", text,
            "--history_prompt", "bark/assets/prompts/ko_speaker_4.npz",
            "--split_input_into_separate_prompts_by", "sentence",
            "--split_input_into_separate_prompts_by_value", "25",
            "--always_save_speaker", "True",
            "--output_dir", "bark_samples",
            "--output_format", "wav",
            "--output_filename", "output.wav",
            "--text_use_gpu", "True",
            "--coarse_use_gpu", "True",
            "--fine_use_gpu", "True",
            "--codec_use_gpu", "True",
            "--split_character_goal_length", "90",
            "--split_character_max_length", "130"
        ]

        logging.info(f"Running command: {' '.join(command)}")
        result = subprocess.run(command, capture_output=True, text=True, env=env, encoding='utf-8', errors='replace')
        
        if result.returncode != 0:
            # 실행 실패 시 에러 메시지를 로깅합니다.
            logging.error(f"Bark TTS generation failed: {result.stderr}")
            raise HTTPException(status_code=500, detail=f"Bark TTS generation failed: {result.stderr}")

        # 고정된 오디오 파일 경로
        audio_file_path = os.path.join("bark_samples", "output.wav")
        logging.info(f"Looking for audio file at: {audio_file_path}")

        if not os.path.exists(audio_file_path):
            logging.error("Audio file not found")
            logging.error(f"Subprocess stderr: {result.stderr}")
            logging.error(f"Subprocess stdout: {result.stdout}")
            raise HTTPException(status_code=404, detail="Audio file not found")
        
        # 임시 파일에 오디오 데이터를 복사하여 인코딩 문제 해결
        temp_file_path = "bark_samples/temp_output.wav"
        with open(audio_file_path, 'rb') as input_file, open(temp_file_path, 'wb') as output_file:
            shutil.copyfileobj(input_file, output_file)
        
        logging.info(f"Audio file generated and copied to: {temp_file_path}")
        logging.info(f"Original audio file path: {audio_file_path}")
        logging.info(f"Temporary audio file path: {temp_file_path}")

        return {"message": "TTS generated successfully.", "audio_file": temp_file_path}

    except Exception as e:
        logging.error(f"Error generating TTS: {e}")
        raise HTTPException(status_code=500, detail=f"Error generating TTS: {e}")

@app.get("/bark_samples/{filename:path}")
async def get_audio_file(filename: str):
    file_path = os.path.join("bark_samples", filename)
    logging.info(f"File path requested: {file_path}")
    if os.path.exists(file_path):
        logging.info(f"File found: {file_path}")
        return FileResponse(file_path)
    else:
        logging.error("File not found")
        raise HTTPException(status_code=404, detail="File not found")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
