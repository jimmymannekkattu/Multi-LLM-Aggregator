from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from services.llm_service import get_all_responses
from services.synthesis_service import synthesize_responses

app = FastAPI(title="Multi-LLM Aggregator API")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class QueryRequest(BaseModel):
    query: str

class QueryResponse(BaseModel):
    individual_responses: dict
    final_answer: str

@app.post("/ask", response_model=QueryResponse)
async def ask_swarm(request: QueryRequest):
    try:
        # 1. Fetch from all providers
        responses = await get_all_responses(request.query)
        
        # 2. Synthesize with offline model
        final_answer = await synthesize_responses(request.query, responses)
        
        return QueryResponse(
            individual_responses=responses,
            final_answer=final_answer
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import os

# Mount frontend directory for static assets if needed (though we just have one file now)
# app.mount("/static", StaticFiles(directory="../frontend"), name="static")

@app.get("/")
async def root():
    # Serve the static HTML file
    frontend_path = os.path.join(os.path.dirname(__file__), "../frontend/index.html")
    return FileResponse(frontend_path)
