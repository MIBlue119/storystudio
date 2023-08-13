import base64
import json
import os

import requests

from storystudio.settings import app_settings
from storystudio.utils import log_io

engine_id = "stable-diffusion-xl-1024-v1-0"
api_host = os.getenv("API_HOST", "https://api.stability.ai")
api_key = app_settings.STABILITY_KEY

if api_key is None:
    raise Exception("Missing Stability API key.")


def generate_image(image_prompt, output_path):
    negative_prompt_list = [
        "ugly",
        "blurry",
        "fused fingers",
        "worst quality",
        "too many fingers",
        "poorly drawn hands",
        "poorly drawn face",
        "body out of frame",
        "deformed",
        "mutated hands",
        "mutation",
        "missing arms",
        "missing hands",
        "extra fingers",
        "extra hands",
        "extra arms",
        "extra legs",
        "long neck",
        "poorly Rendered face",
        "poorly Rendered hands",
        "beginner",
        "watermark",
        "worst quality",
        "malformed limbs",
        "jpeg artifacts",
        "duplicate",
        "deformed body features",
        "distorted face",
        "fused eyes",
        "fused mouth",
        "fused nose",
        "poorly drawn eyes",
        "poorly drawn mouth",
        "poorly rendered eyes",
        "poorly rendered mouth",
    ]
    negative_prompt = ",".join(negative_prompt_list)
    response = requests.post(
        f"{api_host}/v1/generation/{engine_id}/text-to-image",
        headers={
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Authorization": f"Bearer {api_key}",
        },
        json={
            "text_prompts": [
                {"text": image_prompt, "weight": 1},
                # stable diffusion negative prompts: https://thenaturehero.com/stable-diffusion-negative-prompt-list/
                {"text": negative_prompt, "weight": -1},
            ],
            "cfg_scale": 7,
            "height": 1024,
            "width": 1024,
            "samples": 1,
            "steps": 30,
        },
    )

    if response.status_code != 200:
        raise Exception("Non-200 response: " + str(response.text))

    data = response.json()

    for i, image in enumerate(data["artifacts"]):
        with open(output_path, "wb") as f:
            f.write(base64.b64decode(image["base64"]))


@log_io
def generate_scene(scene_prompt, output_dir):
    os.makedirs(output_dir, exist_ok=True)
    scene_prompt = scene_prompt["scene_prompt"]
    for key in scene_prompt:
        output_path = os.path.join(output_dir, f"{key}.png")
        generate_image(scene_prompt[key], output_path)


@log_io
def save_scene_prompt(scene_prompt, output_dir):
    os.makedirs(output_dir, exist_ok=True)
    scene_prompt = scene_prompt["scene_prompt"]
    # Export to json
    with open(os.path.join(output_dir, "scene_prompt.json"), "w") as f:
        json.dump(scene_prompt, f, indent=4)
