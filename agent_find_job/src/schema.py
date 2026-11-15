from pydantic import BaseModel, Field


#phan nay cho LeaderPlan doc thoi nen khong can original quesion va output file o Sub Agent 
class Sub_Agent(BaseModel):
    #viet description de LLM doc 
    agent_id: str = Field(description="ID cua sub-agent, Ex: sub_agent_1")
    role: str = Field(description="Vai tro chuyen gia duoc chi dinh")
    sub_query: str= Field(description="Cau hoi con can tim/ nghien cuu day du ngu canh")

class ResearchPlan(BaseModel):
    original_quesion: str
    analysis: str
    sub_tasks: list[Sub_Agent]

