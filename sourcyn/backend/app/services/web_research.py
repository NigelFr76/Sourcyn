import os
import httpx
from bs4 import BeautifulSoup
from typing import List, Dict, Any
from urllib.parse import urlparse

class WebSearchProvider:
    def __init__(self):
        self.searxng_url = os.getenv("SEARXNG_URL", "http://localhost:8080")

    async def search(self, query: str) -> List[dict]:
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{self.searxng_url}/search",
                    params={"q": query, "format": "json"}
                )
                response.raise_for_status()
                data = response.json()
                results = []
                for res in data.get("results", [])[:5]:
                    results.append({
                        "url": res.get("url"),
                        "title": res.get("title"),
                        "content": res.get("content")
                    })
                return results
        except Exception as e:
            print(f"SearXNG search failed: {e}")
            return []

class PageExtractionService:
    async def extract_text(self, url: str) -> str:
        # Simple extraction using httpx and BeautifulSoup
        # A full production implementation would fallback to Playwright here if needed.
        try:
            headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"}
            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.get(url, headers=headers)
                response.raise_for_status()
                soup = BeautifulSoup(response.text, "html.parser")
                # Remove scripts and styles
                for script in soup(["script", "style"]):
                    script.extract()
                text = soup.get_text(separator=" ", strip=True)
                return text[:5000] # Return first 5000 chars to avoid LLM token overflow
        except Exception as e:
            print(f"Extraction failed for {url}: {e}")
            return ""
