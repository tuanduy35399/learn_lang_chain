from dotenv import load_dotenv
from langchain_openai.chat_models import ChatOpenAI
from langchain.agents import create_agent
from langchain.messages import HumanMessage


load_dotenv()

model = ChatOpenAI(model="my_models", 
                   base_url="http://localhost:20128/v1",
                   temperature=1.0
                   )

agent = create_agent(model=model)



response = agent.invoke(
        {   
            "messages": [HumanMessage(content="Thu do cua Viet Nam?")]
        }
)

print(response["messages"][0])
print(response["messages"][1])
print(response["messages"][-1].content)