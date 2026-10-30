"""API REST de análisis de video con detección facial básica."""
from pathlib import Path
import tempfile

import cv2
from fastapi import FastAPI, File, HTTPException, UploadFile

app = FastAPI(
    title="Face Video Analysis API",
    description="API de demostración para analizar videos y detectar rostros. No identifica personas.",
    version="1.0.0",
)

ALLOWED_EXTENSIONS = {".mp4", ".avi", ".mov", ".mkv"}
MAX_BYTES = 50 * 1024 * 1024


def count_faces_in_video(path: str, max_frames: int = 300) -> dict:
    cap = cv2.VideoCapture(path)
    if not cap.isOpened():
        raise ValueError("No se pudo abrir el archivo como video.")

    classifier = cv2.CascadeClassifier(
        str(Path(cv2.data.haarcascades) / "haarcascade_frontalface_default.xml")
    )
    frame_index = 0
    total_faces = 0
    frames_with_faces = 0
    try:
        while frame_index < max_frames:
            ok, frame = cap.read()
            if not ok:
                break
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = classifier.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
            total_faces += len(faces)
            if len(faces):
                frames_with_faces += 1
            frame_index += 1
    finally:
        cap.release()

    if frame_index == 0:
        raise ValueError("El video no contiene fotogramas legibles.")

    return {
        "frames_analyzed": frame_index,
        "frames_with_faces": frames_with_faces,
        "face_detections_total": total_faces,
        "note": "Conteo de detecciones, no de personas únicas ni de identidades.",
    }


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/analyze")
async def analyze_video(file: UploadFile = File(...)):
    suffix = Path(file.filename or "").suffix.lower()
    if suffix not in ALLOWED_EXTENSIONS:
        raise HTTPException(status_code=415, detail="Formato no admitido. Use MP4, AVI, MOV o MKV.")

    content = await file.read(MAX_BYTES + 1)
    if len(content) > MAX_BYTES:
        raise HTTPException(status_code=413, detail="El archivo supera el límite de 50 MB.")
    if not content:
        raise HTTPException(status_code=400, detail="El archivo está vacío.")

    temp_path = None
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
            tmp.write(content)
            temp_path = tmp.name
        try:
            return count_faces_in_video(temp_path)
        except ValueError as exc:
            raise HTTPException(status_code=422, detail=str(exc)) from exc
    finally:
        if temp_path and Path(temp_path).exists():
            Path(temp_path).unlink()
