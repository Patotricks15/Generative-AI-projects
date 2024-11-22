import wbdata
import pandas as pd
from datetime import datetime
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_experimental.agents import create_pandas_dataframe_agent

# Define the indicator, countries, and time period
indicators = {"SP.POP.TOTL": "Total population"}  # Population indicator
countries = ["BRA", "USA"]  # Brazil and the United States
start_date = datetime(2000, 1, 1)
end_date = datetime(2022, 1, 1)

model = ChatOpenAI(model="gpt-3.5-turbo-1106", temperature=0)

# Retrieve the data
data = wbdata.get_dataframe(indicators=indicators, 
                            country=countries, 
                            date=(start_date, end_date))

agent = create_pandas_dataframe_agent(model, data, verbose=True, allow_dangerous_code=True)

# Display the data
print(data)
print(agent.run("What's the country with the highest population? Give me a complete sentence with numbers"))