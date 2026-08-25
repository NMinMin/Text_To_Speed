import edge_tts
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel

app = FastAPI()

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
        raise HTTPException(status_code=400, detail="Text cannot be empty")

    # Hàm generator để stream dữ liệu âm thanh ngay khi vừa tạo xong từng chunk
    async def audio_stream():
        try:
            communicate = edge_tts.Communicate(request.text, request.voice)
            async for chunk in communicate.stream():
                if chunk["type"] == "audio":
                    yield chunk["data"]
        except Exception as e:
            print(f"Error streaming TTS: {e}")

    return StreamingResponse(
        audio_stream(),
        media_type="audio/mpeg",
        headers={
            "Content-Disposition": "inline; filename=speech.mp3",
            "Accept-Ranges": "bytes"
        }
    )


@app.get("/tts")
async def generate_speech_get(
    text: str, voice: str = "ko-KR-SunHiNeural"
):
    req = TTSRequest(text=text, voice=voice)
    return await generate_speech_post(req)