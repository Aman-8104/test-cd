from __future__ import annotations

import re
from pathlib import Path
from uuid import uuid4

from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

BASE_DIR = Path(__file__).resolve().parent
PUBLIC_DIR = BASE_DIR / "public"
UPLOADS_DIR = BASE_DIR / "uploads"
MAX_FILE_SIZE = 200 * 1024 * 1024  # 200MB
CHUNK_SIZE = 1024 * 1024

UPLOADS_DIR.mkdir(parents=True, exist_ok=True)

app = FastAPI(title="Video Upload API")
app.mount("/uploads", StaticFiles(directory=UPLOADS_DIR), name="uploads")


def _safe_file_name(original_name: str) -> str:
    source_name = Path(original_name).name
    extension = Path(source_name).suffix
    stem = Path(source_name).stem
    clean_stem = re.sub(r"[^a-zA-Z0-9_-]", "-", stem)[:60] or "video"
    return f"{clean_stem}-{uuid4().hex[:10]}{extension}"


@app.get("/")
def read_index() -> FileResponse:
    index_file = PUBLIC_DIR / "index.html"
    if not index_file.exists():
        raise HTTPException(status_code=404, detail="Frontend page not found.")

    return FileResponse(index_file)


@app.post("/api/upload-video", status_code=201)
async def upload_video(video: UploadFile = File(...)) -> dict[str, str | int]:
    content_type = video.content_type or ""
    if not content_type.startswith("video/"):
        raise HTTPException(status_code=400, detail="Only video files are allowed.")

    saved_name = _safe_file_name(video.filename or "video")
    destination = UPLOADS_DIR / saved_name

    bytes_written = 0
    try:
        with destination.open("wb") as buffer:
            while True:
                chunk = await video.read(CHUNK_SIZE)
                if not chunk:
                    break

                bytes_written += len(chunk)
                if bytes_written > MAX_FILE_SIZE:
                    raise HTTPException(
                        status_code=400,
                        detail="Video is too large. Maximum size is 200MB.",
                    )
                buffer.write(chunk)
    except HTTPException:
        if destination.exists():
            destination.unlink(missing_ok=True)
        raise
    except Exception as exc:
        if destination.exists():
            destination.unlink(missing_ok=True)
        raise HTTPException(status_code=500, detail="Upload failed.") from exc
    finally:
        await video.close()

    return {
        "message": "Upload successful.",
        "fileName": saved_name,
        "originalFileName": video.filename or "",
        "size": bytes_written,
    }
