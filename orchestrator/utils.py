import json
import os
from datetime import datetime
from PIL import Image
import mimetypes

def save_agent_log(image_id, data):
    os.makedirs("api/orchestrator/logs", exist_ok=True)
    log_path = f"api/orchestrator/logs/AgentLog_{image_id}.json"
    with open(log_path, "w") as f:
        json.dump(data, f, indent=2)

def generate_image_id():
    return datetime.utcnow().strftime("%Y%m%d%H%M%S%f")

def generate_metadata_from_image(image_path: str) -> dict:
    """Extract basic metadata from the image."""
    metadata = {}

    try:
        with Image.open(image_path) as img:
            metadata["format"] = img.format
            metadata["mode"] = img.mode  # e.g., RGB, L (grayscale)
            metadata["width"], metadata["height"] = img.size

        metadata["file_size_kb"] = round(os.path.getsize(image_path) / 1024, 2)
        metadata["file_type"] = mimetypes.guess_type(image_path)[0]

        # You can add more sophisticated metadata here later (EXIF, color histograms, etc.)
    except Exception as e:
        metadata["error"] = str(e)

    return metadata
