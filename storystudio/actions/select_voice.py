from loguru import logger

from storystudio.settings import TASK_MODEL_MAPPING
from storystudio.tools.llm import generate, parse_output
from storystudio.utils import log_io

PROMPT_TEMPLATE = """
# Context

## shots_tldr
{shots_tldr}

## Format example
{format_example}
-----
Role: You are a Azure TTS professional engineer and voice designer. 
According to your understanding of the shots_tldr and its language and read the azure_document section, select the appropriate voice which support the language and its style and role to synthesize the voice.
ATTENTION: Use '##' to SPLIT SECTIONS, not '#'. AND '## <SECTION_NAME>' SHOULD WRITE BEFORE the code and triple quote. Output carefully referenced "Format example" in format.
RULES: Please don't use any value already at the Example Output of the ## Format example.

# azure_document
```
- ## supported voices: record the voice name and its supported styles and roles
-------
## supported voices
| Voice | Styles |Roles |
| ----- | ----- | ----- |
|de-DE-ConradNeural<sup>1</sup>|`cheerful`|Not supported|
|en-GB-RyanNeural|`chat`, `cheerful`|Not supported|
|en-GB-SoniaNeural|`cheerful`, `sad`|Not supported|
|en-US-AriaNeural|`angry`, `chat`, `cheerful`, `customerservice`, `empathetic`, `excited`, `friendly`, `hopeful`, `narration-professional`, `newscast-casual`, `newscast-formal`, `sad`, `shouting`, `terrified`, `unfriendly`, `whispering`|Not supported|
|en-US-DavisNeural|`angry`, `chat`, `cheerful`, `excited`, `friendly`, `hopeful`, `sad`, `shouting`, `terrified`, `unfriendly`, `whispering`|Not supported|
|en-US-GuyNeural|`angry`, `cheerful`, `excited`, `friendly`, `hopeful`, `newscast`, `sad`, `shouting`, `terrified`, `unfriendly`, `whispering`|Not supported|
|en-US-JaneNeural|`angry`, `cheerful`, `excited`, `friendly`, `hopeful`, `sad`, `shouting`, `terrified`, `unfriendly`, `whispering`|Not supported|
|en-US-JasonNeural|`angry`, `cheerful`, `excited`, `friendly`, `hopeful`, `sad`, `shouting`, `terrified`, `unfriendly`, `whispering`|Not supported|
|en-US-JennyNeural|`angry`, `assistant`, `chat`, `cheerful`, `customerservice`, `excited`, `friendly`, `hopeful`, `newscast`, `sad`, `shouting`, `terrified`, `unfriendly`, `whispering`|Not supported|
|en-US-NancyNeural|`angry`, `cheerful`, `excited`, `friendly`, `hopeful`, `sad`, `shouting`, `terrified`, `unfriendly`, `whispering`|Not supported|
|en-US-SaraNeural|`angry`, `cheerful`, `excited`, `friendly`, `hopeful`, `sad`, `shouting`, `terrified`, `unfriendly`, `whispering`|Not supported|
|en-US-TonyNeural|`angry`, `cheerful`, `excited`, `friendly`, `hopeful`, `sad`, `shouting`, `terrified`, `unfriendly`, `whispering`|Not supported|
|es-MX-JorgeNeural|`chat`, `cheerful`|Not supported|
|fr-FR-DeniseNeural|`cheerful`, `sad`|Not supported|
|fr-FR-HenriNeural|`cheerful`, `sad`|Not supported|
|it-IT-IsabellaNeural|`chat`, `cheerful`|Not supported|
|ja-JP-NanamiNeural|`chat`, `cheerful`, `customerservice`|Not supported|
|pt-BR-FranciscaNeural|`calm`|Not supported|
|zh-CN-XiaohanNeural|`affectionate`, `angry`, `calm`, `cheerful`, `disgruntled`, `embarrassed`, `fearful`, `gentle`, `sad`, `serious`|Not supported|
|zh-CN-XiaomengNeural|`chat`|Not supported|
|zh-CN-XiaomoNeural|`affectionate`, `angry`, `calm`, `cheerful`, `depressed`, `disgruntled`, `embarrassed`, `envious`, `fearful`, `gentle`, `sad`, `serious`|`Boy`, `Girl`, `OlderAdultFemale`, `OlderAdultMale`, `SeniorFemale`, `SeniorMale`, `YoungAdultFemale`, `YoungAdultMale`|
|zh-CN-XiaoruiNeural|`angry`, `calm`, `fearful`, `sad`|Not supported|
|zh-CN-XiaoshuangNeural|`chat`|Not supported|
|zh-CN-XiaoxiaoNeural|`affectionate`, `angry`, `assistant`, `calm`, `chat`, `cheerful`, `customerservice`, `disgruntled`, `fearful`, `friendly`, `gentle`, `lyrical`, `newscast`, `poetry-reading`, `sad`, `serious`|Not supported|
|zh-CN-XiaoxuanNeural|`angry`, `calm`, `cheerful`, `depressed`, `disgruntled`, `fearful`, `gentle`, `serious`|`Boy`, `Girl`, `OlderAdultFemale`, `OlderAdultMale`, `SeniorFemale`, `SeniorMale`, `YoungAdultFemale`, `YoungAdultMale`|
|zh-CN-XiaoyiNeural|`affectionate`, `angry`, `cheerful`, `disgruntled`, `embarrassed`, `fearful`, `gentle`, `sad`, `serious`|Not supported|
|zh-CN-XiaozhenNeural|`angry`, `cheerful`, `disgruntled`, `fearful`, `sad`, `serious`|Not supported|
|zh-CN-YunfengNeural|`angry`, `cheerful`, `depressed`, `disgruntled`, `fearful`, `sad`, `serious`|Not supported|
|zh-CN-YunhaoNeural<sup>2</sup>|`advertisement-upbeat`|Not supported|
|zh-CN-YunjianNeural<sup>3,4</sup>|`angry`, `cheerful`, `depressed`, `disgruntled`, `narration-relaxed`, `sad`, `serious`, `sports-commentary`, `sports-commentary-excited`|Not supported|
|zh-CN-YunxiaNeural|`angry`, `calm`, `cheerful`, `fearful`, `sad`|Not supported|
|zh-CN-YunxiNeural|`angry`, `assistant`, `chat`, `cheerful`, `depressed`, `disgruntled`, `embarrassed`, `fearful`, `narration-relaxed`, `newscast`, `sad`, `serious`|`Boy`, `Narrator`, `YoungAdultMale`|
|zh-CN-YunyangNeural|`customerservice`, `narration-professional`, `newscast-casual`|Not supported|
|zh-CN-YunyeNeural|`angry`, `calm`, `cheerful`, `disgruntled`, `embarrassed`, `fearful`, `sad`, `serious`|`Boy`, `Girl`, `OlderAdultFemale`, `OlderAdultMale`, `SeniorFemale`, `SeniorMale`, `YoungAdultFemale`, `YoungAdultMale`|
|zh-CN-YunzeNeural|`angry`, `calm`, `cheerful`, `depressed`, `disgruntled`, `documentary-narration`, `fearful`, `sad`, `serious`|`OlderAdultMale`, `SeniorMale`|
-------
## voice_name: Provide as Python Dict[str, str], key is `voice_name` and the value is the selected voice name.
"""

FORMAT_EXAMPLE = """
Example Output:
---

## voice_name
```python
{
    "voice_name": "zh-TW-HsiaoChenNeural"
}
```
"""


def get_prompt(shots_tldr):
    return PROMPT_TEMPLATE.format(shots_tldr=shots_tldr, format_example=FORMAT_EXAMPLE)


def get_output_keys():
    return ["voice_name"]


@log_io
def get_select_voice(shots_tldr, retry_count=0, max_retry=3):
    if retry_count < max_retry:
        try:
            retry_count += 1
            prompt = get_prompt(shots_tldr["shots_tldr"])
            select_voice_result = generate(
                prompt,
                model=TASK_MODEL_MAPPING["select_voice"]["model"],
                max_tokens=TASK_MODEL_MAPPING["select_voice"]["max_tokens"],
            )
            select_voice_result_keys = get_output_keys()
            voice_name = parse_output(select_voice_result, select_voice_result_keys)
            return voice_name
        except Exception as e:
            return get_select_voice(shots_tldr, retry_count, max_retry)
    else:
        logger.error(f"select voice attempt {max_retry}")
        raise Exception("select voice failed")
