import os
import subprocess
from multiprocessing import Pool
import numpy as np
from scipy.io.wavfile import read, write
import time

def split_text(text, num_chunks=3):
    words = text.split()
    chunk_size = len(words) // num_chunks
    chunks = [' '.join(words[i*chunk_size:(i+1)*chunk_size]) for i in range(num_chunks)]
    if len(words) % num_chunks != 0:
        chunks[-1] += ' ' + ' '.join(words[num_chunks*chunk_size:])
    return chunks

def process_chunk(args):
    script, input_file, output_file = args
    subprocess.run(["python", script, input_file, output_file])

if __name__ == '__main__':
    # Define the voice preset and text
    text = "글쎄, 기억에 남는 무대라… 무대 위에서 현실 도피하는 젊은 애들만 보였지. 폼 잡고, 소리 지르고, 땀 흘리면 그게 다 진심인 줄 아나? 삶이 그렇게 만만한 줄 아냐고. 진짜 땀 흘려야 할 때는 생각도 안 하고. 쯧."

    # Split the text into 3 chunks
    start_time = time.time()
    text_chunks = split_text(text, num_chunks=3)

    # Save each chunk to a separate file
    for i, chunk in enumerate(text_chunks):
        with open(f"text_chunk_{i+1}.txt", "w", encoding="utf-8") as file:
            file.write(chunk)

    # Prepare for parallel processing
    scripts = ["bark1.py", "bark2.py", "bark3.py"]
    input_files = [f"text_chunk_{i+1}.txt" for i in range(3)]
    output_files = [f"output_chunk_{i+1}.wav" for i in range(3)]

    # Use multiprocessing to process chunks in parallel
    with Pool(processes=3) as pool:
        args = [(scripts[i], input_files[i], output_files[i]) for i in range(3)]
        pool.map(process_chunk, args)

    # Concatenate the output audio files
    audio_arrays = []
    sample_rate = None

    for i in range(1, 4):
        sr, audio_array = read(f"output_chunk_{i}.wav")
        if sample_rate is None:
            sample_rate = sr
        audio_arrays.append(audio_array)

    final_audio = np.concatenate(audio_arrays)
    write("final_output.wav", sample_rate, final_audio)
    end_time = time.time()

    total_time = end_time - start_time
    print(f"Final audio saved as 'final_output.wav'")
    print(f"Total time taken: {total_time:.2f} seconds")
