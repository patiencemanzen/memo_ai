import json
import os
from google import genai
from google.genai import types

# --------------------------------------------------------------
# Configure Gemini Client
# --------------------------------------------------------------
GEN_AI_KEY = os.getenv("GENAI_API_KEY")
GEN_AI_MODEL = os.getenv("GENAI_MODEL", "gemini-1.5-pro")

if not GEN_AI_KEY:
    raise EnvironmentError("GENAI_API_KEY is not set in environment variables.")

client = genai.Client(api_key=GEN_AI_KEY)

# --------------------------------------------------------------
# LLM Client Class
# --------------------------------------------------------------
class Client:
    def generate_response(self, prompt: str, file_path: str, role: str = "user") -> dict:
        try:
            file = client.files.upload(file=file_path)

            contents = [
                types.Content(
                    role=role,
                    parts=[ 
                        types.Part.from_uri(file_uri=file.uri, mime_type="image/jpeg"),
                        types.Part.from_text(text=prompt) 
                    ],
                ),
            ]
            
            generate_content_config = types.GenerateContentConfig(
                response_mime_type="application/json",
            )
                    
            response = client.models.generate_content(
                model=GEN_AI_MODEL,
                contents=contents,
                config=generate_content_config,
            )

            raw_text = response.text.strip()
            return json.loads(raw_text)
        except Exception as e:
            raise ValueError(f"Failed to generate response: {e}")