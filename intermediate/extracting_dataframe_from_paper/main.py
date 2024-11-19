from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from typing import Optional, List
from pydantic import BaseModel, Field
from langchain_community.document_loaders import PyPDFLoader
import pandas as pd
from io import StringIO
from langchain_experimental.text_splitter import RecursiveCharacterTextSplitter, SemanticChunker
import os

# Configuração do modelo e carregamento do PDF
model = ChatOpenAI(model="gpt-4o-mini", temperature=0)
path_file = "/home/patrick/genai_projects/files/pdfs/2411.11059v1.pdf"
pdf_file = path_file.split("/")[-1].split(".pdf")[0]
loader = PyPDFLoader(path_file)
docs = loader.load()
text_splitter = SemanticChunker(OpenAIEmbeddings())

splits = text_splitter.split_documents(docs)

# Vectorstore
vectorstore = Chroma.from_documents(docs, embedding=OpenAIEmbeddings())
retriever = vectorstore.as_retriever()

# Classes BaseModel
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

# Configuração do prompt
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

# Execução do extrator
extractions = extractor.batch(
    [{"text": text} for text in splits],
    {"max_concurrency": 5},  # limit the concurrency by passing max concurrency!
)

# Processar tabelas extraídas
tables = []

# Caminho completo do novo diretório
new_directory_path = os.path.join("/home/patrick/genai_projects/intermediate/extracting_dataframe_from_paper/extracted_data", pdf_file)

# Criar o novo diretório
os.makedirs(new_directory_path, exist_ok=True)

for extraction in extractions:  # Itera sobre a lista de ExtractionTable
    tables.extend(extraction.tables)  # Coleta todas as tabelas extraídas
    # Converter a tabela Markdown para DataFrame
    if len(extraction.tables) > 0:
        df = pd.read_csv(StringIO(extraction.tables[0].table), sep="|", engine="python")
        df = df.iloc[:, 1:-1]  # Remover colunas extras criadas pelos delimitadores "|"
        df.columns = df.columns.str.strip()  # Limpar espaços em branco nos cabeçalhos
        df = df.applymap(lambda x: x.strip() if isinstance(x, str) else x)  # Limpar espaços extras nas células

        # # Adicionar colunas extras com metadados
        # df["Table Name"] = extraction.table_name
        # df["Table Description"] = extraction.table_description
        df.to_excel(f"{new_directory_path}/{extraction.tables[0].table_name}.xlsx")
        print(df)