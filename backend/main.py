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

genai_processor = GeminiProcessor(
        model_name = "gemini-pro",
        project = "ai-dev-cqc-q1-2024"
    )

@app.post("/analyze_video")
def analyze_video(request: VideoAnalysisRequest):
    # Doing the analysis
    processor = YoutubeProcessor(genai_processor = genai_processor)
    result = processor.retrieve_youtube_documents(str(request.youtube_link), verbose=False)
    
    #summary = genai_processor.generate_document_summary(result, verbose=True)
    
    # Find key concepts
    raw_concepts = processor.find_key_concepts(result, verbose=True)
    
    # Deconstruct
    unique_concepts = {}
    for concept_dict in raw_concepts:
        for key, value in concept_dict.items():
            unique_concepts[key] = value
    
    # Reconstruct
    key_concepts_list = [{key: value} for key, value in concept_dict.items()]
    
    return {
        "key_concepts": key_concepts_list
    }
