import os
from langchain_openai import ChatOpenAI
from langchain_core.messages import AIMessage
from langchain_core.messages import HumanMessage
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import START, MessagesState, StateGraph
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import SystemMessage, trim_messages
from typing import Sequence
from langchain_core.messages import BaseMessage
from langgraph.graph.message import add_messages
from typing_extensions import Annotated, TypedDict
from dotenv import load_dotenv

load_dotenv('.env')  # Load .env file

model = ChatOpenAI(model="gpt-3.5-turbo-1106")

# Define a new graph
workflow = StateGraph(state_schema=MessagesState)

# Create the prompt

prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are a chatbot. Answer all questions to the best of your ability",

        ),
        MessagesPlaceholder(variable_name="messages")
    ]
)

# Add the retrieval of messages
trimmer = trim_messages(
    max_tokens=65,
    strategy="last",
    token_counter=len,
    include_system=True,
    allow_partial=False,
    start_on="human",
)

messages = [SystemMessage(content="you're a good assistant"),
    HumanMessage(content="hi! My name is Patrick"),
    AIMessage(content="hi!")
]
class State(TypedDict):
  messages: Annotated[Sequence[BaseMessage], add_messages]
  language: str

# Define the function that calls the model
def call_model(state:State):
  chain = prompt | model
  trimmed_messages = trimmer.invoke(state['messages'])
  response = chain.invoke(
      {"messages":trimmed_messages}
  )
  return {"messages":[response]}

# Define the single node in the graph
workflow.add_edge(START, "model")
workflow.add_node("model", call_model)

# Adding memory
memory = MemorySaver()
app = workflow.compile(checkpointer=memory)
config={"configurable":{"thread_id":"abc123"}}

# The chatbot interaction
while True:
    query = input("Text:")
    input_messages = [HumanMessage(query)]
    output = app.invoke({"messages": input_messages}, config)
    last_ai_message = output['messages'][-1]
    last_ai_message.pretty_print()



