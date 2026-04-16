# subtitles_generator.py

import whisper


def generate_subtitles(audio_path: str = "voice.mp3", output_path: str = "voice.srt"):
    model = whisper.load_model("base")
    result = model.transcribe(audio_path, task="transcribe", fp16=False)

    def format_time(t):
        hours = int(t // 3600)
        minutes = int((t % 3600) // 60)
        seconds = int(t % 60)
        milliseconds = int((t - int(t)) * 1000)
        return f"{hours:02}:{minutes:02}:{seconds:02},{milliseconds:03}"

    with open(output_path, "w", encoding="utf-8") as srt_file:
        for i, segment in enumerate(result["segments"]):
            srt_file.write(f"{i + 1}\n")
            srt_file.write(
                f"{format_time(segment['start'])} --> {format_time(segment['end'])}\n"
            )
            srt_file.write(f"{segment['text'].strip()}\n\n")

    print(f"Subtitles saved: {output_path}")
