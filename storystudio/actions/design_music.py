from loguru import logger

from storystudio.settings import TASK_MODEL_MAPPING
from storystudio.tools.llm import generate, parse_output
from storystudio.utils import log_io

PROMPT_TEMPLATE = """
# Context

## shots_content
{shots_content}

## Format example
{format_example}
-----
Role: You are a music designer and In-depth knowledge of the field of music and soundtracks. I will give you a shots_content. please according to the shots_content to generate music prompt, please export the prompt follow [1], [2], [3], [4] structures.
Requirements: Design the desired `shots<index>`'s music_prompt for music generation. Fill the in the following information, note that each sections are returned in Python code triple quote form seperatedly.
ATTENTION: Use '##' to SPLIT SECTIONS, not '#'. AND '## <SECTION_NAME>' SHOULD WRITE BEFORE the code and triple quote. Output carefully referenced "Format example" in format.
RULES: Please adhere to the structure and formatting below, and follow these guidelines:

- Do not use the words "description" or ":" in any form.
- Write each prompt in one line without using return.
- Please don't use the music prompt already at the Example Output of the ## Format example

Structures
[1] = main music style of the music, use one sentence under 15 words to describe the music style.
[2] = specify the year of the style of the music
[3] = the bpm of the music
[4] = possible music instruments

## music_prompt: Provide as Python Dict[str, Dict[str, str]], key is `music_prompt` and the value is the music prompt of the shots. The key is the shots name with format `shots<index>`, and the value is every shots music prompt following the structure [1], [2], [3], [4].
"""

FORMAT_EXAMPLE = """
Example Output:
---

## music_prompt
```python
{
   "music_prompt": {
    "shots1": "An enchanting orchestral piece blending elements of Western magical music and Japanese ninja-inspired tunes, 2019, a tempo of 90 bpm , instruments like violins, flutes, taiko drums, koto, shamisen, choir, and chimes",
    "shots2": "A futuristic electronic, 1990, a tempo of 120 bpm, using instruments like synthesizers drum machines  and vocoders",
    ...
    }
}
```
"""


def get_prompt(shots_content, format_example=FORMAT_EXAMPLE):
    return PROMPT_TEMPLATE.format(
        shots_content=shots_content, format_example=format_example
    )


def get_output_keys():
    return ["music_prompt"]


@log_io
def design_music_prompt(shots_detail, retry_count=0, max_retry=3):
    if retry_count < max_retry:
        try:
            retry_count += 1
            music_prompt_prompt = get_prompt(shots_detail["shots_content"])
            logger.info(f"Debug: music_prompt_prompt={music_prompt_prompt}")
            response = generate(
                music_prompt_prompt,
                model=TASK_MODEL_MAPPING["design_music"]["model"],
                max_tokens=TASK_MODEL_MAPPING["design_music"]["max_tokens"],
            )
            music_prompt_output_keys = get_output_keys()
            music_prompt = parse_output(response, music_prompt_output_keys)
            return music_prompt
        except Exception as e:
            return design_music_prompt(shots_detail, retry_count, max_retry)
    else:
        logger.error(f"generate scene prompt attempt {max_retry}")
        raise Exception("generate scene prompt failed")
