import json
import os
from datetime import datetime

def save_agent_log(image_id, data):
    os.makedirs("api/orchestrator/logs", exist_ok=True)
    log_path = f"api/orchestrator/logs/AgentLog_{image_id}.json"
    with open(log_path, "w") as f:
        json.dump(data, f, indent=2)

def generate_image_id():
    return datetime.utcnow().strftime("%Y%m%d%H%M%S%f")
