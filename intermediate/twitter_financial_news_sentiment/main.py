from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from pydantic import BaseModel, Field
import pandas as pd
from sklearn.metrics import accuracy_score
import time


start_time = time.time()

# Reading the data
df = pd.read_csv("hf://datasets/zeroshot/twitter-financial-news-sentiment/sent_train.csv")

# Filtering to reduce the execution time
df = df[:1000]

# Creating the maps for labels
sentiments = {
    0: "bearish", 
    1: "bullish", 
    2: "neutral"
}
reverse_sentiments = {v: k for k, v in sentiments.items()}


df['numeric_label'] = df['label']

df['label'] = df['numeric_label'].map(sentiments)

# The prompt to generate the sentiment
tagging_prompt = ChatPromptTemplate.from_template(
    """
Extract the desired information from the following passage.

Only extract the properties mentioned in the 'Classification' function.

Passage:
{input}
"""
)

# Creating the Classification Extractor
class Classification(BaseModel):
    sentiment: str = Field(default = None, description = "The financial market sentiment of the text", enum=["bearish", "bullish", "neutral"])
    explanation: str = Field(default = None, description = "The explanation about the choosen sentiment")

# Define the model
model = ChatOpenAI(temperature=0, model="gpt-4o-mini").with_structured_output(Classification)

# Define the chain
tagging_chain = tagging_prompt | model

# Define the function to generate the classification
def generate_classification(x):
    return tagging_chain.invoke({"input":x})

# Apply the function, extracting the sentiment and explanation
df['result'] = df['text'].apply(lambda x: generate_classification(x))
df['predicted'] = df['result'].apply(lambda x: x.sentiment)
df['numeric_predicted'] = df['predicted'].map(reverse_sentiments)
df['explanation'] = df['result'].apply(lambda x: x.explanation)

# Save as excel
df.to_excel("/home/patrick/genai_projects/intermediate/twitter_financial_news_sentiment/output.xlsx")

# Measuring accuracy score
df = df.dropna(subset=['numeric_label', 'numeric_predicted'])

accuracy = accuracy_score(df['numeric_label'], df['numeric_predicted'])

print(f"Accuracy: {accuracy}")

end_time = time.time()

# Measuring the execution time
execution_time = end_time - start_time
print(f"Execution time: {execution_time:.6f} seconds")