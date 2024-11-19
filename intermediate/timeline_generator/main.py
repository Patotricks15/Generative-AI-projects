from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter, TokenTextSplitter
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from typing import Optional, List
from pydantic import BaseModel, Field
from langchain_community.document_loaders import PyPDFLoader
from langchain.storage import InMemoryByteStore
from goose3 import Goose
from langchain_core.documents import Document


model = ChatOpenAI(model="gpt-4o-mini", temperature=0)

topic_input = input("Topic:")
# Getting the text from a website
g = Goose()
url_website = f"https://en.wikipedia.org/wiki/{topic_input.replace(' ', '_')}"
article = g.extract(url_website)
text = article.cleaned_text

# Put the text into a Document
docs = [Document(page_content=text,
               metadata = {"source": url_website})
]
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000)

splits = text_splitter.split_documents(docs)
# Vectorstore

vectorstore = Chroma.from_documents(docs, embedding=OpenAIEmbeddings())

retriever = vectorstore.as_retriever()


# Class basemodel

class KeyDevelopment(BaseModel):
    f"""Information about a development in the history of {topic_input}."""

    year: int = Field(
        ..., description="The year when there was an important historic development. If the year is million or billion return the entire value with all zeros. Values before christ needs to be negative. FOrce to return an int"
    )
    description: str = Field(
        ..., description="What happened in this year? What was the development?"
    )
    evidence: str = Field(
        ...,
        description="Repeat in verbatim the sentence(s) from which the year and description information were extracted",
    )


class ExtractionData(BaseModel):
    f"""Extracted information about key developments in the history of the {topic_input}."""

    key_developments: List[KeyDevelopment]
# prompt



prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are an expert at identifying key historic development in text. "
            "Only extract important historic developments. Extract nothing if no important information can be found in the text.",
        ),
        ("human", "{text}"),
    ]
)

extractor = prompt | model.with_structured_output(
    schema=ExtractionData,
    include_raw=False,
)


extractions = extractor.batch(
    [{"text": text} for text in splits],
    {"max_concurrency": 5},  # limit the concurrency by passing max concurrency!
)

key_developments = []

for extraction in extractions:
    key_developments.extend(extraction.key_developments)

key_developments = sorted(
    filter(lambda x: x.year is not None and x.year != '-1', key_developments),
    key=lambda x: x.year
)

print(key_developments)