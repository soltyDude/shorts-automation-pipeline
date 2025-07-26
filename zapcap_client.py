import requests
import time

API_KEY = "fa859f53921dc5317d9b1d5f334f6f5076ae2d7776617c706aef2b81f7567a6e"
BASE = "https://api.zapcap.ai"
HEADERS_BASE = {
    "x-api-key": API_KEY,
    "Content-Type": "application/json"
}

# ⚠️ ВАЖНО: заменён шаблон на Felix
TEMPLATE_ID = "cc4b8197-2d49-4cc7-9f77-d9fbd8ef96ab"
LANGUAGE = "en"

def _raise_for_status(resp, action="request"):
    if not resp.ok:
        print(f"❌ {action} -> {resp.status_code}: {resp.text}")
        resp.raise_for_status()

def upload_video_direct(file_path: str) -> str:
    print(f"📥 Direct upload to ZapCap: {file_path}...")
    with open(file_path, "rb") as f:
        # fix UnicodeEncodeError using latin1-safe file name
        safe_name = file_path.encode('utf-8', errors='ignore').decode('latin-1', errors='ignore')
        files = {"file": (safe_name, f)}
        resp = requests.post(f"{BASE}/videos", headers={"x-api-key": API_KEY}, files=files)
    _raise_for_status(resp, "upload_video_direct")
    video_id = resp.json()["id"]
    print(f"📥 Direct upload successful. videoId = {video_id}")
    return video_id

def create_caption_task(
    video_id: str,
    language: str,
    auto_approve: bool,
    template_id: str,
    render_options: dict
) -> str:
    payload = {
        "language": language,
        "templateId": template_id,
        "autoApprove": auto_approve,
        "renderOptions": render_options
    }
    resp = requests.post(f"{BASE}/videos/{video_id}/task", headers=HEADERS_BASE, json=payload)
    _raise_for_status(resp, "create_caption_task")
    task_id = resp.json().get("taskId")  # <--- фикс
    print(f"✅ Subtitle task created. taskId = {task_id}")
    return task_id


def poll_task_status(video_id: str, task_id: str, output_path: str):
    print(f"⏳ Polling ZapCap for task {task_id} status...")
    while True:
        time.sleep(5)
        url = f"{BASE}/videos/{video_id}/task/{task_id}"
        resp = requests.get(url, headers=HEADERS_BASE)
        _raise_for_status(resp, "poll_task_status")
        data = resp.json()
        status = data.get("status")
        print(f"⌛ Status: {status}")

        if status == "completed":
            download_url = data["downloadUrl"]
            print(f"✅ Render complete. Downloading from: {download_url}")
            _download(download_url, output_path)
            print(f"🎉 Final video with subtitles: {output_path}")
            break
        elif status == "failed":
            raise RuntimeError("❌ ZapCap: subtitle task failed")

def _download(url, path):
    r = requests.get(url, stream=True)
    r.raise_for_status()
    with open(path, "wb") as f:
        for chunk in r.iter_content(chunk_size=1024 * 1024):
            if chunk:
                f.write(chunk)

def process_video_with_zapcap_direct(file_path: str, output_path: str):
    video_id = upload_video_direct(file_path)

    task_id = create_caption_task(
        video_id=video_id,
        language=LANGUAGE,
        auto_approve=True,
        template_id=TEMPLATE_ID,
        render_options={
            "subsOptions": {
                "emoji": True,
                "animation": True,
                "emphasizeKeywords": True
            },
            "styleOptions": {
                "fontSize": 46,
                "fontColor": "#ffffff"
            }
        }
    )
    poll_task_status(video_id, task_id, output_path)
