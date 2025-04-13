from workers import (
    deblur_worker,
    superres_worker,
    facefix_worker,
    colorize_worker,
    metadata_worker,
    validator_worker,
    enhance_worker
)

WORKERS = {
    "colorize": colorize_worker.run,
    "deblur": deblur_worker.run,
    "enhance": enhance_worker.run,
    "fix_faces": facefix_worker.run,
    "metadata": metadata_worker.run,
    "upscale": superres_worker.run,
    "validate": validator_worker.run
}

WORKER_DESCRIPTIONS = {
    "colorize": "Add color to grayscale or black & white images",
    "deblur": "Fix blurry or out-of-focus images",
    "enhance": "General image quality enhancement",
    "fix_faces": "Restore and enhance faces in the image",
    "metadata": "Extract and process image metadata",
    "upscale": "Increase image resolution (super resolution)",
    "validate": "Ensure quality did not degrade after restoration",
}