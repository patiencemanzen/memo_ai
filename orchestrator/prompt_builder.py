from .worker_registry import WORKER_DESCRIPTIONS

def build_orchestration_prompt(image_preview_path: str, metadata: str) -> str:
    visible_workers = {
        name: desc for name, desc in WORKER_DESCRIPTIONS.items()
        if name not in ["metadata", "validate"]
    }

    step_options = "\n".join(
        f"- **{name}**: {desc}" for name, desc in visible_workers.items()
    )

    prompt = f"""
You are an AI controller for image restoration and enhancement.

### Objective:
Based on the input image and its metadata, analyze the visual quality and generate a list of required processing steps to improve it.

### Available Processing Steps:
{step_options}

### Instructions:
- Choose only necessary steps from the list above.
- Return them in order of execution.
- Add a short explanation of *why* each step is required.
- Include `"historian_review_required": true` if the image appears culturally or ethically sensitive (e.g., historical photos, identifiable individuals).
- Respond in the following format:

```json
{{
  "steps": [
    {{"name": "deblur", "reason": "The image is blurry with a 0.78 score"}},
    {{"name": "fix_faces", "reason": "Faces are present but unclear"}}
  ],
  "explanation": "The image is blurry, grayscale, and contains faces.",
  "historian_review_required": true
}}
```

### More Input:
Image path: {image_preview_path}
Metadata: {metadata}
""" 
    return prompt.strip()
