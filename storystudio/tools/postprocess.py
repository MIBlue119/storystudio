import os
import subprocess

from storystudio.utils import log_io


def get_audio_duration(voice_file_path):
    cmd = [
        "ffprobe",
        "-v",
        "error",
        "-show_entries",
        "format=duration",
        "-of",
        "default=noprint_wrappers=1:nokey=1",
        voice_file_path,
    ]
    result = subprocess.run(
        cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
    )
    return float(result.stdout.strip())


@log_io
def create_video_from_shots(
    scene_dir, voice_dir, music_dir, output_dir, subtitle_dir=None
):
    """Sythesize scene/voice/music to final story video."""
    # Check if the output directory exists. If not, create it.
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    video_clips = []

    # Get the list of shots based on audio files in the voice directory
    for voice_file in sorted(os.listdir(voice_dir)):
        if voice_file.endswith(".wav"):
            audio_duration = get_audio_duration(os.path.join(voice_dir, voice_file))
            shot_name = os.path.splitext(voice_file)[0]
            image_file = os.path.join(scene_dir, shot_name + ".png")
            music_file = os.path.join(music_dir, shot_name + ".mp3")
            video_clip = os.path.join(output_dir, shot_name + ".mp4")
            if subtitle_dir is not None and os.path.exists(
                os.path.join(subtitle_dir, f"{shot_name}.srt")
            ):
                subtitle_file = os.path.join(subtitle_dir, f"{shot_name}.srt")
                # append subtitle to the video: https://www.bannerbear.com/blog/how-to-add-subtitles-to-a-video-file-using-ffmpeg/
                cmd = [
                    "ffmpeg",
                    "-y",  # Overwrite output file if it exists
                    "-loop",
                    "1",
                    "-t",
                    str(audio_duration),
                    "-i",
                    image_file,
                    "-i",
                    os.path.join(voice_dir, voice_file),
                    "-i",
                    music_file,
                    "-vf",
                    f'subtitles={subtitle_file}:force_style="FontName=Arial"',
                    "-filter_complex",
                    f"[1:a]aformat=sample_fmts=fltp:sample_rates=44100:channel_layouts=stereo,volume=1[a1]; \
                    [2:a]aformat=sample_fmts=fltp:sample_rates=44100:channel_layouts=stereo,volume=0.3, \
                    afade=t=in:st=0:d=2,afade=t=out:st={audio_duration-2}:d=2[a2]; [a1][a2]amix=inputs=2:duration=first:dropout_transition=3",
                    "-c:v",
                    "libx264",
                    "-tune",
                    "stillimage",
                    "-c:a",
                    "aac",
                    "-b:a",
                    "192k",
                    "-pix_fmt",
                    "yuv420p",
                    video_clip,
                ]
            else:
                cmd = [
                    "ffmpeg",
                    "-y",  # Overwrite output file if it exists
                    "-loop",
                    "1",
                    "-t",
                    str(audio_duration),
                    "-i",
                    image_file,
                    "-i",
                    os.path.join(voice_dir, voice_file),
                    "-i",
                    music_file,
                    "-filter_complex",
                    f"[1:a]aformat=sample_fmts=fltp:sample_rates=44100:channel_layouts=stereo,volume=1[a1]; \
                    [2:a]aformat=sample_fmts=fltp:sample_rates=44100:channel_layouts=stereo,volume=0.3, \
                    afade=t=in:st=0:d=2,afade=t=out:st={audio_duration-2}:d=2[a2]; [a1][a2]amix=inputs=2:duration=first:dropout_transition=3",
                    "-c:v",
                    "libx264",
                    "-tune",
                    "stillimage",
                    "-c:a",
                    "aac",
                    "-b:a",
                    "192k",
                    "-pix_fmt",
                    "yuv420p",
                    video_clip,
                ]
            subprocess.run(cmd)
            video_clips.append(video_clip)
    # Sorted the video clips by their names (shot names) from 1 to n
    video_clips = sorted(
        video_clips, key=lambda x: int(x.split("shots")[-1].split(".")[0])
    )

    # Concatenate all the video clips into one video
    concat_file = os.path.join(output_dir, "concat.txt")
    with open(concat_file, "w") as f:
        for clip in video_clips:
            print(clip)
            f.write(f"file '{clip}'\n")

    final_output = os.path.join(output_dir, "final_output.mp4")
    cmd = [
        "ffmpeg",
        "-y",
        "-f",
        "concat",
        "-safe",
        "0",
        "-i",
        concat_file,
        "-c",
        "copy",
        final_output,
    ]
    subprocess.run(cmd)
    print(f"Video created at {final_output}")
    return final_output
