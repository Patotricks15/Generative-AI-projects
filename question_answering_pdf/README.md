# AI-Powered Question Answering System for Nike's Financial Reports

## Objective
The objective of this AI-powered system is to use language processing and AI models to answer questions related to Nike's financial reports.

## Summary of the Objective:
- Use PyPDFLoader to load Nike's financial reports in PDF format.
- Split the documents into chunks, create a retrieval chain, and use an AI model to answer questions related to Nike's financial data.

# Flowchart
```mermaid
flowchart TD
subgraph langchain_community
    subgraph document_loaders
        PyPDFLoader
    end
end
subgraph langchain_core
    subgraph vectorstores
        InMemoryVectorStore
    end
    subgraph prompts
        ChatPromptTemplate
    end
end
subgraph langchain_openai
    OpenAIEmbeddings
    ChatOpenAI
end
subgraph langchain_text_splitters
    RecursiveCharacterTextSplitter
end
subgraph langchain.chains
    create_retrieval_chain
    combine_documents_chain
end
PyPDFLoader --> InMemoryVectorStore
RecursiveCharacterTextSplitter --> InMemoryVectorStore
InMemoryVectorStore --> create_retrieval_chain
ChatOpenAI --> create_stuff_documents_chain
ChatPromptTemplate --> create_stuff_documents_chain
create_retrieval_chain --> create_stuff_documents_chain
```