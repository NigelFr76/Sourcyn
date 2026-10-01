import json
from langchain_core.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
import os
from pydantic import BaseModel, Field
from typing import List, Optional

# Set up Langchain model abstraction
def get_llm():
    model_name = os.getenv("GEMINI_MODEL", "gemini-1.5-pro")
    api_key = os.getenv("GEMINI_API_KEY", "")
    return ChatGoogleGenerativeAI(model=model_name, google_api_key=api_key)

class RequirementItem(BaseModel):
    criterion: str = Field(description="The feature or requirement category, e.g., Processor, RAM")
    requirement: str = Field(description="The actual requirement value, e.g., Intel i7 or equivalent")
    mandatory: bool = Field(description="Whether this is a mandatory requirement")

class StructuredRequirements(BaseModel):
    product_category: str = Field(description="The general category of the product, e.g., Business Laptop")
    quantity: int = Field(description="The number of units requested")
    requirements: List[RequirementItem] = Field(description="List of specific requirements")
    budget: float = Field(description="The total budget. If not given, use 0.0")
    currency: str = Field(description="Currency code, e.g. USD, INR")
    max_delivery_days: Optional[int] = Field(description="Maximum number of days for delivery")

class RequirementAnalysisAgent:
    def __init__(self):
        self.llm = get_llm()
    
    def analyze(self, natural_language_request: str) -> dict:
        prompt = PromptTemplate.from_template(
            "Extract structured procurement requirements from the following natural language request.\n"
            "Request: {request}\n"
            "Return JSON matching the required schema. Ensure you classify mandatory vs optional correctly."
        )
        # We will use structured output parsing
        structured_llm = self.llm.with_structured_output(StructuredRequirements)
        chain = prompt | structured_llm
        
        result = chain.invoke({"request": natural_language_request})
        return result.model_dump()
