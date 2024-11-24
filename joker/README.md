# Interactive Joke Generator with OpenAI Language Model

## Objective
The objective of this code is to create an interactive joke generator using the OpenAI language model. The program takes a user input topic and generates a joke based on that topic.

## Summary of the Objective:
- Set up the configurations for the OpenAI language model.
- Create a prompt template for generating jokes based on user input topics.
- Take user input for the topic.
- Use the prompt template and the language model to generate a joke based on the user input topic.

# Flowchart
```mermaid
flowchart TD
A[Set up the configs] --> B[Instance the ChatPromptTemplate with "topic" parameter]
B --> C[User input the text]
C --> D[Creating the CHAIN containing prompt template and model]
D --> E[Getting the chain result]
E --> F[Print the model response]
```