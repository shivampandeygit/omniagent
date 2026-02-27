import requests
from rich.console import Console

console = Console()

class WebSearchTool:
    def __init__(self):
        self.name = "web_search"
        self.description = "Search the internet for any information"
    
    def run(self, query: str, max_results: int = 5) -> str:
        console.print(f"[dim]🔍 Searching: {query}[/dim]")
        
        try:
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
            }
            
            # Wikipedia API for factual queries
            wiki_url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{requests.utils.quote(query.replace(' ', '_'))}"
            wiki_response = requests.get(wiki_url, headers=headers, timeout=10)
            
            results = []
            
            if wiki_response.status_code == 200:
                wiki_data = wiki_response.json()
                if wiki_data.get("extract"):
                    results.append(f"📖 Wikipedia:\n{wiki_data['extract']}\n")

            # DuckDuckGo Instant Answer
            ddg_url = f"https://api.duckduckgo.com/?q={requests.utils.quote(query)}&format=json&no_html=1"
            ddg_response = requests.get(ddg_url, headers=headers, timeout=10)
            ddg_data = ddg_response.json()
            
            if ddg_data.get("Abstract"):
                results.append(f"🔍 DuckDuckGo:\n{ddg_data['Abstract']}\nURL: {ddg_data.get('AbstractURL', '')}\n")
            
            for topic in ddg_data.get("RelatedTopics", [])[:3]:
                if "Text" in topic:
                    results.append(f"• {topic['Text']}\n  {topic.get('FirstURL', '')}")

            if not results:
                return f"No detailed results found for '{query}'. Please try a more specific query."
            
            return f"Search results for: '{query}'\n\n" + "\n".join(results)
            
        except Exception as e:
            return f"Search failed: {str(e)}"