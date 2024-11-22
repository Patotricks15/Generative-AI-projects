# "Financial News Sentiment Analysis with GPT-4o-mini Model"

## Objective
The objective of this code is to perform sentiment analysis on financial news using the GPT-4o-mini model. The sentiment analysis involves extracting the financial market sentiment from the given text and providing an explanation for the chosen sentiment.

## Summary of the Objective:
- Read financial news data from a CSV file.
- Preprocess the data and create maps for labels.
- Use the GPT-4o-mini model to generate sentiment analysis for the financial news.
- Measure the accuracy of the sentiment analysis and save the results to an Excel file.

# Flowchart
```mermaid
flowchart TD
start[Start] --> read_data{Read Data}
read_data --> filter_data{Filter Data}
filter_data --> create_maps{Create Maps for Labels}
create_maps --> generate_sentiment{Generate Sentiment Analysis}
generate_sentiment --> measure_accuracy{Measure Accuracy}
measure_accuracy --> save_results{Save Results to Excel}
save_results --> end[End]
```