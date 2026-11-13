from langchain_openai import ChatOpenAI
from langchain_community.document_loaders import YoutubeLoader, TextLoader, PyPDFLoader
from pathlib import Path
from pytubefix import YouTube
from langchain_core.prompts import PromptTemplate
from dotenv import load_dotenv
from langchain_core.output_parsers import StrOutputParser
import os

load_dotenv()
# save_dir = Path(__file__).resolve().parent /'youtube_source'
# save_dir.mkdir(parents=True, exist_ok=True)
urls=  ['https://www.youtube.com/watch?v=1rBkC1eB8pA']
docs=[]
for url     in urls:
    title_name= YouTube(url=url).title
    loader = YoutubeLoader.from_youtube_url(
        youtube_url=url,
        language=['vi', 'en'],
        add_video_info=False,
    )
    video_doc=loader.load()

    for i in video_doc:
        i.metadata["title"]= title_name
        i.metadata["source"]= url
    docs.extend(video_doc)

youtube_docs= "\n\n".join(
    f"#Title: {doc.metadata.get('title', 'unknown')}\n#Source: {doc.metadata.get('source', 'unknown')}"
    f"\n{doc.page_content}"
    for doc in docs)


#Luu file subtitle
# file_path= Path(__file__).resolve().parent /'youtube_source.txt'
# with open(file=file_path, mode="+a", encoding='utf-8') as file:
#     file.write(video_text)

base_dir = Path(__file__).resolve().parent
pdf_path= base_dir /'source' / 'Lionel_Messi.pdf'
text_path= base_dir /'source'/'youtube_source.txt'
pdf_doc= PyPDFLoader(str(pdf_path)).load()[:1] # lay 1 trang dau thoi
txt_doc= TextLoader(str(text_path)).load()

all_docs= pdf_doc+ txt_doc+ video_doc

model= ChatOpenAI(model=os.environ["MODEL_NAME"], 
                  base_url=os.environ["BASE_URL"])

#tom tat tung cai doc

doc_sum_template= """
Write a concise summary of the following text:
{content}
DOC SUMMARY:"""

doc_sum_prompt= PromptTemplate.from_template(doc_sum_template)

doc_sum_chain= doc_sum_prompt | model | StrOutputParser()


#refine
refine_summary_template = refine_summary_template = """
Hãy cập nhật bản tổng hợp bằng tiếng Việt từ tài liệu mới.

Yêu cầu:
- Giữ lại thông tin chính của các nguồn đã tổng hợp.
- Bổ sung các ý chính của tài liệu mới.
- Nếu tài liệu mới khác chủ đề, tạo mục riêng; không bỏ qua.
- Ghi tiêu đề và nguồn cho từng mục.
- Không tự bổ sung sự kiện hoặc số liệu ngoài tài liệu.

Bản tổng hợp hiện tại:
{current_refined_summary}

Tài liệu mới:
{content}

Bản tổng hợp cập nhật:
"""


refine_summary_prompt= PromptTemplate.from_template(refine_summary_template)

refine_summary_chain= refine_summary_prompt | model | StrOutputParser()

def refine_and_append_new(docs):
    log_steps= [] 
    #buoc tren thuc the cung khong can thiet, chu yeu de quan sat qua trinh tom tat tung buoc thoi
    current= ''
    for index, doc in enumerate(docs, start=0):
        if index== 0:
            current= doc_sum_chain.invoke({
                "content": doc.page_content,
            })
        else:
            current= refine_summary_chain.invoke({
                "current_refined_summary": current, #buoc phai khop ten voi bien truyen vao cua template
                "content": doc.page_content,
            })
        log_steps.append({
            "step": index+1,
            "source": doc.metadata.get('source', 'unknown'),
            "summary": current,
        })
        print(log_steps[-1])
    return {
        "final_summary": current,
        "log_steps": log_steps
    }
full_summary = refine_and_append_new(all_docs)
print(full_summary["final_summary"])