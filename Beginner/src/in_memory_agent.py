from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain_openai import ChatOpenAI
from langchain.messages import HumanMessage
from langgraph.checkpoint.memory import InMemorySaver

load_dotenv()


model = ChatOpenAI(model="my_models", base_url="http://localhost:20128/v1", temperature=1.0)

agent =create_agent(model=model, checkpointer=InMemorySaver())

config={
    "configurable": {"thread_id": 1},
}


response = agent.invoke(
    {
        "messages": [HumanMessage(content="Cau thu yeu thich cua toi la Messi, toi khong thich Ronaldo (CR7)")]
    }, config=config
)

print("---------First Chat-----------")
print(response["messages"][-1].content)

response = agent.invoke(
    {
        "messages": [HumanMessage(content="Toi thich cau thu nao, ghet cau thu nao ban co nho khong")]
    },config=config
)
print("---------Second Chat-----------")
print(response["messages"][-1].content)
