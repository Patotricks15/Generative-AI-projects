from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter, TokenTextSplitter
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from typing import Optional, List
from pydantic import BaseModel, Field
from langchain_community.document_loaders import PyPDFLoader
from langchain.storage import InMemoryByteStore
from langchain.retrievers.multi_vector import MultiVectorRetriever
import uuid

file_path = "/home/patrick/genai_projects/files/pdfs/414759-1-_5_Nike-NPS-Combo_Form-10-K_WR.pdf"

# Modelo e scraping
model = ChatOpenAI(model="gpt-3.5-turbo-1106")


# Read the document
loader = PyPDFLoader(file_path)

docs = loader.load() 

# Split
text_splitter = TokenTextSplitter(chunk_size=1000)

splits = text_splitter.split_documents(docs)

# Vectorstore
vectorstore = Chroma(
    collection_name="full_documents", embedding_function=OpenAIEmbeddings()
)
# The storage layer for the parent documents
store = InMemoryByteStore()
id_key = "doc_id"

# The retriever (empty to start)
retriever = MultiVectorRetriever(
    vectorstore=vectorstore,
    byte_store=store,
    id_key=id_key,
)

doc_ids = [str(uuid.uuid4()) for _ in docs]

# The splitter
child_text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000)

sub_docs = []
for i, doc in enumerate(docs):
    _id = doc_ids[i]
    _sub_docs = child_text_splitter.split_documents([doc])
    for _doc in _sub_docs:
        _doc.metadata[id_key] = _id
    sub_docs.extend(_sub_docs)

# Making the retriever
retriever.vectorstore.add_documents(sub_docs)
retriever.docstore.mset(list(zip(doc_ids, docs)))




# Class Executive

class Executive(BaseModel):
    name:Optional[str] = Field(default=None, description="The name of the executive")
    executive_job_position:Optional[str] = Field(default=None, description="The job position of the executives")
    executive_sector:Optional[str] = Field(default=None, description="The company sector/field that the executive is responsable for, inside the nike")
    age:Optional[int] = Field(default=None, description="The executive's age")
    nike_since_year:Optional[int] = Field(default=None, description="The year that the executive began to work on Nike")
    gender:Optional[str] = Field(default=None, description="The executive's gender (male or female) based on name or pronouns on the text")

class Data(BaseModel):
    """Extracted data about executives officers"""
    executives: List[Executive]

# Prompt
prompt = ChatPromptTemplate.from_messages(
[
    (
        "system",
        "You are an expert extraction algorithm. "
            "Only extract relevant information from the text. "
            "If you do not know the value of an attribute asked to extract, "
            "return null for the attribute's value.",
     ),
     ("human", "{text}"),
]
)

# Creating the chain
runnable = prompt | model.with_structured_output(schema=Data)

# Function to get relevant chunks by similarity
def get_relevant_chunks(retriever, queries: List[str]) -> List[str]:
    """
    Search the relevant chunks for each query
    """
    retrieved_texts = []
    for query in queries:
        docs = retriever.get_relevant_documents(query)
        retrieved_texts.extend([doc.page_content for doc in docs])
    return list(set(retrieved_texts))


# Queries for the Executive class
queries = [
    f"The NIKE, Inc executive's name",
    f"The NIKE, Inc executive's job position name",
    f"The NIKE, Inc executive's age",
    f"The NIKE, Inc executive's sector/field inside the nike",
    f"The NIKE, Inc executive's first date to start to work on nike",
    f"The NIKE, Inc executive's gender"
]

# Get the relevant chunks
relevant_chunks = get_relevant_chunks(retriever, queries)

# Combine the chunks in a reduced text
reduced_text = " ".join(relevant_chunks)

# Execute the model in a reduced text
result = runnable.invoke({"text": reduced_text})

print(result)
