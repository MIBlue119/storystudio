import json
import os

import replicate
import requests

from storystudio.settings import app_settings
from storystudio.utils import log_io

os.environ["REPLICATE_API_TOKEN"] = app_settings.REPLICATE_API_TOKEN


def generate_music(music_prompt, output_path=None, duration=20, output_format="mp3"):
    # Call replicate music generation API
    # Currently, the model supports 3 versions: large, melody
    # stip the music prompt `\n`
    music_prompt = music_prompt.replace("\n", "")
    input_settings = {
        "model_version": "large",
        "prompt": music_prompt,
        "duration": duration,
        "output_format": output_format,
        "seed": -1,
    }
    output_url = replicate.run(
        "facebookresearch/musicgen:7a76a8258b23fae65c5a22debb8841d1d7e816b75c2f24218cd2bd8573787906",
        input=input_settings,
    )
    print(output_url)
    # Write the output to a file
    if output_path is None:
        output_path = "output" + "." + output_format

    response = requests.get(output_url)
    with open(output_path, "wb") as f:
        f.write(response.content)


@log_io
def generate_scene_music(music_prompt, output_dir):
    os.makedirs(output_dir, exist_ok=True)
    music_prompt = music_prompt["music_prompt"]
    for key in music_prompt:
        output_path = os.path.join(output_dir, f"{key}.mp3")
        generate_music(music_prompt[key], output_path, duration=30, output_format="mp3")


@log_io
def save_scene_music_prompt(music_prompt, output_dir):
    os.makedirs(output_dir, exist_ok=True)
    music_prompt = music_prompt["music_prompt"]
    # Export to json
    with open(os.path.join(output_dir, "music_prompt.json"), "w") as f:
        json.dump(music_prompt, f, indent=4)
