from pydantic import BaseModel, Field
from typing import List, Optional

class RestorationStep(BaseModel):
    name: str = Field(..., description="Name of the enhancement step")
    reason: Optional[str] = Field(None, description="Why this step was chosen")

class OrchestrationPlan(BaseModel):
    steps: List[RestorationStep] = Field(..., description="Ordered steps to be applied on the image restoration")
    explanation: str = Field(..., description="AI explanation of image quality and steps")
    historian_review_required: Optional[bool] = Field(default=False, description="Flag for manual historian review")
