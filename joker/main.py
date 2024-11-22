import os
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv


# Set up the configs
load_dotenv('.env')
model = ChatOpenAI(model="gpt-3.5-turbo-1106")

# Instance the ChatPromptTemplate with "topic" parameter
prompt_template = ChatPromptTemplate.from_messages(
    [
        ("system", "Create a joke about the topic below"),
        ("user", "{topic}")
    ]
)

# User input the text 
user_input = input("Topic:")

# Creating the CHAIN containing prompt template and model
chain = prompt_template | model

# Getting the chain result (the model response is in content)
result = chain.invoke({"topic": user_input
}
)

print(result.content)