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
            "agent_id":task["agent_id"],
            "role":task["role"],
            "sub_query": task["sub_query"],
            "original_question":planner.original_quesion,
            #de Python tao them
            "output_file": f"/researches/{task.agent_id}.md"
        }
        for task in planner.sub_tasks
    ] 

# tao 1 con agent

def build_agent(task: dict):
    print("func build_agent: Dang xay dung agent...")
    formatted_prompt_sub_agent =SUBAGENT_RESEARCH_PROMPT.format(
        role= task.role, 
        sub_question= task.sub_query,
        original_quesion=task.original_question,
        output_file= task.output_file
    )
    agent= create_deep_agent(model=llm, 
                             backend=StateBackend(),
                             tools=[research_web], 
                             system_prompt=formatted_prompt_sub_agent)


    agent_input= {
        "messages": [HumanMessage(content= task.sub_query)]
    }
    return agent, agent_input
def run_agent_sync(task: dict) ->dict:
    print(f"[{task.agent_id}] | Dang tien hanh nghien cuu: {task.sub_query}")
    agent, agent_input= build_agent(task)
    result= agent.ainvoke(agent_input)
    print(f"[{task.agent_id}] | Hoan thanh cong viec!!")
    return {
            "agent_id":task["agent_id"],
            # "role":task["role"],
            # "sub_query": task["sub_query"],
            "original_question":task["original_quesion"],
            "summary": result["messages"][-1].content,
            "files": result.get("files", {})
    }

async def run_agent_async(task: dict) ->dict:
    print(f"[{task.agent_id}] | Dang tien hanh nghien cuu: {task.sub_query}")
    agent, agent_input= build_agent(task)
    result= await agent.ainvoke(agent_input)
    print(f"[{task.agent_id}] | Hoan thanh cong viec!!")
    return {
            "agent_id":task["agent_id"],
            # "role":task["role"],
            # "sub_query": task["sub_query"],
            "original_question":task["original_quesion"],
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
def extract_final_report(final_state: dict) -> dict:
    files = final_state.get("files", {})
    if "/final_report.md" in files:
        report = "\n".join(files["/final_report.md"]["content"])
    else:
        report = final_state["messages"][-1].content

    return {
        "report": report,
        "virtual_files": list(files.keys()),
        "raw_files": files,
    }


