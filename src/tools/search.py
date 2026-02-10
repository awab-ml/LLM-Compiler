"""Search tool using Tavily API."""

import os
from typing import Optional
from langchain_core.tools import tool
from tavily import TavilyClient


@tool
def search_tool(query: str, max_results: int = 5) -> str:
    """Search the web for information using Tavily.
    
    Args:
        query: The search query string
        max_results: Maximum number of results to return (default: 5)
    
    Returns:
        A formatted string with search results
    """
    api_key = os.getenv("TAVILY_API_KEY")
    if not api_key:
        return "Error: TAVILY_API_KEY not found in environment variables"
    
    try:
        client = TavilyClient(api_key=api_key)
        response = client.search(query, max_results=max_results)
        
        if not response.get("results"):
            return f"No results found for query: {query}"
        
        # Format results
        formatted_results = []
        for i, result in enumerate(response["results"], 1):
            title = result.get("title", "No title")
            content = result.get("content", "No content")
            url = result.get("url", "")
            
            formatted_results.append(
                f"{i}. {title}\n"
                f"   {content}\n"
                f"   Source: {url}\n"
            )
        
        return "\n".join(formatted_results)
    
    except Exception as e:
        return f"Error performing search: {str(e)}"
