Ubuntu AIM `Deep Learning OSS Nvidia Driver AMI GPU PyTorch 2.2.0 (Ubuntu 20.04) 20240521`


Custom TCP Rule  TCP  5000  0.0.0.0/0 


```
sudo apt update && sudo apt upgrade -y
sudo apt install python3-pip python3-venv -y 

python3 -m venv whisper_env
source whisper_env/bin/activate

sudo apt install ffmpeg
pip install git+https://github.com/openai/whisper.git
pip install fastapi uvicorn pydantic requests

uvicorn app:app --host 0.0.0.0 --port 5000
```