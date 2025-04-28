from fastapi import FastAPI, UploadFile, File
from typing import Union
import uvicorn
import torch
from transformers import pipeline
from PIL import Image
import io

app = FastAPI()

# 加载本地模型（可以换成你自己的路径）
text_generator = pipeline("text-generation", model="gpt2")
image_captioner = pipeline("image-to-text", model="nlpconnect/vit-gpt2-image-captioning")
speech_recognizer = pipeline("automatic-speech-recognition", model="openai/whisper-small")


def detect_file_type(file_bytes: bytes) -> str:
    if file_bytes.startswith(b"\x89PNG") or file_bytes.startswith(b"\xff\xd8"):
        return "image"
    elif file_bytes.startswith(b"RIFF") and b"WAVE" in file_bytes[:12]:
        return "audio"
    else:
        return "text"

@app.get("/")
def read_root():
    return {"message": "Welcome to the MCP API!"}

@app.post("/mcp/")
async def mcp_infer(file: UploadFile = File(...), prompt: Union[str, None] = None):
    file_bytes = await file.read()
    file_type = detect_file_type(file_bytes)

    if file_type == "image":
        image = Image.open(io.BytesIO(file_bytes))
        caption = image_captioner(image)[0]['generated_text']
        return {"type": "image", "result": caption}

    elif file_type == "audio":
        # 保存音频临时文件
        with open("temp_audio.wav", "wb") as f:
            f.write(file_bytes)
        text = speech_recognizer("temp_audio.wav")["text"]
        return {"type": "audio", "result": text}

    else:
        # 文本模式，直接生成文本
        if not prompt:
            prompt = file_bytes.decode("utf-8")
        output = text_generator(prompt, max_length=500)[0]["generated_text"]
        return {"type": "text", "result": output}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)