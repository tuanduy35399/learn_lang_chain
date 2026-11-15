from deepagents import create_deep_agent
from dotenv import load_dotenv
from phases import *
from langchain_core.runnables import RunnableLambda
from llm import llm
import asyncio
from promtps import LEADER_PROMPT
load_dotenv()

#Lap rap cac pipeline

normalize_input= RunnableLambda(
    lambda x: {"user_question": x} if isinstance(x, str) else x
)

sub_agent_runner= RunnableLambda(func=run_agent_sync, afunc=run_agent_async)

deep_research_pipeline= (
    normalize_input
    | LEADER_PROMPT
    | llm
    | RunnableLambda(prepare_plan)
    | sub_agent_runner.map()
    | RunnableLambda(merge_results)
    | llm
    | RunnableLambda(extract_final_report)
)

cau_hoi= "Toi la sinh vien Ky thuat phan mem toi biet 1 chut ve AI Agent,finetune model LLM va YOLO lieu toi co the ung tuyen vao AI Engineer o TMA khong"
output = asyncio.run(deep_research_pipeline.ainvoke(cau_hoi))