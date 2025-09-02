
import os, requests
from typing import List

def web_search(query: str, k: int = 4) -> List[str]:
    """
    Tries Serper.dev or Bing Web Search if API keys are present.
    Returns a list of result URLs (strings). Silent fallback to [] if not configured.
    """
    urls = []
    # Serper.dev
    serper_key = os.getenv("SERPER_API_KEY")
    if serper_key:
        try:
            resp = requests.post("https://google.serper.dev/search",
                                 headers={"X-API-KEY": serper_key, "Content-Type":"application/json"},
                                 json={"q": query, "num": k})
            data = resp.json()
            for item in (data.get("organic", []) or [])[:k]:
                link = item.get("link")
                if link: urls.append(link)
        except Exception:
            pass
    # Bing
    bing_key = os.getenv("BING_SEARCH_V7_KEY")
    if bing_key and len(urls) < k:
        try:
            resp = requests.get("https://api.bing.microsoft.com/v7.0/search",
                                headers={"Ocp-Apim-Subscription-Key": bing_key},
                                params={"q": query, "count": k})
            data = resp.json()
            for item in (data.get("webPages", {}).get("value", []) or [])[:k-len(urls)]:
                link = item.get("url")
                if link: urls.append(link)
        except Exception:
            pass
    return urls
