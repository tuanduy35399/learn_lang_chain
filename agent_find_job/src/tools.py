from langchain.tools import tool
from dotenv import load_dotenv
from tavily import TavilyClient

load_dotenv()

tavi_client= TavilyClient()
@tool(description="Tìm kiếm thông tin mới nhất trên Internet theo từ khóa query.")
def research_web(query:str, max_reqsult:int):
    return tavi_client.search(query=query, 
                              max_results=max_reqsult)

