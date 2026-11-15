from deepagents import create_deep_agent
from dotenv import load_dotenv
from phases import *
from langchain_core.runnables import RunnableLambda
from llm import llm
import asyncio
from promtps import LEADER_PROMPT
from schema import ResearchPlan
from langchain_core.output_parsers import StrOutputParser
from tools import create_report
load_dotenv()

#Lap rap cac pipeline

normalize_input= RunnableLambda(
    lambda x: {"user_question": x} if isinstance(x, str) else x
)

sub_agent_runner= RunnableLambda(func=run_agent_sync, afunc=run_agent_async)

nguoi_phan_xu = create_deep_agent(model=llm, 
                                  backend=StateBackend(),
                                  tools=[create_report],
                                  system_prompt=(
        "Bạn là Trưởng nhóm Nghiên cứu (Research Lead). Các chuyên gia đã lưu dữ liệu "
        "chi tiết vào các file `/researches/_*.md` trong hệ thống file ảo.\n"
        "1. Dùng `ls` và `read_file` để đọc nội dung chi tiết trong các file `/researches/_*.md`.\n"
        "2. Đối chiếu, loại bỏ trùng lặp và tổng hợp thành báo cáo hoàn chỉnh.\n"
        "3. Dùng tool `create_report` truyền các tham số content là nội dung báo cáo và name_file là tên chủ đề báo cáo"
        "lưu báo cáo cuối cùng vào `<ten_chu_de_bao_cao>.md` vào ổ cứng thật của máy, sau đó trả lời người dùng."
    ))


deep_research_pipeline= (
    normalize_input
    | LEADER_PROMPT
    | llm.with_structured_output(ResearchPlan) 
    | RunnableLambda(prepare_plan)
    | sub_agent_runner.map().with_config({"max_concurrency": 2}) #giam so luong agent chay song song tranh Rate limit 
    #lam cho model khong kip goi write_file
    | RunnableLambda(merge_results)
    | nguoi_phan_xu
    | RunnableLambda(extract_final_report)
)

cau_hoi= "Cho thong tin chi tiet bai hoc ve LangChain, AI Agent di"
output = asyncio.run(deep_research_pipeline.ainvoke(cau_hoi))
print(f'{'='*10}\nKET QUA CUOI CUNG\n{output}')

