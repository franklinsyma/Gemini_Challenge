import os
import uuid
import google.genai.types as types
from google import genai
from google.adk.tools.tool_context import ToolContext
from typing import List, Optional
from pydantic import BaseModel, Field


async def generate_image(prompt: str, tool_context: ToolContext) -> str:
    """
    Génère une image avec Gemini, la stocke en tant qu'artefact ADK 
    et retourne l'URL d'accès pour le frontend.
    """
    try:
        # 1. Initialisation du client Gemini
        api_key = os.environ.get("GOOGLE_API_KEY")
        client = genai.Client(api_key=api_key) if api_key else genai.Client()

        # 2. Génération de l'image
        print(f"🎨 Génération d'image pour : {prompt}")
        response = client.models.generate_content(
            model='gemini-3-pro-image-preview',
            contents=prompt,
            config=types.GenerateContentConfig(
                response_modalities=["IMAGE"],
            )
        )
        
        img_bytes = None
        if response.candidates and response.candidates[0].content.parts:
            for part in response.candidates[0].content.parts:
                if part.inline_data:
                    img_bytes = part.inline_data.data
                    break
                
        
        if img_bytes:
            # 1. On sauvegarde dans le dossier output (comme tu l'as remarqué)
            output_dir = "output"
            os.makedirs(output_dir, exist_ok=True)
            filename = f"guide_img_{uuid.uuid4().hex[:6]}.png"
            filepath = os.path.join(output_dir, filename)
            
            with open(filepath, "wb") as f:
                f.write(img_bytes)
            
            # 2. On l'enregistre dans l'ADK (pour que l'agent garde le contexte)
            image_part = types.Part.from_bytes(data=img_bytes, mime_type="image/png")
            await tool_context.save_artifact(filename, image_part)
            
            # 3. LA CORRECTION EST ICI : On donne la nouvelle URL FastAPI
            artifact_url = f"http://localhost:8000/output/{filename}"
            
            print(f"✅ Artefact sauvegardé et disponible sur : {artifact_url}")
            return artifact_url
        
    except Exception as e:
        print(f"⚠️ Erreur génération : {e}")
        # On renvoie une image élégante par défaut pour ne pas bloquer le Rédacteur
        return "https://images.unsplash.com/photo-1502602898657-3e917247a182?q=80&w=1000&auto=format&fit=crop"
        

from typing import List, Optional
from pydantic import BaseModel, Field

# 1. On définit la structure exacte d'une section pour Gemini
class Section(BaseModel):
    type: str = Field(description="Doit être soit 'text', soit 'image'")
    content: Optional[str] = Field(None, description="Le texte du paragraphe (si type='text')")
    url: Optional[str] = Field(None, description="L'URL de l'image (si type='image')")

# 2. On modifie la signature de l'outil pour utiliser ce modèle
def renderMagazine(title: str, sections: List[Section]) -> str:
    """
    Affiche le guide touristique final sous forme de magazine visuel interactif.
    """
    print(f"📡 [Système] Demande de rendu UI interceptée pour le titre : {title}")
    return "Magazine envoyé à l'interface avec succès."

def generate_video(prompt: str) -> str:
    """
    Mockup pour la vidéo. 
    En production, on ferait une logique similaire avec un fichier .mp4
    """
    # On utilise une vidéo de test stable pour la démo
    return "https://www.w3schools.com/html/mov_bbb.mp4"