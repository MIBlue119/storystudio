# 🎬 StoryStudio - Your Personalized Storytelling Studio 📖

## Table of Contents
- [Introduction](#-storystudio---your-personalized-storytelling-studio-)
- [Showcase](#🎥-showcase-full-video-on-youtube)
- [How does it work?](#-how-does-it-work)
- [Flows of storystudio](#-flows-of-storystudio)
- [Installation](#installation)
- [Usage](#usage)
- [References](#references)
---
Welcome to **StoryStudio**! 🌟 Here, we're reimagining the art of storytelling by blending human imagination with the power of cutting-edge AI. Dive into an innovative experimets where stories are not just read, but experienced.

## 🎥 Showcase ([Full video on YouTube](https://www.youtube.com/watch?v=NEp_huFPfa0))
https://github.com/RayVentura/ShortGPT/assets/demo.mp4
## ✨ How does it work?

Ever thought about turning a simple topic or idea into a mesmerizing story, complete with visuals, voice narration, and music? That's exactly what StoryStudio promises!

## 🚀 Flow of storystudio
1. **Choose your Story's Essence:** Start with inputting a topic or a short description. This seed will be the heart of your personalized story.
2. **Let the Magic Begin:** 
   - GPT-4 gets to work and spins a tale based on your inputs.
   - The crafted story is then deconstructed into a dynamic storyboard - breaking down backgrounds, themes, characters, and even scene-specific music.
   - The story is also seamlessly split into a voice-over script.
3. **Making it Real:**
   - The script is transformed into engaging narration via Azure Cognitive API's Text-To-Speech (TTS).
   - Visuals for the storyboard frames come alive with the prowess of Stability API.
   - Scene music isn't just generic; it's crafted using the Replicate API to resonate with the story's mood.
4. **Integration Symphony:**
   - Synthesis of TTS-generated sound, word by word.
   - A harmonious blend of generated images.
   - The magic of music.
   - Everything is connected to give you a story experience like never before!

## Installation

To set up storystudio on your machine, simply run:
```bash
$ poetry install
```

## Usage
### Prepare API keys
1. **OpenAI (LLM):** 
   - **Key Name:** `OPENAI_API_KEY`
   - **Purpose:** For LLM usage.
   - **Acquisition:** Follow the [OpenAI documentation](https://help.openai.com/en/articles/4936850-where-do-i-find-my-secret-api-key) to obtain your OpenAI API key.

2. **Azure Speech Service (TTS):**
   - **Key Names:** `AZURE_SPEECH_KEY` and `AZURE_SPEECH_REGION`
   - **Purpose:** For TTS functionality.
   - **Acquisition:** Refer to the [Azure documentation](https://learn.microsoft.com/en-us/azure/ai-services/speech-service/get-started-text-to-speech?tabs=macos%2Cterminal&pivots=programming-language-python) to activate the Azure speech service and retrieve the necessary keys.

3. **Replicate (MusicGen):**
   - **Key Name:** `REPLICATE_API_TOKEN`
   - **Purpose:** Call the MusicGen API at Replicate to generate background music.
   - **Acquisition:** Follow the instructions provided in the [Replicate documentation](https://replicate.com/docs/get-started/python) to obtain your API token.

4. **Stability (SDXL):**
   - **Key Name:** `STABILITY_KEY`
   - **Purpose:** Interface with Stability SDXL for image generation.
   - **Acquisition:** Visit the [Stability documentation](https://platform.stability.ai/docs/getting-started/authentication) to get your key.

5. Copy `.env.example` to `.env` and fill the key values
### Happy Generating with CLI
```
$poetry run python storystudio/generate.py
```

### Use at python
```
from storystudio.generate import Studio

your_studio = Studio()
seed_story="HarryPotter is transferred to Naruto's world"
export_dir="./mystory" #Change to your desired path
your_studio.run(seed_story=seed_story, export_dir=export_dir)
```


## References
- Main structures refer to [MetaGPT](https://github.com/geekan/MetaGPT)
- https://github.com/RayVentura/ShortGPT