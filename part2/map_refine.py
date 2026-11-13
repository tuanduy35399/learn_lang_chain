from langchain_openai import ChatOpenAI
from langchain_community.document_loaders import YoutubeLoader
from pathlib import Path
from pytubefix import YouTube
# save_dir = Path(__file__).resolve().parent /'youtube_source'
# save_dir.mkdir(parents=True, exist_ok=True)
urls=  ["https://www.youtube.com/watch?v=U3uRSCBySSo", 
        "https://www.youtube.com/watch?v=shV2704ohpc",
        ]
docs=[]
for url in urls:
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

video_text= "\n\n".join(
    f"#Title: {doc.metadata.get('title', 'unknown')}\n#Source: {doc.metadata.get('source', 'unknown')}"
    f"\n{doc.page_content}"
    for doc in docs)
print(video_text)

#Luu file subtitle
file_path= Path(__file__).resolve().parent /'youtube_source.txt'
with open(file=file_path, mode="+a", encoding='utf-8') as file:
    file.write(video_text)

