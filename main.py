from fastapi import FastAPI, File, UploadFile, Form, Request
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import shutil
import os
import base64

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.get("/", response_class=HTMLResponse)
async def get_form(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/upload/")
async def upload(
    request: Request,
    contract: UploadFile = File(...),
    signature_data: str = Form(...)
):
    # Guardar contrato
    contract_path = os.path.join(UPLOAD_FOLDER, "contract.pdf")
    with open(contract_path, "wb") as buffer:
        shutil.copyfileobj(contract.file, buffer)

    # Guardar firma (base64)
    signature_bytes = base64.b64decode(signature_data.split(",")[1])
    signature_path = os.path.join(UPLOAD_FOLDER, "signature.png")
    with open(signature_path, "wb") as f:
        f.write(signature_bytes)

    return templates.TemplateResponse("index.html", {
        "request": request,
        "message": "¡Contrato y firma guardados!",
        "contract_url": "/uploads/contract.pdf",
        "signature_url": "/uploads/signature.png"
    })

@app.get("/uploads/{filename}")
async def get_uploaded_file(filename: str):
    path = os.path.join(UPLOAD_FOLDER, filename)
    return FileResponse(path)

