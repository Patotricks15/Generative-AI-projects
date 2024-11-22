from langchain_core.messages import HumanMessage
from langchain_core.vectorstores import InMemoryVectorStore
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langgraph.checkpoint.memory import MemorySaver
from langchain.tools.retriever import create_retriever_tool
from langgraph.prebuilt import create_react_agent
from goose3 import Goose
from langchain_core.documents import Document


llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

# Getting the text from a website
g = Goose()
url_website = "https://en.wikipedia.org/wiki/Climate_change"
article = g.extract(url_website)
text = article.cleaned_text

# Put the text into a Document
doc = Document(page_content=text,
               metadata = {"source": url_website})

# Splitting the document in smaller pieces
text_splitter = RecursiveCharacterTextSplitter(chunk_size=200, chunk_overlap=200)
splits = text_splitter.split_documents([doc])

# Creating the Vectorstore
vectorstore = InMemoryVectorStore.from_documents(
    documents=splits, embedding=OpenAIEmbeddings()
)
retriever = vectorstore.as_retriever(search_type = "mmr")

# Starting memory
memory = MemorySaver()

# Building retriever tool
tool = create_retriever_tool(
    retriever,
    "wikipedia_retriever",
    "Searches and returns excerpts from the climate change wikipedia page.",
)
tools = [tool]

# Creating agent
agent_executor = create_react_agent(llm, tools, checkpointer=memory)

# The conversational
config = {"configurable": {"thread_id": "abc123"}}

query = "What is climate change? In 1 paragraph"

for event in agent_executor.stream(
    {"messages": [HumanMessage(content=query)]},
    config=config,
    stream_mode="values",
):
    event["messages"][-1].pretty_print()