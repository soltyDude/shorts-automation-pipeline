# video_assembler.py

import subprocess


def assemble_video(background_path, audio_path, output_path):
    print(f"[VIDEO] Assembling: {background_path} + {audio_path} -> {output_path}")

    command = [
        "ffmpeg", "-y",
        "-stream_loop", "-1",
        "-i", background_path,
        "-i", audio_path,
        "-preset", "ultrafast",
        "-vf", "scale=720:1280",
        "-c:v", "libx264",
        "-c:a", "aac",
        "-shortest",
        output_path
    ]

    process = subprocess.Popen(
        command,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        universal_newlines=True
    )

    for line in process.stdout:
        print(line.strip())

    process.wait()

    if process.returncode == 0:
        print(f"[VIDEO] Success: {output_path}")
    else:
        raise RuntimeError(f"FFmpeg failed with code: {process.returncode}")
