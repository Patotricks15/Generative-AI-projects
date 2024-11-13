import getpass
import os
from langchain_openai import ChatOpenAI
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_core.messages import HumanMessage
from langgraph.prebuilt import create_react_agent
from dotenv import load_dotenv

# Set up
load_dotenv('.env')
model = ChatOpenAI(model="gpt-3.5-turbo-1106")

# Instance the Tavily search
search = TavilySearchResults(max_results=2)

# And put into a list of tools (we can combine with others tools)
tools = [search]

# Create the agent that will identify and use the right tool for each situation
agent_executor = create_react_agent(model, tools)

# The interaction with the agent
query = input("Tavily search:")
response = agent_executor.invoke(
    {
        "messages": [HumanMessage(content=query)
                     ]
                     }
                     )

print(response['messages'][-1].content)