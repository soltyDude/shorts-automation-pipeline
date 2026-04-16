# main.py

from gcp_auth import get_gcp_credentials
from gdrive_client import build_drive_service, download_file_by_name, upload_to_gcs
from tts_generator import generate_voice
from video_assembler import assemble_video
from zapcap_client import process_video_with_zapcap_direct


# Constants
BUCKET_NAME = "autopost-video"

STORY_FILE = "story.txt"
BG_FILE = "bg_converted.mp4"
VOICE_FILE = "voice.mp3"
FINAL_VIDEO = "final_output.mp4"
FINAL_WITH_SUBS = "final_with_subs.mp4"


def main():
    try:
        print("[1/6] Authenticating with Google Cloud...")
        creds = get_gcp_credentials()
        drive = build_drive_service(creds)

        print("[2/6] Downloading source files from Google Drive...")
        download_file_by_name(drive, STORY_FILE, STORY_FILE)
        download_file_by_name(drive, BG_FILE, BG_FILE)

        print("[3/6] Generating voice from text...")
        generate_voice(STORY_FILE, VOICE_FILE)

        print("[4/6] Assembling final video...")
        assemble_video(BG_FILE, VOICE_FILE, FINAL_VIDEO)

        print("[5/6] Uploading video to Google Cloud Storage...")
        public_url = upload_to_gcs(creds, FINAL_VIDEO, BUCKET_NAME)
        print(f"Public GCS URL: {public_url}")

        print("[6/6] Adding subtitles via ZapCap...")
        process_video_with_zapcap_direct(FINAL_VIDEO, FINAL_WITH_SUBS)

        print("Done. Final video with subtitles saved.")

    except Exception as e:
        print(f"[ERROR] {e}")


if __name__ == "__main__":
    main()
