import requests
import shutil

# EC2에 있는 Bark TTS 서버의 URL
BARK_TTS_URL = "http://3.39.170.111:8000/generate_audio"

def generate_tts(text):
    try:
        # Bark TTS 서버에 텍스트를 전송
        response = requests.post(BARK_TTS_URL, json={"text": text})
        response.raise_for_status()
        result = response.json()
        
        # 생성된 오디오 파일을 다운로드
        audio_file_path = result["audio_file"]
        audio_response = requests.get(f"http://3.39.170.111:8000/{audio_file_path}", stream=True)
        if audio_response.status_code == 200:
            with open("output.wav", "wb") as f:
                shutil.copyfileobj(audio_response.raw, f)
            print("Audio file downloaded successfully.")
            return {"message": "TTS generated successfully.", "audio_file": "output.wav"}
        else:
            print("Failed to download audio file.")
            return {"message": "Failed to download audio file"}

    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return {"message": f"Error generating TTS: {e}"}

if __name__ == "__main__":
    text = "로라님 오늘도 좋은 플리 감사합니다! 헉 1번째 댓글인가요? 뜨기 전에 고정 부탁드려요!"
    result = generate_tts(text)
    print(result)
