from langchain_experimental.agents import create_pandas_dataframe_agent
from langchain_openai import ChatOpenAI
import pandas as pd

data = pd.read_excel("/home/patrick/genai_projects/extracting_dataframe_from_paper/extracted_data/TD440/Tabela 3 – Composição dos preços dos derivados de petróleo.xlsx")
model = ChatOpenAI(model="gpt-3.5-turbo-1106", temperature=0)
agent = create_pandas_dataframe_agent(model, data, verbose=True, allow_dangerous_code=True)

print(agent.run("""Check the data quality using the following template:
                - Has null values? yes/no
                - Has wrong format columns? yes/no
                - Has wrong float separator? yes/no"""))