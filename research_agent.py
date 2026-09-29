import os

# Turn off CrewAI telemetry (must be set BEFORE importing crewai)
os.environ["CREWAI_DISABLE_TELEMETRY"] = "true"
os.environ["OTEL_SDK_DISABLED"] = "true"

from crewai import Agent, Task, Crew, Process, LLM
from crewai.tools import tool
from ddgs import DDGS


@tool("DuckDuckGo Search")
def duckduckgo_search(query: str) -> str:
    """Search the web with DuckDuckGo. Input: a search query string.
    Returns titles, URLs and short summaries of the top results."""
    try:
        results = DDGS().text(query, max_results=6)
    except Exception as e:
        return f"Search failed: {e}"

    if not results:
        return "No results found."

    return "\n\n".join(
        f"Title: {r['title']}\nURL: {r['href']}\nSummary: {r['body']}"
        for r in results
    )


def build_llm(api_key: str) -> LLM:
    # Groq has an OpenAI-compatible API, so we use the "openai/" provider
    # with Groq's base_url. No litellm needed.
    return LLM(
        model="openai/gpt-oss-120b",
        base_url="https://api.groq.com/openai/v1",
        api_key=api_key,
        temperature=0.3,
        max_tokens=4000,
    )


def run_research(topic: str, api_key: str) -> str:
    llm = build_llm(api_key)

    researcher = Agent(
        role="Senior Research Analyst",
        goal=f"Research '{topic}' thoroughly and write an accurate, well-structured report.",
        backstory=(
            "You are an experienced analyst who searches the web, "
            "cross-checks information, and writes clear reports with sources."
        ),
        tools=[duckduckgo_search],
        llm=llm,
        max_iter=8,
        verbose=False,
        allow_delegation=False,
    )

    task = Task(
        description=(
            f"Research the topic: {topic}\n"
            "Use the search tool several times with different queries. "
            "Then write a detailed report."
        ),
        expected_output=(
            "A markdown report with: a title, an executive summary, "
            "3-5 key sections with headings, a short conclusion, "
            "and a 'Sources' list containing the URLs you used."
        ),
        agent=researcher,
    )

    crew = Crew(
        agents=[researcher],
        tasks=[task],
        process=Process.sequential,
        verbose=False,
    )

    result = crew.kickoff()
    return result.raw
