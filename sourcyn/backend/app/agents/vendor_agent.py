import json
from langchain_core.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
import os
from pydantic import BaseModel, Field
from typing import List, Optional
from sqlalchemy.orm import Session
from app.models import Vendor

class VendorProfile(BaseModel):
    vendor_id: Optional[int]
    name: str
    location: str
    certifications: List[str]
    capacity: str
    is_internal: bool

class VendorDiscoveryAgent:
    def __init__(self, db: Session):
        self.db = db
        # We can also use LLM for some fuzzy matching or reasoning later,
        # but vendor discovery primarily queries the internal DB or sets up web search.

    def discover_internal_vendors(self, category: str) -> List[dict]:
        # For a real implementation, we'd use pgvector or full-text search.
        # For now, we return all internal vendors.
        vendors = self.db.query(Vendor).filter(Vendor.is_internal == True).all()
        return [
            {
                "vendor_id": v.id,
                "name": v.name,
                "location": v.location,
                "certifications": v.certifications,
                "capacity": v.capacity,
                "is_internal": v.is_internal
            }
            for v in vendors
        ]
