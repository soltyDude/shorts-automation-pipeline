# tts_generator.py

import os
import requests

VOICE_ID = "EXAVITQu4vr4xnSDxMaL"


def generate_voice(text_file_path: str, output_path: str = "voice.mp3"):
    api_keys_raw = os.getenv("ELEVENLABS_API_KEYS")

    if not api_keys_raw:
        raise ValueError("ELEVENLABS_API_KEYS is not set")

    api_keys = [key.strip() for key in api_keys_raw.split(",") if key.strip()]

    if not api_keys:
        raise ValueError("No valid ElevenLabs API keys provided")

    with open(text_file_path, "r", encoding="utf-8") as f:
        story_text = f.read()

    if not story_text.strip():
        raise ValueError("Input text is empty")

    for idx, key in enumerate(api_keys):
        print(f"[TTS] Trying API key #{idx + 1}")

        try:
            response = requests.post(
                f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE_ID}",
                headers={
                    "xi-api-key": key,
                    "Content-Type": "application/json"
                },
                json={
                    "text": story_text,
                    "model_id": "eleven_multilingual_v2",
                    "voice_settings": {
                        "stability": 0.5,
                        "similarity_boost": 0.7,
                        "style": 0.3,
                        "use_speaker_boost": True
                    }
                },
                timeout=30
            )

            if response.status_code == 200:
                with open(output_path, "wb") as out:
                    out.write(response.content)

                print(f"[TTS] Success. Voice saved to {output_path}")
                return

            # если лимит или ошибка → пробуем следующий ключ
            print(f"[TTS] Failed with key #{idx + 1}: {response.status_code}")

        except Exception as e:
            print(f"[TTS] Error with key #{idx + 1}: {e}")

    raise RuntimeError("All ElevenLabs API keys failed")
