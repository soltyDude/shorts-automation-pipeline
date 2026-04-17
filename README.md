# Shorts Automation Pipeline

Automated pipeline for generating short-form videos with AI-generated voiceovers and subtitles.

## Stack

- **Python 3.8+**
- **Google Drive API** — download source files
- **Google Cloud Storage** — store generated videos
- **ElevenLabs TTS** — voice generation
- **OpenAI Whisper** — subtitle generation
- **ZapCap API** — automatic subtitle overlay
- **FFmpeg** — video assembly and processing

## Features

- Download story text and background video from Google Drive
- Generate natural voice from text using ElevenLabs TTS
- Assemble video with synchronized audio
- Upload to Google Cloud Storage
- Automatically add subtitles via ZapCap API
- Process multiple videos in pipeline

## Setup

### Prerequisites

- Python 3.8+
- FFmpeg installed
- Google Cloud Service Account with Drive API and GCS access
- ElevenLabs API key
- ZapCap API key

### Installation

```bash
pip install -r requirements.txt
```

### Configuration

1. Download GCP service account JSON from Google Cloud Console
2. Rename to `credentials.json` (use `credentials.example.json` as template)
3. Set environment variables:
```bash
   export ELEVENLABS_API_KEY="your_key"
   export ZAPCAP_API_KEY="your_key"
```

### Running

```bash
python main.py
```

## Project Structure

- `main.py` — entry point, orchestrates pipeline steps
- `gcp_auth.py` — Google Cloud authentication
- `gdrive_client.py` — Google Drive integration
- `tts_generator.py` — ElevenLabs voice generation
- `video_assembler.py` — FFmpeg video assembly
- `subtitles_generator.py` — Whisper subtitle generation
- `zapcap_client.py` — ZapCap API integration

## How It Works

1. **Authentication** → Load GCP credentials
2. **Download** → Fetch story.txt and bg_converted.mp4 from Drive
3. **Voice Generation** → Convert text to speech via ElevenLabs
4. **Assembly** → Combine background video with generated audio using FFmpeg
5. **Upload** → Store final video in Google Cloud Storage
6. **Subtitles** → Add automatic subtitles using ZapCap API

## Example Output

Input: story.txt, background.mp4  
Output: final_with_subs.mp4 (video with synchronized audio and subtitles)

## License

MIT
