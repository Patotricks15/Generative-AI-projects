import yfinance as yf
from langchain_experimental.agents import create_pandas_dataframe_agent
from langchain_openai import ChatOpenAI, OpenAIEmbeddings


model = ChatOpenAI(model="gpt-3.5-turbo-1106",temperature=0)

# Define the ticker
ticker_symbol = "AAPL"

# Download the data
ticker = yf.Ticker(ticker_symbol)

# Define the period (1 year)
dados_historicos = ticker.history(period="1y")

# Define the pandas dataframe agent
agent = create_pandas_dataframe_agent(model, dados_historicos, verbose=True, allow_dangerous_code=True)

# Ask the question
print(agent.run("What is the highest closing date and its respective value?"))