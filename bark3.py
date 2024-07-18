import sys
import torch
import numpy as np
from transformers import AutoProcessor, BarkModel
from scipy.io.wavfile import write

# Get input text file and output wav file from arguments
input_text_file = sys.argv[1]
output_wav_file = sys.argv[2]

# Read the text from the input file
with open(input_text_file, "r", encoding="utf-8") as file:
    text = file.read()

# Load processor and model
processor = AutoProcessor.from_pretrained("suno/bark")
model = BarkModel.from_pretrained("suno/bark")
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)

# Define the voice preset
voice_preset = "ko_speaker_4"

# Process the input text
inputs = processor(text, voice_preset=voice_preset)
inputs = {key: value.to(device) for key, value in inputs.items()}

# Generate audio
with torch.no_grad():
    audio_array = model.generate(**inputs)

# Move the output audio array back to the CPU and convert to numpy array
audio_array = audio_array.cpu().numpy().squeeze()

# Define the sample rate
sample_rate = model.generation_config.sample_rate

# Save the audio to a file
write(output_wav_file, sample_rate, audio_array)
print(f"Audio saved as '{output_wav_file}'")
