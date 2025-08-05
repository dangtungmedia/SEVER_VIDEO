from fastapi import FastAPI, Request, UploadFile, File, Form
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

import json
from datetime import datetime
from pathlib import Path

app = FastAPI()

templates = Jinja2Templates(directory="app/templates")
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# ✅ Sửa đường dẫn root nếu muốn lưu ở ổ lớn (ví dụ /mnt/data/media)
UPLOAD_ROOT = Path("/mnt/data/media/")
UPLOAD_DIRS = {
    "content": UPLOAD_ROOT / "content",
    "reupload": UPLOAD_ROOT / "reupload"
}
METADATA_FILE = Path("data.json") 

# ✅ Tạo thư mục nếu chưa có
for path in UPLOAD_DIRS.values():
    path.mkdir(parents=True, exist_ok=True)

# ✅ Tạo file metadata nếu chưa có
if not METADATA_FILE.exists():
    METADATA_FILE.write_text(json.dumps({"content": [], "reupload": []}, indent=2))

@app.get("/", response_class=HTMLResponse)
async def homepage(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/upload/")
async def upload_file(
    file: UploadFile = File(...),
    target: str = Form(...)
):
    if target not in UPLOAD_DIRS:
        return JSONResponse(status_code=400, content={"error": "Invalid target folder!"})

    # ✅ Lưu file vào thư mục tương ứng
    dest_folder = UPLOAD_DIRS[target]
    dest_path = dest_folder / file.filename

    with open(dest_path, "wb") as f:
        content = await file.read()
        f.write(content)

    # ✅ Cập nhật metadata
    metadata = {
        "filename": file.filename,
        "saved_path": str(dest_path),
        "upload_time": datetime.now().isoformat()
    }

    data = json.loads(METADATA_FILE.read_text())
    data[target].append(metadata)
    METADATA_FILE.write_text(json.dumps(data, indent=2, ensure_ascii=False))

    return {"message": "Upload thành công", "target": target, "filename": file.filename}
