import os
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv


# Set up the configs
load_dotenv('.env') 
model = ChatOpenAI(model="gpt-3.5-turbo-1106")

# Instance the ChatPromptTemplate with "language" and "text" parameters
prompt_template = ChatPromptTemplate.from_messages(
    [
        ("system", "Translate the following into {language}"),
        ("user", "{text}")
    ]
)

# User input the text 
user_input = input("Text:")

# Creating the CHAIN containing prompt template and model
chain = prompt_template | model

# Getting the chain result (the model response is in content)
result = chain.invoke({"language": "portuguese",
                                 "text": user_input
}
)

print(result.content)