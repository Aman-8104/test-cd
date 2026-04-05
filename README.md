# FastAPI Video Upload

A simple FastAPI application with a beautiful UI for uploading videos.

## Setup

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the server:**
   ```bash
   uvicorn app:app --host 0.0.0.0 --port 3000 --reload
   ```

3. **Open in browser:**
   ```
   http://localhost:3000
   ```

## Features

- 🎥 Drag-and-drop video upload
- 🎨 Beautiful, responsive UI
- 📁 Unique filename generation
- 📏 200MB max file size
- ✅ Video format validation

## API

**POST /api/upload-video**

Upload a video file.

- **Form field:** `video` (file)
- **Response:**
  ```json
  {
    "message": "Upload successful.",
    "fileName": "my-video-a1b2c3d4e5.mp4",
    "originalFileName": "my-video.mp4",
    "size": 123456
  }
  ```

## Uploaded Files

Videos are saved in the `uploads/` directory.
