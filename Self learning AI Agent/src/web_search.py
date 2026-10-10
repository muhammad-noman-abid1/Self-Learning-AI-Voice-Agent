import os

from dotenv import load_dotenv
from tavily import TavilyClient


load_dotenv()


tavily_client = TavilyClient(
    api_key=os.getenv("TAVILY_API_KEY")
)


def search_web(query: str) -> dict:
    """
    Search the web and return both:
    1. information for the AI
    2. source information for the user
    """

    response = tavily_client.search(
        query=query,
        search_depth="basic",
        max_results=3,
    )

    results = response.get("results", [])

    if not results:
        return {
            "context": "No useful web results were found.",
            "sources": [],
        }

    formatted_results = []
    sources = []

    for result in results:

        title = result.get("title", "Untitled")
        content = result.get("content", "")
        url = result.get("url", "")

        # Keep web content small.
        content = content[:1000]

        formatted_results.append(
            f"Title: {title}\n"
            f"Content: {content}\n"
            f"URL: {url}"
        )

        sources.append(
            {
                "title": title,
                "url": url,
            }
        )

    return {
        "context": "\n\n".join(formatted_results),
        "sources": sources,
    }