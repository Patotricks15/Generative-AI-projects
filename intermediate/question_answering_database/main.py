from langchain_community.agent_toolkits import SQLDatabaseToolkit
from langgraph.prebuilt import create_react_agent
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from dotenv import load_dotenv
from langchain_community.utilities import SQLDatabase
from langchain_core.messages import SystemMessage
from langchain_core.messages import HumanMessage
from langgraph.prebuilt import create_react_agent

# Loading the environmental variables
load_dotenv('.env')

# Reading the database sql
db = SQLDatabase.from_uri("sqlite:///Chinook.db")

# Instance the model
model = ChatOpenAI(model="gpt-3.5-turbo-1106",temperature=0)

# Instance the toolkit and insert this tools into a list
toolkit = SQLDatabaseToolkit(db=db, llm = model)
tools = toolkit.get_tools()

# Writing the basic prompt
SQL_PREFIX = """You are an agent designed to interact with a SQL database.
Given an input question, create a syntactically correct SQLite query to run, then look at the results of the query and return the answer.
Unless the user specifies a specific number of examples they wish to obtain, always limit your query to at most 5 results.
You can order the results by a relevant column to return the most interesting examples in the database.
Never query for all the columns from a specific table, only ask for the relevant columns given the question.
You have access to tools for interacting with the database.
Only use the below tools. Only use the information returned by the below tools to construct your final answer.
You MUST double check your query before executing it. If you get an error while executing a query, rewrite the query and try again.

DO NOT make any DML statements (INSERT, UPDATE, DELETE, DROP etc.) to the database.

To start you should ALWAYS look at the tables in the database to see what you can query.
Do NOT skip this step.
Then you should query the schema of the most relevant tables."""

system_message = SystemMessage(content=SQL_PREFIX)

# Creating the agent
agent_executor = create_react_agent(model, tools, messages_modifier=system_message)

# Develop the chat
while True:
    query = input("Text:")
    for s in agent_executor.stream(
        {"messages": [HumanMessage(content=query)]}
    ):
        print(s[list(s.keys())[0]]['messages'][-1].content)
        print("----")