# backend/app.py
from typing import Optional
import os
from io import BytesIO
from pathlib import Path
from uuid import uuid4


from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from dotenv import load_dotenv
from elevenlabs.client import ElevenLabs

from storage import init_db, insert_transcript, get_transcript

# env + client
load_dotenv()
API_KEY = os.getenv("ELEVENLABS_API_KEY")
if not API_KEY:
    raise RuntimeError("ELEVENLABS_API_KEY missing in backend/.env")
client = ElevenLabs(api_key=API_KEY)

# app + cors
app = FastAPI(title="STT demo")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],          # tighten in prod
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ensure folders/db exist
UPLOAD_DIR = Path(__file__).parent / "uploads"
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
init_db()

@app.get("/api/health")
def health():
    return {"ok": True}

@app.post("/api/transcribe")
async def transcribe_audio(
    file: UploadFile = File(...),
    language_code: Optional[str] = Form(None),
    diarize: bool = Form(False),
    tag_audio_events: bool = Form(False),
):
    # save audio for auditing
    suffix = Path(file.filename).suffix or ".webm"
    fname = f"{uuid4().hex}{suffix}"
    fpath = UPLOAD_DIR / fname
    data = await file.read()
    fpath.write_bytes(data)

    # send to elevenlabs scribe
    try:
        audio_data = BytesIO(data)
        # model_id can stay scribe_v1
        # normalize falsy/empty language_code -> None so the SDK will auto-detect
        if language_code == "" or language_code is None:
            lc = None
        else:
            lc = language_code

        # Ensure boolean-like form values are proper booleans (FastAPI may receive strings)
        def to_bool(v):
            if isinstance(v, bool):
                return v
            if isinstance(v, str):
                return v.lower() in ("1", "true", "yes", "on")
            return bool(v)

        # Build kwargs and only include language_code when provided to avoid sending
        # an empty string to the ElevenLabs API (which returns invalid_language_code).
        kwargs = {
            "file": audio_data,
            "model_id": "scribe_v1",
            "diarize": to_bool(diarize),
            "tag_audio_events": to_bool(tag_audio_events),
        }
        if lc is not None:
            kwargs["language_code"] = lc

        resp = client.speech_to_text.convert(**kwargs)
    except Exception as e:
        # clean up if wanted: fpath.unlink(missing_ok=True)
        raise HTTPException(status_code=502, detail=f"STT error: {e}")

    # normalize text field from response
    # common fields: resp.text (or resp.get('text') if dict-like)
    text = getattr(resp, "text", None) or (resp.get("text") if isinstance(resp, dict) else None)
    if not text:
        # fallback to raw json if structure changes
        return JSONResponse({"id": None, "filename": fname, "raw": resp}, status_code=207)

    # store transcript; make sure the STT response is JSON-serializable
    stt_meta = None
    try:
        # pydantic or similar models may have a dict() method
        if hasattr(resp, "dict"):
            stt_meta = resp.dict()
        elif isinstance(resp, dict):
            stt_meta = resp
        else:
            stt_meta = str(resp)
    except Exception:
        stt_meta = str(resp)

    tid = insert_transcript(filename=fname, text=text, meta={"stt_response": stt_meta})

    return {"id": tid, "filename": fname, "text": text}

@app.get("/api/transcripts/{tid}")
def fetch_transcript(tid: int):
    rec = get_transcript(tid)
    if not rec:
        raise HTTPException(status_code=404, detail="Not found")
    return rec
