# Idea Plan

How could i combine current generative AI tool to make a storystudio.
Which could generate a video story with background music according to user's idea.

## Plans
- Users input a topic or short description
- Users can choose:
	- Scene style
	- Upload their own voice to duplicate, and use the duplicated voice to tell the story
- GPT-4 generates a story
- GPT-4, based on the story:
	- Deconstructs it into storyboard frames and scene music descriptions
		- Description of the background/theme/characters
	- Splits the story into a script based on the storyboard
- Send the script into Text-To-Speech (TTS)
	- Call Elevenlabs
- Send the description of storyboard frames into Stable XL to generate images
- Send the scene music description to Musicgen to generate music
- Integration:
	- TTS generates sound and script word by word
	- Images
	- Music combination
	- Synthesis after connecting everything together
- Transition can be added with a black screen, or something suitable

## System Design



## Possible data structures
```=json
{
    "story_intro": "Pikachu meets a new friend, Ditto, on the Good Hill during a summer evening.",
    "characters": {
        "total_characters": ["Pikachu", "Ditto"],
        "character_descripts":{
            "Pikachu": "Mischievous and adventurous, Pikachu loves to eat Big Malasada chocolate.",
            "Ditto": "Shy and lacks confidence in its original appearance."
        }
    },
    "scene_common_prompt": ["pixar_style", "cute", "high_resolution"],
    "shots_tldr":
    {
        "shots1": "On a summer evening after a frontal rain, Pikachu, exerting all his strength, runs up Good Hill to wait for the summer evening glow.",
        "shots2": "Before the evening glow arrives, Pikachu falls asleep in the wind-blown grass. A visitor who looks like him, named PikaQiu, arrives.",
        "shots3": "They chat about everything. When the sunset comes, all disguises are removed, and PikaQiu transforms back into the Ditto form that it doesn't like.",
        "shots4": "PikaQiu worries that Pikachu might not like Ditto's appearance, but Pikachu says he likes it. PikaQiu then tells Pikachu its real name, 'Ditto'."
    },
    "shots_content":
    {
        "shots1":{
            "detail_script": "The front of a summer evening with continuous rain just passed Good Hill, and the air is clear with no PM2.5. An active Pikachu rushes to Good Hill from afar because Good Hill is the best spot to view the beautiful summer sunset. It finally reaches the top of the hill, panting and muttering, 'Pika, PikaPikaPika' // Translation: 'Looks like, I need to lose weight.'",
            "captions": None,
            "scene_prompt": None,
            "bgm_prompt": None,
        },
        "shots2":{
            "detail_script": "At this time the sun is still at an angle of 40 degrees, still dazzling white-yellow. Pikachu seems to have arrived a bit early, so it lies down on the fluffy grass to sunbathe. The wind on Good Hill is always gentle to the visitors, unlike other high places. Pikachu enjoys the gentle breeze and drifts into a half-awake state. 'Sua SuaSuaSua Sua SuaSuaSua' seems to have a visitor approaching. The visitor speaks: 'PikaPika' // Translation: 'Hello there.' It seems to be of the same species as Pikachu, so Pikachu wakes up to see. Indeed, the visitor looks like him but with smaller eyes and a big smile. The visitor introduces herself as PikaQiu, and Pikachu welcomes her to lie down and wait for the evening glow together.",
            "captions": None,
            "scene_prompt": None,
            "bgm_prompt": None,
        },
        "shots3":{
            "detail_script": "But there's still some time before the evening glow, so they start to chat. From World Human Rights Day, how much they bought on Double 11, to what kind of chocolate they like, although they just met, they chat like old friends. As they chat, the sun falls to the angle where it starts to show its magical side, with flames spreading among the clouds in the sky. It happens that both Pikachu and PikaQiu fulfill the conditions of a legend at Good Hill, where all disguises will be removed during a magical moment of a summer evening. PikaQiu changes back into its original form, a purple irregular shape, but still with small eyes and a big smile. However, they both fail to notice as they are enchanted by the view. When the magical performance is about to end, they both look at each other, wanting to share their feelings. Pikachu is slightly surprised, PikaQiu, through the reflection in Pikachu's eyes, realizes she's changed back to her original form, which she doesn't want others to see.",
            "captions": None,
            "scene_prompt": None,
            "bgm_prompt": None,
        },
        "shots4":{
            "detail_script": "When PikaQiu wonders what to do, Pikachu speaks: 'You also look good in purple.' This is the first time PikaQiu, actually a Ditto, has been praised for its original form. Since Ditto lacks self-confidence, it often changes into other forms. PikaQiu asks, 'Don't you think I look strange like this? Won't you want to be my friend anymore?' Pikachu replies, 'No, I like it, there's no such thing as a strange appearance. I'm glad to have met you today, because with you, the evening glow on Good Hill has become even more unforgettable.' PikaQiu, with moist eyes, says: 'I'm also very glad to have met you. My real name is Ditto :)' 'Hello Ditto, nice to meet you :P,' says Pikachu.",
            "captions": None,
            "scene_prompt": None,
            "bgm_prompt": None,
        }
    }
}

```