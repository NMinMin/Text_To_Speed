import io
import aiohttp
import edge_tts
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_URL = "https://api-cloud-u4v8.onrender.com/upload"


class TTSRequest(BaseModel):
    text: str
    voice: str = "ko-KR-SunHiNeural"
    filename: str = "speech.mp3"


async def generate_and_upload_tts(text: str, voice: str, filename: str = "speech.mp3"):
    if not text.strip():
        raise HTTPException(status_code=400, detail="Text cannot be empty")

    if not filename.endswith(".mp3"):
        filename = f"{filename}.mp3"

    # 1. Tạo audio MP3 từ edge_tts
    audio_data = bytearray()
    try:
        communicate = edge_tts.Communicate(text, voice)
        async for chunk in communicate.stream():
            if chunk["type"] == "audio":
                audio_data.extend(chunk["data"])
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"TTS generation error: {str(e)}")

    if not audio_data:
        raise HTTPException(status_code=500, detail="Failed to generate audio data")

    # 2. Upload file MP3 lên Cloud API
    form_data = aiohttp.FormData()
    form_data.add_field(
        "file",
        bytes(audio_data),
        filename=filename,
        content_type="audio/mpeg",
    )

    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(UPLOAD_URL, data=form_data) as response:
                if response.status != 200:
                    error_text = await response.text()
                    raise HTTPException(
                        status_code=502,
                        detail=f"Upload service failed with status {response.status}: {error_text}",
                    )
                return await response.json()
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Upload error: {str(e)}")


@app.post("/tts")
async def create_speech_post(request: TTSRequest):
    return await generate_and_upload_tts(
        text=request.text,
        voice=request.voice,
        filename=request.filename,
    )


@app.get("/tts")
async def create_speech_get(
    text: str,
    voice: str = "ko-KR-SunHiNeural",
    filename: str = "speech.mp3",
):
    return await generate_and_upload_tts(
        text=text,
        voice=voice,
        filename=filename,
    )