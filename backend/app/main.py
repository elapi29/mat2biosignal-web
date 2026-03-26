from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.responses import FileResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path
import shutil
import subprocess
import tempfile
import uuid
import zipfile

app = FastAPI(title="mat2biosignal-web")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

BASE_DIR = Path(__file__).resolve().parent.parent
PROJECT_ROOT = BASE_DIR.parent
ENGINE_DIR = PROJECT_ROOT / "engine"
ENGINE_BINARY = ENGINE_DIR / "mat2biosignal"

JOBS_DIR = PROJECT_ROOT / "jobs"
JOBS_DIR.mkdir(exist_ok=True)


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/convert")
async def convert_mat_file(
    file: UploadFile = File(...),
    output_prefix: str = Form(...)
):
    if not file.filename.endswith(".mat"):
        raise HTTPException(status_code=400, detail="Only .mat files are supported.")

    if not ENGINE_BINARY.exists():
        raise HTTPException(
            status_code=500,
            detail="Engine binary not found at engine/mat2biosignal"
        )

    job_id = str(uuid.uuid4())
    job_dir = JOBS_DIR / job_id
    input_dir = job_dir / "input"
    output_dir = job_dir / "output"
    input_dir.mkdir(parents=True, exist_ok=True)
    output_dir.mkdir(parents=True, exist_ok=True)

    input_path = input_dir / file.filename
    with input_path.open("wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    output_base = output_dir / output_prefix

    try:
        result = subprocess.run(
            [str(ENGINE_BINARY), str(input_path), str(output_base)],
            capture_output=True,
            text=True,
            check=True,
            cwd=str(PROJECT_ROOT)
        )
    except subprocess.CalledProcessError as e:
        raise HTTPException(
            status_code=500,
            detail={
                "message": "Conversion failed",
                "stdout": e.stdout,
                "stderr": e.stderr,
            }
        )

    generated_files = sorted(output_dir.glob(f"{output_prefix}*"))
    if not generated_files:
        raise HTTPException(
            status_code=500,
            detail="No output files were generated."
        )

    zip_path = job_dir / f"{output_prefix}_outputs.zip"
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zipf:
        for file_path in generated_files:
            zipf.write(file_path, arcname=file_path.name)

    return JSONResponse(
        {
            "job_id": job_id,
            "message": "Conversion successful",
            "stdout": result.stdout,
            "stderr": result.stderr,
            "files": [p.name for p in generated_files],
            "download_url": f"/download/{job_id}"
        }
    )


@app.get("/download/{job_id}")
def download_outputs(job_id: str):
    job_dir = JOBS_DIR / job_id
    if not job_dir.exists():
        raise HTTPException(status_code=404, detail="Job not found")

    zip_files = list(job_dir.glob("*_outputs.zip"))
    if not zip_files:
        raise HTTPException(status_code=404, detail="ZIP output not found")

    return FileResponse(
        path=zip_files[0],
        filename=zip_files[0].name,
        media_type="application/zip"
    )
