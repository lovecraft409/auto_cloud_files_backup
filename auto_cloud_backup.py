from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from b2sdk.v2 import InMemoryAccountInfo, B2Api
from dotenv import load_dotenv
import os
import time
import sys

load_dotenv()

application_key_id = os.getenv("B2_KEY_ID")
application_key = os.getenv("B2_APPLICATION_KEY")
watch_path = os.getenv("WATCH_FOLDER")
bucket_name = os.getenv("BUCKET_NAME")

info = InMemoryAccountInfo()
b2_api = B2Api(info)
b2_api.authorize_account("production", application_key_id, application_key)
bucket = b2_api.get_bucket_by_name("auto-backup-2026")
home = os.path.expanduser("~")
folders = os.getenv("WATCH_FOLDERS", "Documents").split(",")
min_size_kb = int(os.getenv("MIN_FILE_SIZE_KB", 1))
min_size_bytes = min_size_kb * 1024

print("Connected to Backblaze.")

SKIP_PATTERNS = (".swp", ".part", ".crdownload", ".tmp")

class MyHandler(FileSystemEventHandler):
    def on_created(self, event):
        if not event.is_directory:
            file_path = event.src_path
            file_name = os.path.basename(file_path)

            if file_name.startswith(".") or file_name.startswith("unconfirmed") or file_name.endswith(SKIP_PATTERNS):
                print(f"Skipping temp file: {file_name}")
                return

            file_size = os.path.getsize(file_path)

            if file_size < min_size_bytes:
                print(f"Skipping {file_name}: too small ({file_size} bytes, minimum is {min_size_kb} KB)")
                return

            print(f"New file detected: {file_path}")
            try:
                bucket.upload_local_file(local_file=file_path, file_name=file_name)
                print(f"Uploaded {file_name} to Backblaze.")
            except Exception as e:
                print(f"Upload failed: {e}")

observer = Observer()
for folder in folders:
    folder_path = os.path.join(home, folder.strip())
    observer.schedule(MyHandler(), path=folder_path, recursive=True)
    print(f"Watching: {folder_path}")
observer.start()

print("Watching Documents folder... press Ctrl+C to stop")

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    observer.stop()

observer.join()