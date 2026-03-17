import os
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from ag_ui_adk import ADKAgent, add_adk_fastapi_endpoint
from google.adk.agents import LlmAgent, SequentialAgent, ParallelAgent
from google.adk.tools import google_search
from google.adk.artifacts import InMemoryArtifactService
import asyncio

# Imports locaux
from instruction import (
    GUIDE_INSTRUCTION,
    ACTIVITY_ILLUSTRATOR_INSTRUCTION,
    PLACE_ILLUSTRATOR_INSTRUCTION,
    GUIDE_REDACTOR_INSTRUCTION,
)
from tools import generate_image, generate_video, renderMagazine

load_dotenv()

# --- CONFIGURATION AGENTS ---
model_flash = "gemini-2.5-flash"
model_pro = "gemini-2.5-pro"

guide_agent = LlmAgent(
    model=model_pro, name='guide_agent', instruction=GUIDE_INSTRUCTION, 
    tools=[google_search], output_key='guide_output'
)

activity_illustrator = LlmAgent(
    model=model_flash, name='activity_illustrator', instruction=ACTIVITY_ILLUSTRATOR_INSTRUCTION,
    tools=[generate_image, generate_video]
)

place_illustrator = LlmAgent(
    model=model_flash, name='place_illustrator', instruction=PLACE_ILLUSTRATOR_INSTRUCTION,
    tools=[generate_image]
)

visit_illustrator = ParallelAgent(
    name='visit_illustrator', sub_agents=[activity_illustrator, place_illustrator]
)

guide_redactor = LlmAgent(
    model=model_pro, name='guide_redactor', instruction=GUIDE_REDACTOR_INSTRUCTION, 
    tools=[renderMagazine]
)

tourist_guide_pipeline = SequentialAgent(
    name='my_tourist_agent', sub_agents=[guide_agent, visit_illustrator, guide_redactor]
)

# --- SERVEUR FASTAPI ---
app = FastAPI(title="Tourist Guide Agent API")
artifact_service = InMemoryArtifactService()

adk_tourist_agent = ADKAgent(
    adk_agent=tourist_guide_pipeline,
    user_id="demo_user",
    artifact_service=artifact_service,
    use_in_memory_services=True,
)

add_adk_fastapi_endpoint(app, adk_tourist_agent, path="/")

# Montage du dossier output pour l'accès local (fallback)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.join(BASE_DIR, "output")
os.makedirs(OUTPUT_DIR, exist_ok=True)
app.mount("/output", StaticFiles(directory=OUTPUT_DIR), name="output")

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)