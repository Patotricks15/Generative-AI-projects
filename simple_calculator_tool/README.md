# "Python Chatbot with Arithmetic Tools"

## Objective
The objective of this Python code is to create a chatbot using the langchain_openai library and implement arithmetic tools for addition and multiplication. The chatbot will be able to answer arithmetic queries using the implemented tools.

## Summary of the Objective:
- Create a chatbot using the langchain_openai library.
- Implement arithmetic tools for addition and multiplication.

# Flowchart
```mermaid
flowchart TD
A[User Query] --> B{Invoke Chatbot}
B --> |Invoke Arithmetic Tools| C{Tool Call}
C --> |Select Tool| D[Addition Tool]
C --> |Select Tool| E[Multiplication Tool]
D --> F{Invoke Addition Tool}
E --> G{Invoke Multiplication Tool}
F --> H[Tool Response]
G --> I[Tool Response]
H --> J[Chatbot Response]
I --> J
```

The README has been generated based on the provided Python code.