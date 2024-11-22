from langchain_community.document_loaders import WebBaseLoader, PyPDFLoader
from langchain_openai import ChatOpenAI
from langchain import hub


model = ChatOpenAI(model="gpt-3.5-turbo-1106")

# Reading the website
loader = WebBaseLoader("https://blog.langchain.dev/how-to-safely-query-enterprise-data-with-langchain-agents-sql-openai-gretel/")
docs = loader.load()
content = docs[0].page_content

prompt = hub.pull("whiteforest/chain-of-density-prompt")# The chain
chain = prompt | model

# invoke chain
result = chain.invoke({"content":content,
                       "content_category":"Technical blog post",
                       "max_words":2000,
                       "iterations":5,
                       "entity_range":4})

print(result)

