import os
from dotenv import load_dotenv
from fastapi import FastAPI
from ag_ui_adk import ADKAgent, add_adk_fastapi_endpoint

from google.adk.agents import LlmAgent, SequentialAgent, ParallelAgent
from google.adk.tools import google_search
from google.adk.artifacts import InMemoryArtifactService

from fastapi.staticfiles import StaticFiles
import os




artifact_service = InMemoryArtifactService()


# On importe vos instructions et outils
from instruction import (
    GUIDE_INSTRUCTION,
    ACTIVITY_ILLUSTRATOR_INSTRUCTION,
    PLACE_ILLUSTRATOR_INSTRUCTION,
    GUIDE_REDACTOR_INSTRUCTION,
)
from tools import generate_image, generate_video, renderMagazine

load_dotenv()

# --- 1. VOS AGENTS ADK ---
model_flash = "gemini-2.5-flash" # Je vous conseille de repasser sur la 2.5 pour plus de stabilité, la 3 est très expérimentale
model_pro = "gemini-2.5-pro"

guide_agent = LlmAgent(
    model=model_pro,
    name='guide_agent',
    description='Recherche des infos sur la ville et propose des activités et des lieux, avec un résumé.',
    instruction=GUIDE_INSTRUCTION,
    tools=[google_search],
    output_key='guide_output'
)

activity_illustrator = LlmAgent(
    model=model_flash,
    name='activity_illustrator',
    description='Illustre les activités proposées par le guide.',
    instruction=ACTIVITY_ILLUSTRATOR_INSTRUCTION,
    tools=[generate_image, generate_video],
    output_key='activity_illustration'
)

place_illustrator = LlmAgent(
    model=model_flash,
    name='place_illustrator',
    description='Illustre les lieux à visiter proposés par le guide.',
    instruction=PLACE_ILLUSTRATOR_INSTRUCTION,
    tools=[generate_image],
    output_key='place_illustration'
)

visit_illustrator = ParallelAgent(
    name='visit_illustrator',
    sub_agents=[activity_illustrator, place_illustrator]
)

guide_redactor = LlmAgent(
    model=model_pro,
    name='guide_redactor',
    description='Rédige le guide final et l\'assemble.',
    instruction=GUIDE_REDACTOR_INSTRUCTION,
    tools= [renderMagazine]
)

tourist_guide_pipeline = SequentialAgent(
    name='my_tourist_agent', # C'est ce nom que CopilotKit va reconnaitre
    sub_agents=[guide_agent, visit_illustrator, guide_redactor]
)

root_agent=tourist_guide_pipeline
# --- 2. LE SERVEUR AG-UI (Spécifique au template CopilotKit) ---

# On encapsule votre agent avec l'adaptateur AG-UI
adk_tourist_agent = ADKAgent(
    adk_agent=tourist_guide_pipeline,
    user_id="demo_user",
    artifact_service=artifact_service,
    session_timeout_seconds=3600,
    use_in_memory_services=True,
)

# On crée le serveur FastAPI
app = FastAPI(title="Tourist Guide Agent API")
# On attache l'agent au serveur sur la route principale "/"
add_adk_fastapi_endpoint(app, adk_tourist_agent, path="/")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.join(BASE_DIR, "output")
app.mount("/output", StaticFiles(directory=OUTPUT_DIR), name="output")


if __name__ == "__main__":
    import uvicorn

    if not os.getenv("GOOGLE_API_KEY"):
        print("⚠️  Warning: GOOGLE_API_KEY environment variable not set!")

    port = int(os.getenv("PORT", 8000))
    # Le serveur se lance sur le port 8000
    uvicorn.run(app, host="0.0.0.0", port=port)