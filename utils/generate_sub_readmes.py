import os
from tqdm import tqdm
from langchain_openai import ChatOpenAI
from langchain.chains import LLMChain
from langchain_core.prompts import ChatPromptTemplate
from langchain.document_loaders import PythonLoader
from langchain_core.documents import Document

# Step 1: Initialize the model
model = ChatOpenAI(model="gpt-3.5-turbo-1106", temperature=0)

# Step 2: Iterate through subfolders and process "main.py" files
current_directory = os.getcwd()



for subfolder_name in tqdm(os.listdir(current_directory), desc="Processing subfolders"):
    subfolder_path = os.path.join(current_directory, subfolder_name)
    
    # Skip if not a directory or if the directory is "files" or "venv"
    if not os.path.isdir(subfolder_path) or subfolder_name in ['timeline_generator',
                                                                'question_answering_youtube_videos',
                                                                'simple_translator',
                                                                'question_answering_database',
                                                                'nike_executive_officers_information_extraction',
                                                                'extracting_dataframe_from_paper',
                                                                'twitter_financial_news_sentiment', 'simple_calculator_tool',
                                                                'check_dataframe_quality', 'question_answering_pdf',
                                                                 'summarizing_text', 'question_answering_website', 
                                                                 'question_answering_world_bank_data', 'chatbot', 
                                                                 'conversational_website', 'npc_simulator', 'utils', 'files',
                                                                 'financial_analyser', 'question_answering_yfinance_dataframe',
                                                                 'orchestrating_summarization_using_langgraph', 'search_tavily_agent',
                                                                 'joker', 'person_information_extractor', 'venv']:
        continue

    # Ensure the "main.py" file exists in the subfolder
    main_file_path = os.path.join(subfolder_path, "main.py")
    if not os.path.exists(main_file_path):
        continue

    # Step 3: Load the content of "main.py" using PythonLoader
    loader = PythonLoader(file_path=main_file_path)
    main_docs = loader.load()

    # Step 4: Use LLM to generate a project title based on the content of main.py
    title_prompt = (
        "You are an assistant that reads Python code and generates an appropriate title for the project."
        "PLEASE DON'T MENTION THE MODEL LIKE GPT OR ETC"
        "Based on the following code, suggest a concise and descriptive title:"
        "\n\n"
        "{context}"
    )
    title_prompt_template = ChatPromptTemplate.from_template(title_prompt)
    title_chain = LLMChain(llm=model, prompt=title_prompt_template)
    title_response = title_chain.run(context=main_docs[0].page_content)
    title = title_response.strip()
    title = title.replace('"', '')
    title = title.split(":")[1] if ":" in title else title

    # Step 5: Define the system prompt for generating the documentation
    system_prompt = (
        "You are an assistant that transforms Python code into structured documentation. "
        "Use the following format to generate a README for the given code. Follow this template strictly:"
        "\n\n"
        f"# {title}\n\n"
        "## Objective\n\n"
        "## Summary of the Objective:\n\n"
        "- {{summary_1}}\n"
        "- {{summary_2}}\n\n"
        "# Flowchart\n"
        "```mermaid\n"
        "flowchart TD\n"
        "{{flowchart_nodes}}\n"
        "```"
        "Generate the README from the following Python code:"
        "{context}"
    )

    human_prompt = (
        "Please generate a README for the given Python code using the provided template."
    )

    prompt = ChatPromptTemplate(
        [
            ("system", system_prompt),
            ("human", human_prompt)
        ]
    )

    # Step 6: Create an LLMChain for generating the documentation
    documentation_chain = LLMChain(llm=model, prompt=prompt)

    # Step 7: Generate the documentation
    response = documentation_chain.run(context=main_docs[0].page_content)

    # Step 8: Write the generated README to "README.md" in the subfolder
    readme_path = os.path.join(subfolder_path, "README.md")
    with open(readme_path, "w") as readme_file:
        readme_file.write(response.strip())
