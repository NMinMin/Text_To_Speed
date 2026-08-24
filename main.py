import io
import edge_tts
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel

app = FastAPI()

# Bắt buộc thêm CORS để gọi được từ Front-end/App
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class TTSRequest(BaseModel):
    text: str
    voice: str = "ko-KR-SunHiNeural"


@app.post("/tts")
async def generate_speech_post(request: TTSRequest):
    if not request.text.strip():
        raise HTTPException(
            status_code=400, detail="Text cannot be empty"
        )

    try:
        communicate = edge_tts.Communicate(request.text, request.voice)
        audio_bytes = b""

        async for chunk in communicate.stream():
            if chunk["type"] == "audio":
                audio_bytes += chunk["data"]

        return StreamingResponse(
            io.BytesIO(audio_bytes),
            media_type="audio/mpeg",
            headers={
                "Content-Disposition": "inline; filename=speech.mp3"
            },
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/tts")
async def generate_speech_get(
    text: str, voice: str = "ko-KR-SunHiNeural"
):
    req = TTSRequest(text=text, voice=voice)
    return await generate_speech_post(req)