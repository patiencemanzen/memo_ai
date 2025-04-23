import json
import logging
from typing import Dict

from .LlmClient import Client as LangClient
from .models import OrchestrationPlan, RestorationStep
from .prompt_builder import build_orchestration_prompt

# --------------------------------------------------------------
# Initialize logging
# --------------------------------------------------------------

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)

# --------------------------------------------------------------
# Image Orchestration Agent
# --------------------------------------------------------------

class OrchestrationAgent:
    def __init__(self, image_preview_path: str, metadata: dict = None):
        """
        Initialize the OrchestrationAgent with the image path and metadata.
        """
        self.image_preview_path = image_preview_path
        self.metadata = metadata or {}

    def analyze(self) -> Dict:
        """
        Generate the orchestration plan for the image enhancement process.

        Returns:
            Dict: The orchestration plan or error message.
        """
        try:
            return self._construct_orchestration_plan()
        except Exception as e:
            logger.error(f"Orchestration Error: {e}")
            raise ValueError(f"Orchestration Error: {e}")

    def _construct_orchestration_plan(self) -> Dict:
        """
        Construct the orchestration plan by interacting with Gemini API.

        Returns:
            Dict: The parsed orchestration plan.
        """
        metadata_str = str(self.metadata or "None")

        prompt = build_orchestration_prompt(
            image_preview_path=self.image_preview_path,
            metadata=metadata_str,
        )

        logger.info("Sending request to Gemini API for orchestration plan.")

        try:
            client = LangClient()

            parsed_json = client.generate_response(
                prompt=prompt,
                file_path=self.image_preview_path,
            )

            if not isinstance(parsed_json, dict):
                logger.error("Parsed JSON is not a dictionary.")
                raise ValueError("Parsed JSON is not a dictionary.")

            plan = OrchestrationPlan(**parsed_json)
            return plan.model_dump()
        except Exception as e:
            logger.error(f"Failed to parse orchestration response: {e}")
            raise ValueError(f"Failed to parse orchestration response: {e}")
