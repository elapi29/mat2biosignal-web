# mat2biosignal-web

Single-page web app for uploading MATLAB biosignal files and downloading analysis-ready CSV/TXT exports powered by a C++ backend.

## Features

- Upload MATLAB `.mat` files from the browser
- Run a C++ export engine through FastAPI
- Download generated CSV/TXT outputs as a ZIP
- Single-process local app
- One local URL
- Visual processing state with loading spinner

## Architecture

- `backend/` - FastAPI app serving both API routes and frontend assets
- `engine/` - compiled `mat2biosignal` C++ binary
- `frontend/` - static UI assets served by FastAPI

## Local setup

### Create the backend environment

```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
