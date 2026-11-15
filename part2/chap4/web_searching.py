# from langchain_community.utilities import  BingSearchAPIWrapper
from typing import List
from tavily import TavilyClient
from dotenv import load_dotenv

load_dotenv()
client = TavilyClient()
def web_search(web_query: str, num_result:int) -> List[dict]:
    respone= client.search(query=web_query,max_results=num_result)
    return [{
        "title": element["title"],
        "link": element["url"],
        "content": element["content"]
    } for element in respone["results"]]

respone = web_search("How many titles did Michael Jordan win?", 2)



