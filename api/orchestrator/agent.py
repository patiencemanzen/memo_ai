from typing import Dict
from openai import OpenAI
import logging
import os
from .models import OrchestrationPlan
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
# Initialize OpenAI client
# --------------------------------------------------------------
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
model = "gpt-4o-mini"

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

    def get_orchestration_plan(self) -> Dict:
        """
        Generate the orchestration plan for the image enhancement process.

        Returns:
            Dict: The orchestration plan or an error message.
        """
        try:
            return self._construct_orchestration_plan()
        except Exception as e:
            logger.error(f"Error generating orchestration plan: {e}")
            return {"error": str(e)}

    def _construct_orchestration_plan(self) -> Dict:
        """
        Construct the orchestration plan by interacting with the LLM API.

        Returns:
            Dict: The parsed orchestration plan.
        """
        metadata_str = self.metadata if self.metadata else "None"

        prompt = build_orchestration_prompt(self.image_preview_path, metadata_str)

        try:
            logger.info("Sending request to OpenAI API for orchestration plan.")
            completion = client.beta.chat.completions.parse(
                model=model,
                messages=[
                    {
                        "role": "system",
                        "content": prompt,
                    }
                ],
                response_format=OrchestrationPlan,
            )
            logger.info("Successfully received response from OpenAI API.")
            return completion.choices[0].message.parsed
        except Exception as e:
            logger.error(f"Error constructing orchestration plan: {e}")
            raise
