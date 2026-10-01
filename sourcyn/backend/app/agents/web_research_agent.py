from langchain_core.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from pydantic import BaseModel, Field
from typing import List, Optional
import os
from app.services.web_research import WebSearchProvider, PageExtractionService
from app.models import WebResearchResult
from sqlalchemy.orm import Session
from datetime import datetime

class ExtractedFact(BaseModel):
    fact: str
    confidence: str = Field(description="HIGH, MEDIUM, or LOW")

class WebEvidence(BaseModel):
    summary: str
    facts: List[ExtractedFact]
    source_type: str = Field(description="e.g. Vendor Website, Retailer, Public Database, News, Other Public Source")

def get_llm():
    model_name = os.getenv("GEMINI_MODEL", "gemini-1.5-pro")
    api_key = os.getenv("GEMINI_API_KEY", "")
    return ChatGoogleGenerativeAI(model=model_name, google_api_key=api_key)

class WebResearchAgent:
    def __init__(self, db: Session):
        self.db = db
        self.search_provider = WebSearchProvider()
        self.extractor = PageExtractionService()
        self.llm = get_llm()

    async def run_research(self, procurement_id: int, query: str):
        # 1. Search the web
        results = await self.search_provider.search(query)
        
        prompt = PromptTemplate.from_template(
            "Extract structured evidence from the following web page content related to the query: '{query}'.\n"
            "URL: {url}\n"
            "Title: {title}\n"
            "Content:\n{content}\n"
            "Do not hallucinate. If no relevant info is found, return empty facts."
        )
        structured_llm = self.llm.with_structured_output(WebEvidence)
        chain = prompt | structured_llm

        for res in results:
            url = res["url"]
            title = res["title"]
            # 2. Extract page text
            page_text = await self.extractor.extract_text(url)
            if not page_text:
                continue
            
            # 3. Analyze with LLM
            try:
                evidence = await chain.ainvoke({"query": query, "url": url, "title": title, "content": page_text})
                
                # 4. Save to DB
                db_record = WebResearchResult(
                    procurement_request_id=procurement_id,
                    search_query=query,
                    url=url,
                    title=title,
                    source_type=evidence.source_type,
                    extracted_information=evidence.model_dump(),
                    status="SUCCESS",
                    retrieved_at=datetime.utcnow()
                )
                self.db.add(db_record)
            except Exception as e:
                db_record = WebResearchResult(
                    procurement_request_id=procurement_id,
                    search_query=query,
                    url=url,
                    title=title,
                    source_type="UNKNOWN",
                    extracted_information={"error": str(e)},
                    status="FAILED",
                    retrieved_at=datetime.utcnow()
                )
                self.db.add(db_record)
                
        self.db.commit()
