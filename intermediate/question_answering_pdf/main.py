from langchain_community.document_loaders import PyPDFLoader
from langchain_core.vectorstores import InMemoryVectorStore
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import ChatOpenAI
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate

file_path = "/home/patrick/genai_projects/files/pdfs/414759-1-_5_Nike-NPS-Combo_Form-10-K_WR.pdf"

loader = PyPDFLoader(file_path)

docs = loader.load()

model = ChatOpenAI(model="gpt-3.5-turbo-1106")

text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000)

splits = text_splitter.split_documents(docs)

vectorstore = InMemoryVectorStore.from_documents(
    documents=splits,
    embedding=OpenAIEmbeddings()
)

retriever = vectorstore.as_retriever()

system_prompt = (
    "You are an assistant for question-answering tasks. "
    "Use the following pieces of retrieved context to answer "
    "the question. If you don't know the answer, say that you "
    "don't know. Use three sentences maximum and keep the "
    "answer concise."
    "\n\n"
    "{context}"
)

prompt = ChatPromptTemplate(
    [
        ("system", system_prompt),
        ("human","{input}")
    ]
)

question_answer_chain = create_stuff_documents_chain(model, prompt)
rag_chain = create_retrieval_chain(retriever, question_answer_chain)

#results = rag_chain.invoke({"input": "what was nike's revenue in 2023?"})

results = rag_chain.invoke({"input": "How about competitors?"})

print(results['answer'])
