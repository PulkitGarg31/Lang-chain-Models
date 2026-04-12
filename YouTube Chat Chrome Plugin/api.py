from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from CoreModel import extract_video_id, load_transcript, build_vectorstore, build_qa_chain

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

vectorstores = {}  # cache per video_id in memory

class QueryRequest(BaseModel):
    url: str
    query: str

@app.post("/chat")
async def chat(request: QueryRequest):
    video_id = extract_video_id(request.url)

    if video_id not in vectorstores:
        text = load_transcript(video_id)
        vectorstores[video_id] = (build_vectorstore(text, video_id), text)

    vectorstore, text = vectorstores[video_id]
    chain = build_qa_chain(vectorstore, text)

    def stream():
        for chunk in chain.stream(request.query):
            yield chunk

    return StreamingResponse(stream(), media_type="text/plain")