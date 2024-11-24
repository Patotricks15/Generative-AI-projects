## Objective
The objective of this code is to perform a data quality check using ChatOpenAI and Pandas DataFrame.

## Summary of the Objective:
- Read an Excel file containing data on the composition of petroleum derivatives prices.
- Use ChatOpenAI to create a Pandas DataFrame agent for checking the data quality.

# Flowchart
```mermaid
flowchart TD
A[Read Excel file] --> B[Create ChatOpenAI model]
B --> C[Create Pandas DataFrame agent]
C --> D[Check data quality using template]
```