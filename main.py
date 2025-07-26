# main.py
from gcp_auth import get_gcp_credentials
from gdrive_client import build_drive_service, download_file_by_name, upload_to_gcs
from tts_generator import generate_voice
from video_assembler import assemble_video
from zapcap_client import process_video_with_zapcap_direct


# Константы
BUCKET_NAME = "autopost-video"

STORY_FILE = "story.txt"
BG_FILE = "bg_converted.mp4"
VOICE_FILE = "voice.mp3"
FINAL_VIDEO = "final_output.mp4"
FINAL_WITH_SUBS = "final_with_subs.mp4"

if __name__ == "__main__":
    # 1) Авторизация
    creds = get_gcp_credentials()
    drive = build_drive_service(creds)

    # 2) Скачиваем исходники
    download_file_by_name(drive, STORY_FILE, STORY_FILE)
    download_file_by_name(drive, BG_FILE, BG_FILE)

    # 3) Озвучка
    generate_voice(STORY_FILE, VOICE_FILE)

    # 4) Склейка
    assemble_video(BG_FILE, VOICE_FILE, FINAL_VIDEO)

    # 5) (опционально) Заливаем собранное видео в GCS
    public_url = upload_to_gcs(creds, FINAL_VIDEO, BUCKET_NAME)
    print("🌐 Public GCS URL:", public_url)

    # 6) Отдаём локальный файл в ZapCap (надёжно, без 403)
    process_video_with_zapcap_direct(FINAL_VIDEO, FINAL_WITH_SUBS)

    print("🚀 Готово. Финальное видео с субтитрами сохранено.")
