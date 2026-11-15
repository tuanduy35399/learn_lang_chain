from schema import Sub_Agent, ResearchPlan
from promtps import SUBAGENT_RESEARCH_PROMPT, LEADER_PROMPT
from deepagents import create_deep_agent
from llm import llm
from deepagents.backends import StateBackend
from tools import research_web
from langchain.messages import HumanMessage
#buoc chuan bi plan 
def prepare_plan(planner: ResearchPlan) -> list[dict]: #tra ve danh sach dict chua cac sub_tasks cho SubAgent
    return [
        {
            # lay 1 phan tu lop cha
            "agent_id":task.agent_id,
            "role":task.role,
            "sub_query": task.sub_query,
            "original_question":planner.original_question,
            #de Python tao them
            "output_file": f"/researches/{task.agent_id}.md"
        }
        for task in planner.sub_tasks
    ] 

# tao 1 con agent

def build_agent(task: dict):
    print(f"func build_agent: Dang xay dung agent {task['agent_id']}...")
    formatted_prompt_sub_agent =SUBAGENT_RESEARCH_PROMPT.format(
        role= task["role"], 
        sub_query= task["sub_query"],
        original_question=task["original_question"],
        output_file= task["output_file"]
    )
    agent= create_deep_agent(model=llm, 
                             backend=StateBackend(),
                             tools=[research_web], 
                             system_prompt=formatted_prompt_sub_agent)

    print(f"Xay dung xong agent {task['agent_id']}")
    agent_input= {
        "messages": [HumanMessage(content= task["sub_query"])]
    }
    
    return agent, agent_input
def run_agent_sync(task: dict) ->dict:
    
    agent, agent_input= build_agent(task)
    
    print(f"[{task["agent_id"]}] | Dang tien hanh nghien cuu: {task["sub_query"]}")
    result= agent.invoke(agent_input)
    print(f"[{task['agent_id']}] | Hoan thanh cong viec!!")
    return {
            "agent_id":task["agent_id"],
            # "role":task["role"],
            # "sub_query": task["sub_query"],
            "original_question":task["original_question"],
            "summary": result["messages"][-1].content,
            "files": result.get("files", {})
    }

async def run_agent_async(task: dict) ->dict:
    
    agent, agent_input= build_agent(task)
    print(f"[{task["agent_id"]}] | Dang tien hanh nghien cuu: {task["sub_query"]}")
    result= await agent.ainvoke(agent_input)
    print(f"[{task['agent_id']}] | Hoan thanh cong viec!!")
    return {
            "agent_id":task["agent_id"],
            # "role":task["role"],
            # "sub_query": task["sub_query"],
            "original_question":task["original_question"],
            "summary": result["messages"][-1].content,
            "files": result.get("files", {})
    }

#gop ket qua lai
def merge_results(sub_results: list[dict]) -> dict:
    print("Dang tong hop du lieu tu cac sub_agent...")
    shared_files= {}
    summaries= []
    original_question= sub_results[0]["original_question"] 
    #sub_results[0] lay 1 cai tu phan dau duoc roi tai may cai kia y chang nhau
    for res in sub_results:
        shared_files.update(res["files"])
        summaries.append(f"### Bao cao tu {res['agent_id']}\nNoi dung: {res["summary"]}")
        print(f"### Bao cao tu {res['agent_id']}\nNoi dung: {res["summary"]}")
    
    return {
        "messages": [HumanMessage(content=f"Cau hoi goc: {original_question}\nKet qua tu cac sub{summaries}")],
        "files": shared_files,
    }


#tao file bao cao cuoi cung
def extract_final_report(result: dict):
    files = result.get("files", {})
    # print(f'Ham extract final report {files}')
    # Ưu tiên lấy nội dung từ file ảo /final_report.md nếu agent đã gọi write_file
    if "final_report.md" in files:
        file_data = files["final_report.md"]
        # Tùy phiên bản deepagents, content có thể là str hoặc list các dòng
        content = file_data["content"] if isinstance(file_data, dict) else file_data
        if isinstance(content, list):
            content = "\n".join(content)
    else:
        # Dự phòng: lấy tin nhắn trả lời cuối cùng của agent
        content = result["messages"][-1].content

    return content

