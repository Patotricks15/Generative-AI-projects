from dotenv import load_dotenv
import bs4
from langchain import hub
from langchain_chroma import Chroma
from langchain_community.document_loaders import WebBaseLoader
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
import os
from langchain_openai import ChatOpenAI
from langchain_ollama import OllamaEmbeddings
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate

# Set up
load_dotenv('.env')
model = ChatOpenAI(model="gpt-3.5-turbo-1106")


from goose3 import Goose
from langchain_core.documents import Document

g = Goose()
url_website = "https://en.wikipedia.org/wiki/Climate_change"
article = g.extract(url_website)
text = article.cleaned_text

# Put the text into a Document
doc = Document(page_content=text,
               metadata = {"source": url_website})

# Splitting the document in smaller pieces
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
splits = text_splitter.split_documents([doc])

# Creating the Vectorstore
vectorstore = Chroma.from_documents(splits,
                                    OpenAIEmbeddings())

# Retrieve and generate a response

retriever = vectorstore.as_retriever(search_type="similarity",
                                     search_kwargs={"k": 2}
                                     )


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

query = input("Text:")
response = rag_chain.invoke({"input": query})
print(response["answer"])

# Getting the context
for document in response["context"]:
    print(document)
    print()