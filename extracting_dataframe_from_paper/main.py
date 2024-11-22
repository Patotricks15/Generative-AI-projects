from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from typing import Optional, List
from pydantic import BaseModel, Field
from langchain_community.document_loaders import PyPDFLoader
import pandas as pd
from io import StringIO
from langchain_experimental.text_splitter import SemanticChunker
import os
from tqdm import tqdm

# Set up the model
model = ChatOpenAI(model="gpt-4o-mini", temperature=0)

# Read the pdf
path_file = "/home/patrick/genai_projects/files/pdfs/TD440.pdf"
pdf_file = path_file.split("/")[-1].split(".pdf")[0]
loader = PyPDFLoader(path_file)
docs = loader.load()

# Text split
text_splitter = SemanticChunker(OpenAIEmbeddings())
splits = text_splitter.split_documents(docs)

# Vectorstore
vectorstore = Chroma.from_documents(docs, embedding=OpenAIEmbeddings())
retriever = vectorstore.as_retriever()

# Class Table BaseModel
class Table(BaseModel):
    """The table on text"""
    table_name: str = Field(..., description="The name of the table")
    table_description: Optional[str] = Field(
        ..., description="What's the description of the table? Usually appears after the table name"
    )
    table: str = Field(..., description="Return the table as a pandas DataFrame")

class ExtractionTable(BaseModel):
    """Extracted tables present on the text"""
    tables: List[Table]

# Prompt
prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are an expert at identifying tables on text. DO NOT extract images or informations in images"
            "Only extract tables. Extract nothing if no important information can be found in the text.",
        ),
        ("human", "{text}"),
    ]
)

extractor = prompt | model.with_structured_output(
    schema=ExtractionTable,
    include_raw=False,
)

# Extractor
extractions = extractor.batch(
    [{"text": text} for text in splits],
    {"max_concurrency": 5},  # limit the concurrency by passing max concurrency!
)

tables = []

# Creating the new directory to save tables
new_directory_path = os.path.join("/home/patrick/genai_projects/extracting_dataframe_from_paper/extracted_data", pdf_file)
os.makedirs(new_directory_path, exist_ok=True)

# Table -> dataframe -> excel
for extraction in tqdm(extractions, desc="Extracting tables"):  # Iterate over the extracted tables list
    tables.extend(extraction.tables)  # Collect all the extracted tables
    # Converter a tabela Markdown para DataFrame
    if len(extraction.tables) > 0:
        print(f"Table name: {extraction.tables[0].table_name}")
        df = pd.read_csv(StringIO(extraction.tables[0].table), sep="|", engine="python")
        df = df.iloc[:, 1:-1]  # Remove extra columns made by delimiters "|"
        df.columns = df.columns.str.strip()  # Clean the blank spaces on header
        df = df.applymap(lambda x: x.strip() if isinstance(x, str) else x)  # Clean blank spaces on cells
        df.to_excel(f"{new_directory_path}/{extraction.tables[0].table_name}.xlsx") # Save as excel
        print(df)