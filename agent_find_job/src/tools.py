from langchain.tools import tool
from dotenv import load_dotenv
from tavily import TavilyClient
from pathlib import Path
load_dotenv()

tavi_client= TavilyClient()
@tool(description="Tìm kiếm thông tin mới nhất trên Internet theo từ khóa query.")
def research_web(query:str, max_reqsult:int=5):
    return tavi_client.search(query=query, 
                              max_results=max_reqsult)

@tool(description="Tao file bao cao ghi vao o dia dua tren chu de")
def create_report(content: str, name_file:str) -> str:
    file_path= Path(__file__).parent.parent
    with open(f'{file_path}/reports/{name_file}', '+a', encoding='utf-8') as file:
        file.write(content)
    return f"File duoc luu tai {file_path}/reports/{name_file}."
