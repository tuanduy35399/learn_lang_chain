from dotenv import load_dotenv
from langchain_openai.chat_models import ChatOpenAI
from langchain.agents import create_agent
from langchain.messages import HumanMessage, AIMessage


load_dotenv()

model = ChatOpenAI(model="my_models", 
                   base_url="http://localhost:20128/v1",
                   temperature=1.0
                   )

agent = create_agent(model=model)

for token, metadata in agent.stream(
    {
        "messages":[HumanMessage(content="Mien Tay Viet Nam co mon nao lam tu ca loc")]
    },
    stream_mode="messages"
):
    if token.content:
        print(token.content,end="", flush=True)


print("")

# response = agent.invoke(
#         {   
#             "messages": [HumanMessage(content="Thu do cua Viet Nam?"),
#                          AIMessage(content= "Thu do cua Viet Nam la **Ha Noi**"), 
#                          HumanMessage(content="Vay thu do cua Ha Noi nam o mien nao cua Viet Nam, noi chi tiet hon ve Ha Noi di")]
#         }
# )

# print(response["messages"][0])
# print(response["messages"][1])
# print(response["messages"][-1].content)