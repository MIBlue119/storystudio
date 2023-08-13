from loguru import logger

from storystudio.settings import TASK_MODEL_MAPPING
from storystudio.tools.llm import generate, parse_output
from storystudio.utils import log_io

PROMPT_TEMPLATE = """
# Context

## story_intro
{story_intro}

## character_descripts
{character_descripts}

## shots_tldr
{shots_tldr}

## Format example
{format_example}
-----
Role: You are a professional and creative storyteller; the goal is to design compelling, impressive and touching story.
Requirements: According to the story_intro/character_descripts and shots_tldr,  design the desired `shots<index>`'s detail description. Fill the in the following information, note that each sections are returned in Python code triple quote form seperatedly.
ATTENTION: Use '##' to SPLIT SECTIONS, not '#'. AND '## <SECTION_NAME>' SHOULD WRITE BEFORE the code and triple quote. Output carefully referenced "Format example" in format.
RULES: Please don't use any value already at the Example Output of the ## Format example.

## shots_content: Provide as Python Dict[str, Dict[str, str]], key is `shots_content` and the value is the detail studio of the shots. The key is the shots name with format `shots<index>`, and the value is the story detail of the shots. Please use the `story_intro`/`character_descripts` and `shots_tldr` to design the story detail of the shots.
"""


FORMAT_EXAMPLE = """
Example Output:
---

## shots_content
```python
{
    "shots_content":
    {
        "shots1": {
            "detail_script": "The front of a summer evening with continuous rain just passed Good Hill, and the air is clear with no PM2.5. An active Pikachu rushes to Good Hill from afar because Good Hill is the best spot to view the beautiful summer sunset. It finally reaches the top of the hill, panting and muttering, 'Pika, PikaPikaPika' // Translation: 'Looks like, I need to lose weight."
        },
        "shots2": {
            "detail_script": "At this time the sun is still at an angle of 40 degrees, still dazzling white-yellow. Pikachu seems to have arrived a bit early, so it lies down on the fluffy grass to sunbathe. The wind on Good Hill is always gentle to the visitors, unlike other high places. Pikachu enjoys the gentle breeze and drifts into a half-awake state. 'Sua SuaSuaSua Sua SuaSuaSua' seems to have a visitor approaching. The visitor speaks: 'PikaPika' // Translation: 'Hello there.' It seems to be of the same species as Pikachu, so Pikachu wakes up to see. Indeed, the visitor looks like him but with smaller eyes and a big smile. The visitor introduces herself as PikaQiu, and Pikachu welcomes her to lie down and wait for the evening glow together."
        },
        "shots3": {
            "detail_script": "But there's still some time before the evening..."
        }
        ,
        "shots4": {
            "detail_script": "When PikaQiu wonders what to do, Pikachu speaks: 'You also look good in purple.' ..."
        }
    }
}
```
---
"""


def get_prompt(
    story_intro, character_descripts, shots_tldr, format_example=FORMAT_EXAMPLE
):
    return PROMPT_TEMPLATE.format(
        story_intro=story_intro,
        character_descripts=character_descripts,
        shots_tldr=shots_tldr,
        format_example=format_example,
    )


def get_output_keys():
    return ["shots_content"]


@log_io
def generate_shots_detail(
    story_intro, character_descripts, shots_tldr, retry_count=0, max_retry=3
):
    if retry_count < max_retry:
        try:
            retry_count += 1
            shots_detail_prompt = get_prompt(
                story_intro["story_intro"],
                character_descripts,
                shots_tldr["shots_tldr"],
            )
            shots_detail = generate(
                shots_detail_prompt,
                model=TASK_MODEL_MAPPING["write_shots_detail"]["model"],
                max_tokens=TASK_MODEL_MAPPING["write_shots_detail"]["max_tokens"],
            )
            shots_detail_output_keys = get_output_keys()
            shots_detail = parse_output(shots_detail, shots_detail_output_keys)
            return shots_detail
        except Exception as e:
            return generate_shots_detail(
                story_intro, character_descripts, shots_tldr, retry_count, max_retry
            )
    else:
        logger.error(f"generate shots detail attempt {max_retry}")
        raise Exception("generate shots detail failed")
