# Auto Cloud Files Backup

A Python script that watches your folders and automatically uploads new files to the cloud, so you never have to remember to back things up manually.

## What it does

- Watches folders like Documents, Desktop, and Pictures
- When a new file shows up, it's automatically uploaded to Backblaze B2 (cloud storage)
- Skips junk files (temp files, lock files, partial downloads) and files that are too small or too large
- Can run permanently in the background using systemd

## Tech used

- Python
- `watchdog` – detects file changes
- `b2sdk` – uploads to Backblaze B2
- `python-dotenv` – keeps API keys out of the code
- systemd – runs it in the background automatically

## How to use it

1. Install the requirements:
   ```bash
   pip install watchdog b2sdk python-dotenv
   ```

2. Create a `.env` file with your Backblaze info:
   ```
   B2_KEY_ID=your_key_id
   B2_APPLICATION_KEY=your_application_key
   BUCKET_NAME=your_bucket_name
   WATCH_FOLDERS=Documents,Desktop,Pictures
   MIN_FILE_SIZE_KB=1
   MAX_FILE_SIZE_MB=50
   ```

3. Run it:
   ```bash
   python3 auto_cloud_backup.py
   ```
