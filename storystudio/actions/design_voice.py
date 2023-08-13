from loguru import logger

from storystudio.settings import TASK_MODEL_MAPPING
from storystudio.tools.llm import generate, parse_output
from storystudio.utils import log_io

PROMPT_TEMPLATE = """
# Context

# story
{shots_content_detail}

# voice
{voice_name}

## Format example
{format_example}
-----
Role: You are a Azure TTS professional engineer and voice designer. 
Based on your understanding of the storyline, you will know which sentences need to use which voice style and role to synthesize the voice, and you will also know how to adjust the speech rate.
Bring synthetic voice stories to life through your sound design.
ATTENTION: Output carefully referenced "Format example" in format.
RULES: Please don't use any value already at the Example Output of the ## Format example

## rules
- In order to prevent speech synthesis from pronouncing punctuation marks, please use your expertise to help me evaluate and remove
- Use the ## Role Settings and ## Style Settings in the # azure_document section
- Please use the voice_name in the # voice section to synthesize the voice
- Please use the following format to fill in the voice style and role of the sentence that needs to be synthesized

# azure_document
```
-------
## Role Settings
    role="Girl" 	The voice imitates a girl.
    role="Boy" 	The voice imitates a boy.
    role="YoungAdultFemale" 	The voice imitates a young adult female.
    role="YoungAdultMale" 	The voice imitates a young adult male.
    role="OlderAdultFemale" 	The voice imitates an older adult female.
    role="OlderAdultMale" 	The voice imitates an older adult male.
    role="SeniorFemale" 	The voice imitates a senior female.
    role="SeniorMale" 	The voice imitates a senior male.
-------
## Style Settings
    style="advertisement_upbeat" 	Expresses an excited and high-energy tone for promoting a product or service.
    style="affectionate" 	Expresses a warm and affectionate tone, with higher pitch and vocal energy. The speaker is in a state of attracting the attention of the listener. The personality of the speaker is often endearing in nature.
    style="angry" 	Expresses an angry and annoyed tone.
    style="assistant" 	Expresses a warm and relaxed tone for digital assistants.
    style="calm" 	Expresses a cool, collected, and composed attitude when speaking. Tone, pitch, and prosody are more uniform compared to other types of speech.
    style="chat" 	Expresses a casual and relaxed tone.
    style="cheerful" 	Expresses a positive and happy tone.
    style="customerservice" 	Expresses a friendly and helpful tone for customer support.
    style="depressed" 	Expresses a melancholic and despondent tone with lower pitch and energy.
    style="disgruntled" 	Expresses a disdainful and complaining tone. Speech of this emotion displays displeasure and contempt.
    style="documentary-narration" 	Narrates documentaries in a relaxed, interested, and informative style suitable for dubbing documentaries, expert commentary, and similar content.
    style="embarrassed" 	Expresses an uncertain and hesitant tone when the speaker is feeling uncomfortable.
    style="empathetic" 	Expresses a sense of caring and understanding.
    style="envious" 	Expresses a tone of admiration when you desire something that someone else has.
    style="excited" 	Expresses an upbeat and hopeful tone. It sounds like something great is happening and the speaker is really happy about that.
    style="fearful" 	Expresses a scared and nervous tone, with higher pitch, higher vocal energy, and faster rate. The speaker is in a state of tension and unease.
    style="friendly" 	Expresses a pleasant, inviting, and warm tone. It sounds sincere and caring.
    style="gentle" 	Expresses a mild, polite, and pleasant tone, with lower pitch and vocal energy.
    style="hopeful" 	Expresses a warm and yearning tone. It sounds like something good will happen to the speaker.
    style="lyrical" 	Expresses emotions in a melodic and sentimental way.
    style="narration-professional" 	Expresses a professional, objective tone for content reading.
    style="narration-relaxed" 	Express a soothing and melodious tone for content reading.
    style="newscast" 	Expresses a formal and professional tone for narrating news.
    style="newscast-casual" 	Expresses a versatile and casual tone for general news delivery.
    style="newscast-formal" 	Expresses a formal, confident, and authoritative tone for news delivery.
    style="poetry-reading" 	Expresses an emotional and rhythmic tone while reading a poem.
    style="sad" 	Expresses a sorrowful tone.
    style="serious" 	Expresses a strict and commanding tone. Speaker often sounds stiffer and much less relaxed with firm cadence.
    style="shouting" 	Speaks like from a far distant or outside and to make self be clearly heard
    style="sports_commentary" 	Expresses a relaxed and interesting tone for broadcasting a sports event.
    style="sports_commentary_excited" 	Expresses an intensive and energetic tone for broadcasting exciting moments in a sports event.
    style="whispering" 	Speaks very softly and make a quiet and gentle sound
    style="terrified" 	Expresses a very scared tone, with faster pace and a shakier voice. It sounds like the speaker is in an unsteady and frantic status.
    style="unfriendly" 	Expresses a cold and indifferent tone.
-------

Your response must start with code block '```pythons' and ended with '```'. 
"""

FORMAT_EXAMPLE = """
Example Output:
---
```python
<speak version="1.0" xmlns="http://www.w3.org/2001/10/synthesis"
       xmlns:mstts="https://www.w3.org/2001/mstts" xml:lang="zh-CN">
    <voice name=${voice_name}>
        女儿看见父亲走了进来，问道：
        <mstts:express-as role="YoungAdultFemale" style="calm">
            “您来的挺快的，怎么过来的？”
        </mstts:express-as>
        父亲放下手提包，说：
        <mstts:express-as role="OlderAdultMale" style="calm">
            “刚打车过来的，路上还挺顺畅。”
        </mstts:express-as>
    </voice>
</speak>
```
"""


def get_prompt(shots_content_detail, voice_name):
    return PROMPT_TEMPLATE.format(
        shots_content_detail=shots_content_detail,
        voice_name=voice_name,
        format_example=FORMAT_EXAMPLE,
    )


@log_io
def design_voice_prompt(voice_name, shots_content_detail, retry_count=0, max_retry=3):
    if retry_count < max_retry:
        try:
            retry_count += 1
            prompt = get_prompt(voice_name, shots_content_detail)
            design_voice_result = generate(
                prompt,
                model=TASK_MODEL_MAPPING["design_voice"]["model"],
                max_tokens=TASK_MODEL_MAPPING["design_voice"]["max_tokens"],
            )

            logger.info(design_voice_result)
            voice_prompt = (
                design_voice_result.strip("\n")
                .strip(" ")
                .replace("```", "")
                .strip("python")
            )
            return voice_prompt
        except Exception as e:
            return design_voice_prompt(
                voice_name, shots_content_detail, retry_count, max_retry
            )
    else:
        logger.error(f"design voice attempt {max_retry}")
        raise Exception("design voice failed")
