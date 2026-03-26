# mat2biosignal-web

Minimal web interface for uploading MATLAB `.mat` biosignal files, running a C++ export engine, and downloading the generated CSV/TXT outputs as a ZIP.

## Architecture

- `frontend/` - static HTML/CSS/JS upload UI
- `backend/` - FastAPI service
- `engine/` - compiled `mat2biosignal` C++ binary

## Features

- Upload `.mat` file from the browser
- Set an output prefix
- Run the C++ exporter through a FastAPI backend
- Package generated outputs into a ZIP
- Download all exported files in one click

## Local setup

### Backend

```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
