# tts_generator.py
import requests

ELEVENLABS_API_KEYS = [
    "sk_d35dde92294f76432059473338017fb688dd7f258f6429fd",
    "sk_56e8bcc149299e04fed2345691ccb1d189ece419bad6afed"
]

VOICE_ID = "EXAVITQu4vr4xnSDxMaL"

def generate_voice(text_file_path: str, output_path: str = "voice.mp3"):
    with open(text_file_path, "r", encoding="utf-8") as f:
        story_text = f.read()

    for idx, key in enumerate(ELEVENLABS_API_KEYS):
        print(f"🔄 Ключ #{idx+1}")
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
                }
            )
            if response.status_code == 200:
                with open(output_path, "wb") as out:
                    out.write(response.content)
                print(f"✅ Озвучка сохранена: {output_path}")
                return
            else:
                print(f"⚠️ Ошибка: {response.status_code} - {response.text}")
        except Exception as e:
            print(f"❌ Ошибка ключа #{idx+1}: {e}")

    raise RuntimeError("⛔ Все ключи не сработали")
