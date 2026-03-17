# 🌍 Gemini Travel Concierge

![Gemini](https://img.shields.io/badge/Gemini%202.5-Pro%20%26%20Flash-blue?style=for-the-badge&logo=google)
![Google Cloud](https://img.shields.io/badge/Google_Cloud-Storage-4285F4?style=for-the-badge&logo=google-cloud)
![CopilotKit](https://img.shields.io/badge/CopilotKit-React_UI-black?style=for-the-badge)
![FastAPI](https://img.shields.io/badge/FastAPI-Backend-009688?style=for-the-badge&logo=fastapi)

**The Artificial Intelligence that doesn't just plan your trip, but designs it.**

Gemini Travel Concierge is an "Agentic UI" application developed for the Google AI Hackathon. It leverages the Google **ADK (Agent Development Kit)** to orchestrate a team of specialized AI agents capable of researching, illustrating, and formatting a bespoke, interactive travel magazine.

---

## ✨ Core Features

* **Real-Time Research:** Connects to the web via Google Search to ensure up-to-date recommendations for activities, restaurants, and landmarks.
* **Unique Visual Generation:** Creates stunning, AI-generated photographs (via Gemini Image capabilities) to dynamically illustrate each step of the journey.
* **Dynamic "Magazine" Interface:** Uses CopilotKit to transform the AI's JSON data stream into a premium, sequentially rendered web interface.
* **Cloud-Native Storage:** Asynchronously uploads generated visuals to Google Cloud Storage (GCS) for global availability and data persistence.

---

## 🏗️ Technical Architecture: The Power of the ADK

Instead of a simple scripted chatbot, our backend relies on a complex **Multi-Agent** system orchestrated by the Google ADK.



1. **The Guide (Research Agent - Gemini 2.5 Pro):** The "brain" that searches for the best destinations and crafts a logical, engaging itinerary.
2. **The Illustrators (Parallel Agents - Gemini 2.5 Flash):** Two agents (`activity_illustrator` and `place_illustrator`) work **simultaneously** to generate visual prompts and call the image generation API, cutting wait times by 50%.
3. **The Editor (Synthesis Agent):** Assembles the Guide's texts and the Illustrators' URLs (GCS or local fallback) to format the final output according to a strict schema expected by the frontend UI.

---

## 🛠️ Tech Stack

**Frontend:**
* React / Next.js
* CopilotKit (AI UI components & component streaming)
* Tailwind CSS (Premium editorial design)
* Zod (Schema validation)

**Backend:**
* Python 3.12+ / FastAPI
* Google ADK (Agent Development Kit)
* Google Cloud Storage (`google-cloud-storage` library)

---

## 🚀 Installation & Local Deployment

### 1. Prerequisites
* Node.js (18+)
* Python (3.12+)
* A Google API Key (Google AI Studio / Makersuite)
* A Google Cloud Service Account with a GCS bucket.

### 2. Backend Setup (Agent)
```bash
cd agent
# Create and activate the virtual environment
python -m venv .venv
source .venv/Scripts/activate  # On Windows
# Install dependencies
pip install -r requirements.txt
