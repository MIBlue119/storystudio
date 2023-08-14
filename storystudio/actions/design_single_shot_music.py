from loguru import logger

from storystudio.settings import TASK_MODEL_MAPPING
from storystudio.tools.llm import generate, parse_output
from storystudio.utils import log_io

PROMPT_TEMPLATE = """
Role: You are a music designer and In-depth knowledge of the field of music and soundtracks. I will give you a shots_content_detail. please according to the shots_content_detail to generate music prompt, please export the prompt follow ```python <MAIN_MUSIC_STYLE>, <AGE_OF_THE_MUSIC>, <BPM>, <MUSIC_INSTRUMENTS> ```structures.
This music prompt will be used for music generation, please use your professional music vocabulary to accurately/lifelikely describe the soundtrack of this story.
ATTENTION: Output carefully referenced "Format example" in format.
RULES: 
- Please don't use any value already at the Examples.
- Please adhere to the structure and formatting below, and follow these guidelines.
- Do not use the words "description" or ":" in any form.
- Write each prompt in one line without using return.
- Please don't use the music prompt already at the Example Output of the ## Format example
- Your response must start with code block '```pythons' and ended with '```'
- Don't explain and only return the response.

Structures
<MAIN_MUSIC_STYLE> = use one sentence under 30 words to describe the music style appropriated for the story.
<AGE_OF_THE_MUSIC> = specify the music's age, maybe 1990/1980/1960/2000 or 18th/15th
<BPM> = the bpm of the music.
<MUSIC_INSTRUMENTS> = possible music instruments. Up to 5 instruments.
-------
Your response must start with code block '```pythons' and ended with '```'. 
-----
## Example1
###Input
```
Harry bids farewell to Naruto and his friends, promising to remember them always. He is transported back to his own world, where he is greeted by Hermione and Ron. As he tells them about his adventures in the Naruto world, he can't help but smile, grateful for the friendships he has made and the experiences he has had.
```
###Response
```python
A harmonious blend of melancholic British magic undertones with vibrant Ninja-inspired crescendos, 2023, a tempo of 88 bpm, instruments such as violins, flutes, shinobue, koto, and shamisen.
```
-----
## Example2
###Input
```
The front of a summer evening with continuous rain just passed Good Hill, and the air is clear with no PM2.5. An active Pikachu rushes to Good Hill from afar because Good Hill is the best spot to view the beautiful summer sunset. It finally reaches the top of the hill, panting and muttering, 'Pika, PikaPikaPika' // Translation: 'Looks like, I need to lose weight.
```
###Response
```python
A vibrant mix of cheerful Pokemon tunes with soothing summer evening vibes, 2023, a rhythm of 80 bpm, instruments such as acoustic guitar, pan flute, tambourine, triangle, and marimba.
```
-----
### Input
```
{shots_content_detail}
```
###Response
"""


def get_prompt(
    shots_content_detail,
):
    return PROMPT_TEMPLATE.format(shots_content_detail=shots_content_detail)


@log_io
def design_single_shot_music_prompt(shots_content_detail, retry_count=0, max_retry=3):
    if retry_count < max_retry:
        try:
            retry_count += 1
            prompt = get_prompt(shots_content_detail)
            logger.info(f"Debug: single shots music prompt for LLM={prompt}")
            response = generate(
                prompt,
                model=TASK_MODEL_MAPPING["design_single_shot_music"]["model"],
                max_tokens=TASK_MODEL_MAPPING["design_single_shot_music"]["max_tokens"],
            )

            single_shot_music_prompt = (
                response.strip("\n").strip(" ").replace("```", "").strip("python")
            )
            return single_shot_music_prompt
        except Exception as e:
            return design_single_shot_music_prompt(
                shots_content_detail, retry_count, max_retry
            )
    else:
        logger.error(f"generate single shot music prompt attempt {max_retry}")
        raise Exception("generate single shot music prompt failed")
