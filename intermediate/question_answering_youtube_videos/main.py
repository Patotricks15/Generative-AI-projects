from langchain_community.document_loaders import YoutubeLoader
import datetime
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api._errors import NoTranscriptFound
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.docstore.document import Document
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI, OpenAIEmbeddings

model = ChatOpenAI(model="gpt-3.5-turbo-1106")

class Youtube:
    def __init__(self, url):
        self.url = url
        self.video_id = self.url.split("v=")[1] if "watch" in self.url else self.url.split('/')[-1].split('?')[0]
        
    def extract_text(self):
        self.text = ''
        dict_transcrition = YouTubeTranscriptApi.get_transcript(self.video_id, languages=['en'])
        for dict in dict_transcrition:
            self.text += '' + dict['text']
        return self.text
    
urls = [
    "https://www.youtube.com/watch?v=HAn9vnJy6S4",
    "https://www.youtube.com/watch?v=dA1cHGACXCo",
    "https://youtu.be/PHe0bXAIuk0?si=qos_bkwWa-aehTH_",
    # "https://www.youtube.com/watch?v=ZcEMLz27sL4",
    # "https://www.youtube.com/watch?v=hvAPnpSfSGo",
    # "https://www.youtube.com/watch?v=EhlPDL4QrWY",
    # "https://www.youtube.com/watch?v=mmBo8nlu2j0",
    # "https://www.youtube.com/watch?v=rQdibOsL1ps",
    # "https://www.youtube.com/watch?v=28lC4fqukoc",
    # "https://www.youtube.com/watch?v=es-9MgxB-uc",
    # "https://www.youtube.com/watch?v=wLRHwKuKvOE",
    # "https://www.youtube.com/watch?v=ObIltMaRJvY",
    # "https://www.youtube.com/watch?v=DjuXACWYkkU",
    # "https://www.youtube.com/watch?v=o7C9ld6Ln-M",
]

docs = []
for url in urls:
    extracted_text = Youtube(url=url).extract_text()
    doc = Document(page_content=extracted_text, metadata={"source": url})
    docs.append(doc)

text_splitter = RecursiveCharacterTextSplitter(chunk_size=2000)
chunked_docs = text_splitter.split_documents(docs)
embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
vectorstore = Chroma.from_documents(
    chunked_docs,
    embeddings,
)

#search_results = vectorstore.similarity_search("how do economics works?")

retriever = vectorstore.as_retriever(search_type="similarity",
                                     search_kwargs={"k":2})

#######################
system_prompt = (
    "You are an assistant for question-answering tasks. "
    "Use the following pieces of retrieved context to answer "
    "the question. If you don't know the answer, say that you "
    "don't know. Use three sentences maximum and keep the "
    "answer concise."
    "\n\n"
    "{context}"
)

prompt = ChatPromptTemplate.from_messages(
    [
        ("system", system_prompt),
        ("human", "{input}"),
    ]
)


question_answer_chain = create_stuff_documents_chain(model, prompt)
rag_chain = create_retrieval_chain(retriever, question_answer_chain)

query = input("Text:") # How do economics works? OR How do I build a RAG?
response = rag_chain.invoke({"input": query})
print(response["answer"])