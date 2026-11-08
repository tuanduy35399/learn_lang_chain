from langchain.agents import create_agent 
from dotenv import load_dotenv
from langchain.tools import tool
from langchain_openai import ChatOpenAI
load_dotenv()

@tool
def print_document(name: str) -> str: 
    """
    use this tool to generate th propore document for ur student
    """
    return f"this is the document of {name}"

model = ChatOpenAI(model="my_models", 
                   base_url="http://localhost:20128/v1",
                   temperature=1.0)

agent= create_agent(model=model, tools=)

