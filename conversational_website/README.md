# Climate Change Wikipedia Chatbot

## Objective
The objective of this code is to create a chatbot that retrieves information from the Wikipedia page on climate change and provides conversational responses to user queries.

## Summary of the Objective:
- Extract text from the Wikipedia page on climate change.
- Split the text into smaller pieces for processing.

# Flowchart
```mermaid
flowchart TD
A[Extract text from Wikipedia] --> B[Create Document]
B --> C[Split Document]
C --> D[Create Vectorstore]
D --> E[Create Retriever]
E --> F[Start Memory]
F --> G[Build Retriever Tool]
G --> H[Create Agent]
H --> I[Conversational Query]
I --> J[Provide Response]
```