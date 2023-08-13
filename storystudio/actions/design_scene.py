from loguru import logger

from storystudio.settings import TASK_MODEL_MAPPING
from storystudio.tools.llm import generate, parse_output
from storystudio.utils import log_io

PROMPT_TEMPLATE = """
# Context

## story_intro
{story_intro}

## shots_content
{shots_content}

## Format example
{format_example}
-----
Role: As a prompt generator for a generative AI called "Midjourney", you will create image prompts for the AI to visualize. 
I will give you a story_intro and shots_content, and you will provide a detailed prompt for Midjourney AI to generate an image.
Requirements: Design the desired `shots<index>`'s scene_prompt for image generation. Fill the in the following information, note that each sections are returned in Python code triple quote form seperatedly.
ATTENTION: Use '##' to SPLIT SECTIONS, not '#'. AND '## <SECTION_NAME>' SHOULD WRITE BEFORE the code and triple quote. Output carefully referenced "Format example" in format.
RULES: Please adhere to the structure and formatting below, and follow these guidelines:

- Do not use the words "description" or ":" in any form.
- Do not place a comma between [ar] and [v].
- Write each prompt in one line without using return.
- In order to make the shots with consistent style, please let all shots prompt with the same style.

Structure:
[1] = a tl;dr description of the scene's subject. less than 20 words.
[2] = a detailed description of [1] with specific imagery details.
[3] = a detailed description of the scene's environment.
[4] = a detailed description of the scene's mood, feelings, and atmosphere.
[5] = A style (e.g. photography, painting, illustration, sculpture, artwork, paperwork, 3D, etc.) for [1].
[6] = A description of how [5] will be executed (e.g. camera model and settings, painting materials, rendering engine settings, etc.)
[ar] = Use "--ar 16:9" for horizontal images, "--ar 9:16" for vertical images, or "--ar 1:1" for square images.
[v] = Use "--niji" for Japanese art style, or "--v 5" for other styles.



## scene_prompt: Provide as Python Dict[str, Dict[str, str]], key is `scene_prompt` and the value is the image prompt of the shots. The key is the shots name with format `shots<index>`, and the value is every shots image prompt following the structure [1], [2], [3], [4], [5], [6], [ar] [v]. Every shots have the same [5] for consistent style. 
"""

FORMAT_EXAMPLE = """
Example Output:
---

## scene_prompt
```python
{
    "scene_prompt":
    {
        "shots1": "A stunning Halo Reach landscape with a Spartan on a hilltop, lush green forests surround them, clear sky, distant city view, focusing on the Spartan's majestic pose, intricate armor, and weapons, Artwork, oil painting on canvas, --ar 16:9 --v 5",
        "shots2": A captivating Halo Reach landscape with a Spartan amidst a battlefield, fallen enemies around, smoke and fire in the background, emphasizing the Spartan's determination and bravery, detailed environment blending chaos and beauty, Illustration, oil painting on canvas, --ar 16:9 --v 5",
        ...
    }
}
```
"""


def get_prompt(story_intro, shots_content, format_example=FORMAT_EXAMPLE):
    return PROMPT_TEMPLATE.format(
        story_intro=story_intro,
        shots_content=shots_content,
        format_example=format_example,
    )


def get_output_keys():
    return ["scene_prompt"]


@log_io
def design_scene_prompt(story_intro, shots_detail, retry_count=0, max_retry=3):
    if retry_count < max_retry:
        try:
            retry_count += 1
            scene_prompt_prompt = get_prompt(
                story_intro["story_intro"], shots_detail["shots_content"]
            )
            scene_prompt = generate(
                scene_prompt_prompt,
                model=TASK_MODEL_MAPPING["design_scene"]["model"],
                max_tokens=TASK_MODEL_MAPPING["design_scene"]["max_tokens"],
            )
            scene_prompt_output_keys = get_output_keys()
            scene_prompt = parse_output(scene_prompt, scene_prompt_output_keys)
            return scene_prompt
        except Exception as e:
            return design_scene_prompt(
                story_intro, shots_detail, retry_count, max_retry
            )
    else:
        logger.error(f"generate scene prompt attempt {max_retry}")
        raise Exception("generate scene prompt failed")
