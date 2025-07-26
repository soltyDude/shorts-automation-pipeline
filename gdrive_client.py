# gdrive_client.py
import io
import os
from google.cloud import storage
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload

PROJECT_ID = "autopost-466916"  # твой
DRIVE_FIELDS = "files(id, name)"

def build_drive_service(creds):
    return build("drive", "v3", credentials=creds)

def download_file_by_name(service, filename, local_path):
    results = service.files().list(
        q=f"name='{filename}' and trashed = false",
        fields=DRIVE_FIELDS
    ).execute()

    items = results.get("files", [])
    if not items:
        raise FileNotFoundError(f"❌ Файл '{filename}' не найден на Google Drive.")

    file_id = items[0]["id"]
    request = service.files().get_media(fileId=file_id)
    with io.FileIO(local_path, "wb") as fh:
        downloader = MediaIoBaseDownload(fh, request)
        done = False
        while not done:
            status, done = downloader.next_chunk()
            if status:
                print(f"⬇️ Загрузка: {int(status.progress() * 100)}%")

    print(f"✅ Скачано: {filename} → {local_path}")

def upload_to_gcs(creds, local_path, bucket_name, destination_blob_name=None):
    if destination_blob_name is None:
        destination_blob_name = os.path.basename(local_path)

    client = storage.Client(project=PROJECT_ID, credentials=creds)
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)

    print(f"⬆️ Загрузка в gs://{bucket_name}/{destination_blob_name}")
    blob.upload_from_filename(local_path)

    # Uniform access → ACL запрещены, .make_public() не вызываем.
    print(f"✅ Public URL: {blob.public_url}")
    return blob.public_url
