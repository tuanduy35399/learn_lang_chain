from langchain.agents import create_agent 
from dotenv import load_dotenv
from langchain.tools import tool
from langchain_openai import ChatOpenAI
from langchain.messages import HumanMessage
from tavily import TavilyClient
from typing import Dict, Any
from pathlib import Path

load_dotenv()
tavily_client = TavilyClient()

@tool
def web_search(query: str)-> Dict[str, Any]:
    """ 
    Tool for searching the web for information
    """
    print(f"Searching for {query}")
    return tavily_client.search(query=query)

@tool
def make_report(content: str)->str:
    """
    Tool for make a report markdown
    """
    path= Path("report.md")
    path.write_text(content, encoding="utf-8")
    return f"Saved report file in {path.resolve()}"


model = ChatOpenAI(model="my_models", 
                   base_url="http://localhost:20128/v1",
                   temperature=1.0)

agent= create_agent(model=model, tools=[web_search, make_report])
for token, metadata in agent.stream(
    {
        "messages": [HumanMessage(content="Give me the lastest news of the day and make a report md")]
    },
    stream_mode="messages"
):
    if token.content:
        print(token.content, end="", flush=True)
