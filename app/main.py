from fastapi import FastAPI, Request, UploadFile, File, Form
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

import json
from datetime import datetime
from pathlib import Path

app = FastAPI()

MEDIA_ROOT = Path("/app/media")
MEDIA_ROOT.mkdir(parents=True, exist_ok=True)

templates = Jinja2Templates(directory="app/templates")
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Serve file tĩnh tại /media (có hỗ trợ Range header để tua video)
app.mount("/media", StaticFiles(directory=MEDIA_ROOT), name="media")

METADATA_FILE = Path("data.json")
if not METADATA_FILE.exists():
    METADATA_FILE.write_text(json.dumps({"content": [], "reupload": []}, indent=2, ensure_ascii=False))

@app.get("/", response_class=HTMLResponse)
async def homepage(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/upload/")
async def upload_file(
    request: Request,
    file: UploadFile = File(...),
    target: str = Form(...),
):
    UPLOAD_DIRS = {
        "content": MEDIA_ROOT / "content",
        "reupload": MEDIA_ROOT / "reupload",
    }

    if target not in UPLOAD_DIRS:
        return JSONResponse(status_code=400, content={"error": "Invalid target folder! (content|reupload)"})

    dest_folder = UPLOAD_DIRS[target]
    dest_folder.mkdir(parents=True, exist_ok=True)

    # Lưu file
    dest_path = dest_folder / file.filename
    with open(dest_path, "wb") as f:
        f.write(await file.read())

    # Cập nhật metadata
    metadata = {
        "filename": file.filename,
        "saved_path": str(dest_path),
        "target": target,
        "upload_time": datetime.now().isoformat(),
    }
    db = json.loads(METADATA_FILE.read_text() or '{"content":[],"reupload":[]}')
    db[target].append(metadata)
    METADATA_FILE.write_text(json.dumps(db, indent=2, ensure_ascii=False))

    # Trả về URL xem trực tiếp (không cần giao diện)
    file_url = str(request.base_url).rstrip("/") + f"/media/{target}/{file.filename}"
    return {
        "message": "Upload thành công",
        "target": target,
        "filename": file.filename,
        "url": file_url
    }

