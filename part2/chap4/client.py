import os, json
from promtps import ASSISTANT_SELECTION_PROMPT, RESEARCH_REPORT_PROMPT, SUMMARY_PROMPT, WEB_SEARCH_PROMPT
from web_scrapping import web_scrape
from web_searching import web_search
from langchain_core.prompts import  PromptTemplate
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

load_dotenv()

model = ChatOpenAI(model=os.environ["MODEL_NAME"], 
                   base_url=os.environ["BASE_URL"])

# chuyen tu json sang dict cua python
def to_obj(s):
    return json.loads(s)

