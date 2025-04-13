from .worker_registry import WORKERS
from .utils import save_agent_log
from .models import OrchestrationPlan

def run_pipeline(image_path: str, plan: OrchestrationPlan, image_id: str):
    log = {
        "image_id": image_id,
        "original": image_path,
        "steps": [],
        "output_path": None
    }

    current_path = image_path

    for step in plan.steps:
        worker = WORKERS.get(step.name)
        if worker:
            current_path = worker(current_path)
            log["steps"].append({"name": step.name, "status": "done"})
        else:
            log["steps"].append({"name": step.name, "status": "missing"})

    log["output_path"] = current_path
    
    save_agent_log(image_id, log)

    return current_path, log
