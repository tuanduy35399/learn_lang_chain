from dotenv import load_dotenv
import os
from langchain_openai import ChatOpenAI
from schema import ResearchPlan
load_dotenv()

llm =  ChatOpenAI(model=os.environ["MODEL_NAME"], 
                  base_url=os.environ["BASE_URL"],
                  temperature=0.5
                  )

