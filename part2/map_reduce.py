from langchain_openai import ChatOpenAI
from langchain_text_splitters import TokenTextSplitter
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableLambda, RunnableParallel
from dotenv import load_dotenv
import os
from pathlib import Path
load_dotenv()
model= ChatOpenAI(model=os.environ["MODEL_NAME"],
                  base_url=os.environ["BASE_URL"])
# respone = model.invoke("Xin chao ban")
# print(respone.content)

# split: tach large doc thanh cac doc_chunk
text_chunks_chain= (
    RunnableLambda(lambda x:[
        {
            'chunk':text_chunk,
        } for text_chunk in TokenTextSplitter(chunk_size= 3000, chunk_overlap= 100).split_text(x)
    ])
)

#map dung RunnableParallel

summarize_chunk_prompt_template= """
Write a concise summary of the following text, and include the main details.
Text: {chunk}
"""

summarize_chunk_prompt= PromptTemplate.from_template(template=summarize_chunk_prompt_template)
summarize_chunk_chain= summarize_chunk_prompt | model #buoc nay can goi model de tom tat cac chunk

summarize_map_chain= (
    RunnableParallel(
        {# chen cai summarize_chunk_chain vo day, khi goi model tra ve raw tring thi lay content cua no bang StrOutputParser()
            'summary': summarize_chunk_chain  | StrOutputParser()
        }
    )
)

#reduce: gom may cai chunk_sum lai thanh final sum

make_final_sum_prompt_template= """
Write a concise summary of the following text, 
which joins several summaries, and include the main details.
Final Sum: {final_sum}
"""
make_final_sum_prompt = PromptTemplate.from_template(template=make_final_sum_prompt_template)
make_final_reduce_chain= (
    RunnableLambda(lambda x:{'final_sum': '\n'.join([i['summary'] for i in x])}) 
    | make_final_sum_prompt 
    | model 
    | StrOutputParser()
)

split_map_reduce_chain= (
    text_chunks_chain | summarize_map_chain.map() | make_final_reduce_chain
)
file_path= Path(__file__).resolve().parent / "Moby-Dick.txt"
with open(file_path, 'r', encoding='utf-8') as file:
    moby_file = file.read()

summary= split_map_reduce_chain.invoke(moby_file)
print(summary)