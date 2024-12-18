from langchain.chains import create_citation_fuzzy_match_chain
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain.document_loaders import PyPDFLoader
from langchain_core.vectorstores import InMemoryVectorStore
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.prompts import ChatPromptTemplate
from typing import Optional, List
from pydantic import BaseModel, Field
from dotenv import load_dotenv
import os

loader = PyPDFLoader("/home/patrick/genai_projects/files/pdfs/CV_Patrick_Gomes_de_Oliveira.pdf")

docs = loader.load()

text_split = RecursiveCharacterTextSplitter(chunk_size=1000)

splits = text_split.split_documents(docs)

vectorstore = InMemoryVectorStore.from_documents(
    documents=splits,
    embedding=OpenAIEmbeddings()
)
retriever = vectorstore.as_retriever(search_type="similarity")
model = ChatOpenAI(model="gpt-3.5-turbo-1106")


class Candidate(BaseModel):
    name: str = Field(default=None, description="The name of the candidate")
    role: str = Field(default=None, description="The main job role of the candidate")
    years_of_experience: int = Field(default=None, description="Total candidate's years of experience")
    bachelor_degree: Optional[str] = Field(default=None, description="The candidate's bachelor degree")
    years_of_experience_python: int = Field(default=None, description="The candidate's years of experience working with python")
    github_url: Optional[str] = Field(default=None, description="The candidate's github url")
    linkedin_url: Optional[str] = Field(default=None, description="The candidate's linkedin url")
    years_of_experience_machine_learning_projects: int = Field(default=None, description="The candidate's years of experience working on machine learning projects")
    quantity_companies_worked_on: int = Field(default=None, description="The candidate's quantity of companies that worked on")


# Prompt para extração
prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are an expert extraction algorithm. "
            "You need to extract information from a candidate's cv"
            "Only extract relevant information from the text. "
            "If you do not know the value of an attribute asked to extract, "
            "return null for the attribute's value.",
        ),
        ("human", "{text}"),
    ]
)

runnable = prompt | model.with_structured_output(schema=Candidate)

# Função para buscar por similaridade para cada atributo
def get_relevant_chunks(retriever, queries: List[str]) -> List[str]:
    """
    Busca os chunks relevantes para cada consulta fornecida.
    """
    retrieved_texts = []
    for query in queries:
        docs = retriever.get_relevant_documents(query)
        retrieved_texts.extend([doc.page_content for doc in docs])
    # Remover duplicatas e combinar os chunks
    return list(set(retrieved_texts))


# Consultas específicas para os campos da classe Person
queries = [
    f"The name of the candidate",
    f"The main job role of the candidate",
    f"Total candidate's years of experience",
    "The candidate's bachelor degree",
    "The candidate's years of experience working with python",
    "The candidate's github url",
   "The candidate's linkedin url",
    "The candidate's years of experience working on machine learning projects"
]

# Buscar os chunks relevantes
relevant_chunks = get_relevant_chunks(retriever, queries)

# Combinar os chunks em um texto reduzido
reduced_text = " ".join(relevant_chunks)

# Executar o modelo com o texto reduzido
result = runnable.invoke({"text": reduced_text})

print(result)