# ssml_string = open("ssml.xml", "r").read()
"""
Reference:
https://learn.microsoft.com/en-us/azure/cognitive-services/speech-service/speech-synthesis-markup-voice
https://learn.microsoft.com/zh-tw/azure/cognitive-services/speech-service/how-to-speech-synthesis?tabs=browserjs%2Cterminal&pivots=programming-language-python#use-ssml-to-customize-speech-characteristics
"""
import json
import os

import azure.cognitiveservices.speech as speechsdk

from storystudio.settings import app_settings
from storystudio.utils import log_io


def generate_voice(ssml_string, output_path):
    speech_config = speechsdk.SpeechConfig(
        subscription=app_settings.AZURE_SPEECH_KEY,
        region=app_settings.AZURE_SPEECH_REGION,
    )
    synthesizer = speechsdk.SpeechSynthesizer(
        speech_config=speech_config, audio_config=None
    )
    result = synthesizer.speak_ssml_async(ssml_string).get()

    stream = speechsdk.AudioDataStream(result)
    stream.save_to_wav_file(output_path)


@log_io
def generate_scene_voice(shots_voice_detail, output_dir):
    os.makedirs(output_dir, exist_ok=True)
    for key in shots_voice_detail:
        output_path = os.path.join(output_dir, f"{key}.wav")
        generate_voice(shots_voice_detail[key], output_path)


@log_io
def save_voice_prompt(shots_voice_detail, output_dir):
    os.makedirs(output_dir, exist_ok=True)
    # Export to json
    with open(os.path.join(output_dir, "shots_voice_detail.json"), "w") as f:
        json.dump(shots_voice_detail, f, indent=4)
