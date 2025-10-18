# Emotion Agent Microservice

A FastAPI microservice for the ASL Translation system that interprets **emotion** and **intent** from model outputs, mapping them into expressive metadata — such as punctuation and text-to-speech (TTS) tone — to make generated speech more natural.

---

## Overview
**Resources:**
- **`EmotionAnalysis`** – Configuration rules mapping (emotion, intent) → punctuation/TTS adjustments.  
- **`AgentSession`** – Runtime records of processed inputs and generated metadata.

---

## API Reference
- This project follows an API-first workflow defined in Swagger.
- View the latest Swagger contract on SwaggerHub: [ASL Emotion Agent API](https://app.swaggerhub.com/apis/personalcx/ASLAgent/1.0.0)
- Resolved contract included in the repo: `swagger_api.json`
- Quick preview of the documented endpoints:

[![Swagger documentation preview](doc/swagger.png)](https://app.swaggerhub.com/apis/personalcx/ASLAgent/1.0.0)

---

## Run Locally
```bash
git clone https://github.com/char15xu/aslagent.git
cd aslagent
python3 -m venv venv && source venv/bin/activate
pip install -r requirements.txt
python main.py
