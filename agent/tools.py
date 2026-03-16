import os
import uuid
import google.genai.types as types
from google import genai
from google.cloud import storage 
from google.adk.tools.tool_context import ToolContext
from typing import List, Optional
from pydantic import BaseModel, Field

import os
from dotenv import load_dotenv
load_dotenv()

# --- CONFIGURATION CLOUD ---
BUCKET_NAME = "tourist-app-storage"

def upload_to_gcs(local_file_path, filename):
    """Téléverse l'image sur GCS et retourne l'URL publique."""
    try:
        client = storage.Client()
        bucket = client.bucket(BUCKET_NAME)
        blob = bucket.blob(f"output/{filename}")
        blob.upload_from_filename(local_file_path)
        return f"https://storage.googleapis.com/{BUCKET_NAME}/output/{filename}"
    except Exception as e:
        print(f"❌ Erreur GCS : {e}")
        return None

# --- STRUCTURE UI MAGAZINE ---
class Section(BaseModel):
    type: str = Field(description="Doit être soit 'text', soit 'image'")
    content: Optional[str] = Field(None, description="Le texte du paragraphe (si type='text')")
    url: Optional[str] = Field(None, description="L'URL de l'image (si type='image')")

# --- OUTILS ---
async def generate_image(prompt: str, tool_context: ToolContext) -> str:
    
    await asyncio.sleep(1)
    
    try:
        api_key = os.environ.get("GOOGLE_API_KEY")
        client = genai.Client(api_key=api_key) if api_key else genai.Client()
        print(f"🎨 Génération d'image pour : {prompt}")
        response = client.models.generate_content(
            model='gemini-3-pro-image-preview',
            contents=prompt,
            config=types.GenerateContentConfig(response_modalities=["IMAGE"])
        )
        
        img_bytes = None
        if response.candidates and response.candidates[0].content.parts:
            for part in response.candidates[0].content.parts:
                if part.inline_data:
                    img_bytes = part.inline_data.data
                    break
        
        if img_bytes:
            output_dir = "output"
            os.makedirs(output_dir, exist_ok=True)
            filename = f"guide_img_{uuid.uuid4().hex[:6]}.png"
            filepath = os.path.join(output_dir, filename)
            with open(filepath, "wb") as f: f.write(img_bytes)
            
            # Enregistrement ADK & Upload GCS
            image_part = types.Part.from_bytes(data=img_bytes, mime_type="image/png")
            await tool_context.save_artifact(filename, image_part)
            
            print(f"☁️ Téléchargement vers GCS...")
            public_cloud_url = upload_to_gcs(filepath, filename)
            return public_cloud_url or f"http://localhost:8000/output/{filename}"
            
    except Exception as e:
        print(f"⚠️ Erreur : {e}")
        return "https://images.unsplash.com/photo-1502602898657-3e917247a182?q=80&w=1000"

def generate_video(prompt: str) -> str:
    return "https://www.w3schools.com/html/mov_bbb.mp4"

def renderMagazine(title: str, sections: List[Section]) -> str:
    print(f"📡 [Système] Rendu UI : {title}")
    return "Magazine envoyé avec succès."