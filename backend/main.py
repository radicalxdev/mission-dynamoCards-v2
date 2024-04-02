from fastapi import FastAPI
from pydantic import BaseModel, HttpUrl
from fastapi.middleware.cors import CORSMiddleware

from services.genai import (
    YoutubeProcessor,
    GeminiProcessor
)

class VideoAnalysisRequest(BaseModel):
    youtube_link: HttpUrl
    # advanced settings

app = FastAPI()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/analyze_video")
def analyze_video(request: VideoAnalysisRequest):
    # Doing the analysis
    processor = YoutubeProcessor()
    result = processor.retrieve_youtube_documents(str(request.youtube_link))
    
    genai_processor = GeminiProcessor(
        model_name = "gemini-pro",
        project = "ai-dev-cqc-q1-2024"
    )
    
    summary = genai_processor.generate_document_summary(result, verbose=True)
    
    return {
        "summary": summary
    }
