# Text Extraction and Structured Information Retrieval for Wikipedia Person Profiles

## Objective
The objective of this code is to extract relevant information from Wikipedia person profiles and retrieve structured information such as the person's name, birth year, and height in meters.

## Summary of the Objective:
- Extract relevant information from Wikipedia person profiles.
- Retrieve structured information such as the person's name, birth year, and height in meters.

## Medium tutorial:
[Click here](https://patotricks15.medium.com/generative-ai-project-extracting-personalinformation-from-wikipedia-using-langchain-9dceefddedfe)

# Flowchart
```mermaid
flowchart TD
A[Input Person] --> B[Extract Wikipedia URL]
B --> C[Extract Text from URL]
C --> D[Split Text into Chunks]
D --> E[Create Vectorstore]
E --> F[Retrieve Relevant Chunks]
F --> G[Combine Chunks]
G --> H[Execute Model with Reduced Text]
H --> I[Output Structured Information]
```
