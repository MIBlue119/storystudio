import os
import time
from pathlib import Path

from loguru import logger

from storystudio.actions import (design_music, design_scene, design_voice,
                                 select_voice, write_shots_detail,
                                 write_shots_tldr,
                                 write_story_and_characters_intro)
from storystudio.tools import (caption, postprocess, stt, txt2image, txt2music,
                               txt2voice)
from storystudio.settings import app_settings

class Studio():
    app_settings = app_settings
    def __init__(self,default_seed_story=None):
        self.workspace = app_settings.WORKSPACE
        self.default_seed_story = default_seed_story if default_seed_story else "HarryPotter is transferred to Naruto's World."

    def _construct_new_export_dir(self, export_dir=None):
        if export_dir is None:
            timestamp = time.strftime("%Y%m%d-%H%M%S", time.localtime())
            self.export_dir = Path(f"./workspace/{timestamp}").resolve()
        else:
            self.export_dir = Path(export_dir).resolve()
        os.makedirs(self.export_dir , exist_ok=True) 

    
    def cli(self):
        """Ask user the seed story content"""
        print("="*100)
        print(self.app_settings.ClI_CONFIG.APP_LOGO)
        print('-'*80)
        print("Happy Generating!")
        seed_story=''
        while True:
            seed_story = input(f"Please Enter Your Seed Story (press 'g' for default seed story '{self.default_seed_story}'):")
            if seed_story == 'g':
                seed_story = self.default_seed_story
                logger.info(f"Using default seed story: {seed_story}")
            if seed_story !='':
                self.run(seed_story)

    def run(self, seed_story=None, export_dir=None):
        self._construct_new_export_dir(export_dir)
        story_intro = write_story_and_characters_intro.generate_story_intro(seed_story)

        # Generate shots tl;dr
        shots_tldr = write_shots_tldr.generate_shots_tldr(
            story_intro, story_intro["character_descripts"]
        )

        # Generate shots detail
        shots_detail = write_shots_detail.generate_shots_detail(
            story_intro, story_intro["character_descripts"], shots_tldr
        )

        # Export shots detail to json
        shots_detail_output_dir = os.path.join(self.export_dir, "shots_detail")
        caption.generate_caption(shots_detail, shots_detail_output_dir)

        # Select voice
        voice_name = select_voice.get_select_voice(shots_tldr)

        # Design voice
        logger.info("####### Start designing voice #######")
        # Iterate the "shots_content" to generate voice prompt
        shots_voice_detail = {}
        for key, value in shots_detail["shots_content"].items():
            shots_name = key
            shots_content_detail = value["detail_script"]
            voice_prompt = design_voice.design_voice_prompt(
                voice_name, shots_content_detail
            )
            shots_voice_detail[shots_name] = voice_prompt
        logger.info("####### Voice designed #######")
        logger.info(shots_voice_detail)
        logger.info("####### End designing voice #######")

        logger.info("Save voice prompt to json")
        # Save voice prompt to json
        voice_prompt_output_dir = os.path.join(self.export_dir, "voice_prompt")
        txt2voice.save_voice_prompt(shots_voice_detail, voice_prompt_output_dir)

        # Generate scene prompt
        scene_prompt = design_scene.design_scene_prompt(story_intro, shots_detail)

        # Save scene prompt to json
        scene_prompt_output_dir = os.path.join(self.export_dir, "scene_prompt")
        txt2image.save_scene_prompt(scene_prompt, scene_prompt_output_dir)

        # Generate scene
        scene_output_dir = os.path.join(self.export_dir, "scene")
        txt2image.generate_scene(scene_prompt, scene_output_dir)

        # Generate voice
        voice_output_dir = os.path.join(self.export_dir, "voice")
        txt2voice.generate_scene_voice(shots_voice_detail, voice_output_dir)

        # Generate music prompt
        music_prompt = design_music.design_music_prompt(shots_detail)
        logger.info(music_prompt)

        # Save music prompt to json
        music_prompt_output_dir = os.path.join(self.export_dir, "music_prompt")
        txt2music.save_scene_music_prompt(music_prompt, music_prompt_output_dir)

        # Generate music
        music_output_dir = os.path.join(self.export_dir, "music")
        txt2music.generate_scene_music(music_prompt, music_output_dir)

        # Generate voice to text
        voice_to_text_output_dir = os.path.join(self.export_dir, "voice_to_text")
        stt.generate_voice_to_text(voice_output_dir, voice_to_text_output_dir)

        # # Merge voice and scene
        video_output_dir = os.path.join(self.export_dir, "video")
        postprocess.create_video_from_shots(
            scene_output_dir,
            voice_output_dir,
            music_output_dir,
            video_output_dir,
            voice_to_text_output_dir,
        )        


if __name__ == "__main__":
    your_studio = Studio()
    your_studio.cli()