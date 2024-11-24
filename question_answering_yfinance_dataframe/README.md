# Stock Data Analysis with Chatbot Integration

## Objective
The objective of this code is to perform stock data analysis using the yfinance library and integrate a chatbot to interact with the user for querying the data.

## Summary of the Objective:
- Download stock data using the yfinance library for a specified ticker symbol.
- Create a pandas dataframe from the downloaded stock data.
- Integrate a chatbot to interact with the user and query the stock data.

# Flowchart
```mermaid
flowchart TD
A[Define the ticker] --> B[Download the data]
B --> C[Define the period (1 year)]
C --> D[Define the pandas dataframe agent]
D --> E[Ask the question]
```

The flowchart illustrates the process of defining the ticker, downloading the data, defining the period, creating the pandas dataframe agent, and asking the question to interact with the chatbot.