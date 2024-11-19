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
from goose3 import Goose
from langchain_core.documents import Document
from typing import Optional, List
from pydantic import BaseModel, Field


# Modelo e scraping
model = ChatOpenAI(model="gpt-3.5-turbo-1106")
g = Goose()

person = input("Person:")
url = f"https://en.wikipedia.org/wiki/{person.replace(' ', '_')}"
article = g.extract(url)

text = article.cleaned_text
doc = Document(page_content=text, metadate={"search": url})

# Divisão do texto em chunks
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000)
splits = text_splitter.split_documents([doc])

# Criação do vetorstore
vectorstore = Chroma.from_documents(splits, embedding=OpenAIEmbeddings())
retriever = vectorstore.as_retriever(search_type="similarity")


# Classe de saída
class Person(BaseModel):
    name: Optional[str] = Field(default=None, description="The name of the person")
    born_at: Optional[str] = Field(default=None, description="The year when the person was born")
    height_in_meters: Optional[str] = Field(default=None, description="Height measured in meters")


# Prompt para extração
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

runnable = prompt | model.with_structured_output(schema=Person)

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
    f"Information about the name of {person}",
    f"Year when {person} was born",
    f"Height in meters of {person}",
]

# Buscar os chunks relevantes
relevant_chunks = get_relevant_chunks(retriever, queries)

# Combinar os chunks em um texto reduzido
reduced_text = " ".join(relevant_chunks)

# Executar o modelo com o texto reduzido
result = runnable.invoke({"text": reduced_text})

print(result)
