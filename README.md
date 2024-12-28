# Intelligent PDF Interaction Tool

## Overview
The **Intelligent PDF Interaction Tool** is an advanced application that allows users to interact with their PDF documents in an intuitive and dynamic way. The application leverages cutting-edge technologies to enable natural language-based interactions with the content of PDF files, making it easier to search, extract, and analyze information.

## Features
- **Natural Language Interaction**: Query your PDF document using natural language inputs.
- **Fast Search and Retrieval**: Efficiently retrieve relevant sections of the PDF using vector search.
- **Advanced Embedding Models**: Powered by Huggingface Embeddings and AzureOpenAI for enhanced understanding of document content.
- **User-Friendly Interface**: Built with Streamlit for an interactive and responsive user experience.
- **Scalable Storage**: Uses FAISS vector store for efficient storage and retrieval of embeddings.

## Technologies Used
- **LangChain**: For building and managing the interaction pipeline.
- **Huggingface Embeddings**: To generate semantic representations of PDF content.
- **AzureOpenAI**: For processing natural language queries and generating intelligent responses.
- **FAISS Vector Store**: For storing and searching embeddings.
- **Streamlit**: For creating a user-friendly web interface.

## How It Works
1. **PDF Upload**:
   - Users upload a PDF document via the web interface.
2. **Processing**:
   - The document is processed, and its content is embedded using Huggingface Embeddings.
   - Embeddings are stored in FAISS for efficient search and retrieval.
3. **Query Handling**:
   - Users input natural language queries via the interface.
   - The system uses AzureOpenAI to understand the query and retrieve relevant embeddings.
   - Results are displayed as answers or highlighted sections from the document.

## Installation
1. Clone the repository:
   ```bash
   git clone <repository_url>
   ```
2. Navigate to the project directory:
   ```bash
   cd intelligent-pdf-interaction-tool
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage
1. Run the Streamlit app:
   ```bash
   streamlit run app.py
   ```
2. Open the web interface in your browser.
3. Upload a PDF document and interact with it using natural language queries.

## Future Enhancements
- Add support for multilingual PDF documents.
- Implement summarization and keyword extraction features.
- Integrate additional embedding models for improved performance.
- Enhance the UI/UX with advanced visualization tools.
