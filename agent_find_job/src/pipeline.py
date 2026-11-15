from deepagents import create_deep_agent
from dotenv import load_dotenv
from phases import *
from langchain_core.runnables import RunnableLambda
from llm import llm
import asyncio
from promtps import LEADER_PROMPT
from schema import ResearchPlan
load_dotenv()

#Lap rap cac pipeline

normalize_input= RunnableLambda(
    lambda x: {"user_question": x} if isinstance(x, str) else x
)

sub_agent_runner= RunnableLambda(func=run_agent_sync, afunc=run_agent_async)

nguoi_phan_xu = create_deep_agent(model=llm, 
                                  backend=StateBackend(),
                                  system_prompt=(
        "Bạn là Trưởng nhóm Nghiên cứu (Research Lead). Các chuyên gia đã lưu dữ liệu "
        "chi tiết vào các file `/research_*.md` trong hệ thống file ảo.\n"
        "1. Dùng `ls` và `read_file` để đọc nội dung chi tiết trong các file `/research_*.md`.\n"
        "2. Đối chiếu, loại bỏ trùng lặp và tổng hợp thành báo cáo hoàn chỉnh.\n"
        "3. Dùng `write_file` lưu báo cáo cuối cùng vào `/final_report.md`, sau đó trả lời người dùng."
    ))


deep_research_pipeline= (
    normalize_input
    | LEADER_PROMPT
    | llm.with_structured_output(ResearchPlan)
    | RunnableLambda(prepare_plan)
    | sub_agent_runner.map()
    | RunnableLambda(merge_results)
    | nguoi_phan_xu
    | RunnableLambda(extract_final_report)
)

cau_hoi= "Toi la sinh vien Ky thuat phan mem toi biet 1 chut ve AI Agent,finetune model LLM va YOLO lieu toi co the ung tuyen vao AI Engineer o TMA khong"
output = asyncio.run(deep_research_pipeline.ainvoke(cau_hoi))

