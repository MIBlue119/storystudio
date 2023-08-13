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

## Format example
{format_example}
-----
Role: You are a professional and creative storyteller; the goal is to design compelling, impressive and touching story.
Requirements: According to the story_intro and character_descripts, design the shots of the total story and write their tl;dr. Use the story to fill the in the following information, note that each sections are returned in Python code triple quote form seperatedly.
ATTENTION: Use '##' to SPLIT SECTIONS, not '#'. AND '## <SECTION_NAME>' SHOULD WRITE BEFORE the code and triple quote. Output carefully referenced "Format example" in format.
RULES: Please don't use any value already at the Example Output of the ## Format example.

## shots_tldr: Provide as Python Dict[str, Dict[str, str]], key is `shots_tldr` and the value is the tl;dr of the shots. The key is the shots name with format `shots<index>`, and the value is the tl;dr of the shots.
"""

FORMAT_EXAMPLE = """
Example Output:
---

## shots_tldr
```python
{
    "shots_tldr":
    {
        "shots1": "On a summer evening after a frontal rain, Pikachu, exerting all his strength, runs up Good Hill to wait for the summer evening glow.",
        "shots2": "Before the evening glow arrives, Pikachu falls asleep in the wind-blown grass. A visitor who looks like him, named PikaQiu, arrives.",
        "shots3": "They chat about everything. When the sunset comes, all disguises are removed, and PikaQiu transforms back into the Ditto form that it doesn't like.",
        "shots4": "PikaQiu worries that Pikachu might not like Ditto's appearance, but Pikachu says he likes it. PikaQiu then tells Pikachu its real name, 'Ditto'."
    }
}
```
---
"""


def get_prompt(story_intro, character_descripts, format_example=FORMAT_EXAMPLE):
    return PROMPT_TEMPLATE.format(
        story_intro=story_intro,
        character_descripts=character_descripts,
        format_example=format_example,
    )


def get_output_keys():
    return ["shots_tldr"]


@log_io
def generate_shots_tldr(story_intro, character_descripts, retry_count=0, max_retry=3):
    if retry_count < max_retry:
        try:
            retry_count += 1
            shots_tldr_prompt = get_prompt(
                story_intro["story_intro"], character_descripts
            )
            shots_tldr = generate(
                shots_tldr_prompt,
                model=TASK_MODEL_MAPPING["write_shots_tldr"]["model"],
                max_tokens=TASK_MODEL_MAPPING["write_shots_tldr"]["max_tokens"],
            )
            shots_tldr_output_keys = get_output_keys()
            shots_tldr = parse_output(shots_tldr, shots_tldr_output_keys)
            return shots_tldr
        except Exception as e:
            return generate_shots_tldr(
                story_intro, character_descripts, retry_count, max_retry
            )
    else:
        logger.error(f"generate shots tldr attempt {max_retry}")
        raise Exception("generate shots tldr failed")
