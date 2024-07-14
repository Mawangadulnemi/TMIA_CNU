import argparse
import numpy as np
from rich import print
from bark_infinity import config

logger = config.logger
from bark_infinity import generation
from bark_infinity import api
from bark_infinity import text_processing
import os
import time
import random
import torch
from torch.utils import collect_env

text_prompts_in_this_file = []

try:
    text_prompts_in_this_file.append(
        f"It's {text_processing.current_date_time_in_words()} And if you're hearing this, Bark is working. But you didn't provide any text"
    )
except Exception as e:
    print(f"An error occurred: {e}")

text_prompt = """
    In the beginning the Universe was created. This has made a lot of people very angry and been widely regarded as a bad move. However, Bark is working.
"""
text_prompts_in_this_file.append(text_prompt)

text_prompt = """
    A common mistake that people make when trying to design something completely foolproof is to underestimate the ingenuity of complete fools.
"""
text_prompts_in_this_file.append(text_prompt)

def get_group_args(group_name, updated_args):
    updated_args_dict = vars(updated_args)
    group_args = {}
    for key, value in updated_args_dict.items():
        if key in dict(config.DEFAULTS[group_name]):
            group_args[key] = value
    return group_args

def main(args):
    if args.loglevel is not None:
        logger.setLevel(args.loglevel)

    if args.OFFLOAD_CPU is not None:
        generation.OFFLOAD_CPU = args.OFFLOAD_CPU
    else:
        if generation.get_SUNO_USE_DIRECTML() is not True:
            generation.OFFLOAD_CPU = True
    if args.USE_SMALL_MODELS is not None:
        generation.USE_SMALL_MODELS = args.USE_SMALL_MODELS
    if args.GLOBAL_ENABLE_MPS is not None:
        generation.GLOBAL_ENABLE_MPS = args.GLOBAL_ENABLE_MPS

    if not args.silent:
        if args.detailed_gpu_report or args.show_all_reports:
            print(api.startup_status_report(quick=False))
        elif not args.text_prompt and not args.prompt_file:
            print(api.startup_status_report(quick=True))
        if args.detailed_hugging_face_cache_report or args.show_all_reports:
            print(api.hugging_face_cache_report())
        if args.detailed_cuda_report or args.show_all_reports:
            print(api.cuda_status_report())
        if args.detailed_numpy_report:
            print(api.numpy_report())
        if args.run_numpy_benchmark or args.show_all_reports:
            from bark_infinity.debug import numpy_benchmark
            numpy_benchmark()

    if args.list_speakers:
        api.list_speakers()
        return

    if args.render_npz_samples:
        api.render_npz_samples()
        return

    if args.text_prompt:
        text_prompts_to_process = [args.text_prompt]
    elif args.prompt_file:
        text_file = text_processing.load_text(args.prompt_file)
        if text_file is None:
            logger.error(f"Error loading file: {args.prompt_file}")
            return
        text_prompts_to_process = text_processing.split_text(
            text_processing.load_text(args.prompt_file),
            args.split_input_into_separate_prompts_by,
            args.split_input_into_separate_prompts_by_value,
        )
        print(f"\nProcessing file: {args.prompt_file}")
        print(f"  Looks like: {len(text_prompts_to_process)} prompt(s)")
    else:
        print("No --text_prompt or --prompt_file specified, using test prompt.")
        text_prompts_to_process = random.sample(text_prompts_in_this_file, 2)

    things = len(text_prompts_to_process) + args.output_iterations
    if things > 10:
        if args.dry_run is False:
            print(f"WARNING: You are about to process {things} prompts. Consider using '--dry-run' to test things first.")

    print("Loading Bark models...")
    if not args.dry_run and generation.get_SUNO_USE_DIRECTML() is not True:
        generation.preload_models(
            args.text_use_gpu,
            args.text_use_small,
            args.coarse_use_gpu,
            args.coarse_use_small,
            args.fine_use_gpu,
            args.fine_use_small,
            args.codec_use_gpu,
            args.force_reload,
        )

    print("Done.")

    for idx, text_prompt in enumerate(text_prompts_to_process, start=1):
        if len(text_prompts_to_process) > 1:
            print(f"\nPrompt {idx}/{len(text_prompts_to_process)}:")

        for iteration in range(1, args.output_iterations + 1):
            if args.output_iterations > 1:
                print(f"\nIteration {iteration} of {args.output_iterations}.")
                if iteration == 1:
                    print("ss", text_prompt)

            args.current_iteration = iteration
            args.text_prompt = text_prompt
            args_dict = vars(args)

            api.generate_audio_long(**args_dict)

    output_dir = args.output_dir if args.output_dir else "bark_samples"
    expected_output_path = os.path.join(output_dir, "output.wav")

    # Check the actual generated file and rename it to expected output path
    for file in os.listdir(output_dir):
        if file.startswith("output.wav"):
            actual_output_path = os.path.join(output_dir, file)
            os.rename(actual_output_path, expected_output_path)
            print(f"Renamed {actual_output_path} to {expected_output_path}")
            break
    else:
        print(f"Expected file {expected_output_path} does not exist.")

if __name__ == "__main__":
    parser = config.create_argument_parser()
    args = parser.parse_args()
    updated_args = config.update_group_args_with_defaults(args)
    namespace_args = argparse.Namespace(**updated_args)
    main(namespace_args)
