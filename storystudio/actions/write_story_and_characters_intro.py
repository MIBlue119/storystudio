from loguru import logger

from storystudio.settings import TASK_MODEL_MAPPING
from storystudio.tools.llm import generate, parse_output
from storystudio.utils import log_io

PROMPT_TEMPLATE = """
# Context

## Seed Story
{seed_story}

## Format example
{format_example}
-----
Role: You are a professional and creative storyteller; the goal is to design compelling, impressive,and touching story.
Requirements: If the ## Seed Story is not empty, according to it to write a story. If the ## Seed Story is 'None', ideate a whole new story from your own creativity. And return the result with following format, note that each sections are returned in Python code triple quote form seperatedly.
ATTENTION: Use '##' to SPLIT SECTIONS, not '#'. AND '## <SECTION_NAME>' SHOULD WRITE BEFORE the code and triple quote. Output carefully referenced "Format example" in format.
RULES: Please don't use any value already at the Example Output ## Format example.

## story_intro: Provide as Python dict[str, str], key is `story_intro` and the value is the tl;dr of the story.
## total_characters: Provide as Python dict[str, list[str]], key is `total_characters`, and the value is up to 5 characters appeared in the story. Please according to the story to think possible characters.
## character_descripts: Provide as Python dict[str, dict[str, str]], key is `character_descripts` and the value is the description of each character, the key is the character name, and the value is the description(personality/appearance /preferences) of the character.
"""

FORMAT_EXAMPLE = """
Example Output:
---

## story_intro
```python
{
    "story_intro": "Pikachu meets a new friend, Ditto, on the Good Hill during a summer evening."
}
```

## total_characters
```python
{
    "total_characters": ["Pikachu", "Ditto"]
}
```

## character_descripts
```python
{
    "character_descripts":{
        "Pikachu": "Mischievous and adventurous, Pikachu loves to eat Big Malasada chocolate.",
        "Ditto": "Shy and lacks confidence in its original appearance."
    }
}
---
"""


def get_prompt(seed_story, format_example=FORMAT_EXAMPLE):
    return PROMPT_TEMPLATE.format(seed_story=seed_story, format_example=format_example)


def get_output_keys():
    return ["story_intro", "total_characters", "character_descripts"]


@log_io
def generate_story_intro(seed_story, retry_count=0, max_retry=3):
    if retry_count < max_retry:
        try:
            retry_count += 1
            story_intro_prompt = get_prompt(seed_story)
            story_intro = generate(
                story_intro_prompt,
                model=TASK_MODEL_MAPPING["write_story_and_characters_intro"]["model"],
                max_tokens=TASK_MODEL_MAPPING["write_story_and_characters_intro"][
                    "max_tokens"
                ],
            )
            story_intro_output_keys = get_output_keys()
            story_intro = parse_output(story_intro, story_intro_output_keys)
            return story_intro
        except Exception as e:
            return generate_story_intro(seed_story, retry_count, max_retry)
    else:
        logger.error(f"generate story intro attempt {max_retry}")
        raise Exception("generate story intro failed")
