import os
from langchain_openai import AzureChatOpenAI
from langchain.prompts import ChatPromptTemplate, PromptTemplate
from langchain.embeddings.huggingface import HuggingFaceEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_core.output_parsers import StrOutputParser
from langchain.schema import Document

from dotenv import load_dotenv

import fitz


# Setting/loading the environment variables
load_dotenv()

AZURE_OPENAI_API_KEY = os.getenv("AZURE_OPENAI_API_KEY")
AZURE_OPENAI_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT")
OPENAI_API_VERSION = os.getenv("OPENAI_API_VERSION")


def create_chat_model():
    # Defining LLM
    chatmodel = AzureChatOpenAI(
        azure_deployment="gpt_turbo_16",
        azure_endpoint=AZURE_OPENAI_ENDPOINT,
        api_key=AZURE_OPENAI_API_KEY,
        api_version=OPENAI_API_VERSION,
        temperature=0.6,
    )
    return chatmodel


def generate_chat_template():
    # Defining the template for model to understand it's role.
    # template = ChatPromptTemplate.from_messages(
    #     [
    #         (
    #             "system",
    #             "You are an helpful AI assistant that can answer user questions.",
    #         ),
    #         ("human", "How are you?"),
    #         ("ai", "I'm doing well, thanks!"),
    #         ("human", "Questions: {question}"),
    #     ]
    # )

    template = PromptTemplate(
        input_variables=["context", "question"],
        template="Answer the user question based on following context. Do not hallucinate, if you could not find the answer in the context, tell the user that you do not know. provide the answers in pointers or paragraphs that is easy to read. Also, provide sub-headers and bolden text wherever necessary. \n\n context: {context} \n\n question: {question}",
    )

    return template


def invoke_llm_chain(question, context):

    chat_template = generate_chat_template()
    chat_model = create_chat_model()
    output_parser = StrOutputParser()
    llm_chain = chat_template | chat_model | output_parser

    response = llm_chain.invoke({"context": context, "question": question})

    return response


def extract_pdf_content(uploaded_file):
    doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")
    text = ""
    for page in doc:
        text += page.get_text()
    return text


def create_vector_store(pdf_file):
    pdf_content = extract_pdf_content(pdf_file)
    # Split the text into smaller chunks using RecursiveCharacterTextSplitter
    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=50)
    text_chunks = splitter.split_text(pdf_content)

    # Embed the text chunks using Hugging Face embeddings
    # model_name = "sentence-transformers/all-MiniLM-L6-v2"
    embedding_model = HuggingFaceEmbeddings()
    text_embeddings = embedding_model.embed_documents(text_chunks)

    # Create Document objects
    documents = [Document(page_content=chunk) for chunk in text_chunks]
    # Store the embeddings in a vector store using LangChain
    vector_store = FAISS.from_embeddings(
        text_embeddings=zip(text_chunks, text_embeddings),
        embedding=embedding_model,
        metadatas=[doc.metadata for doc in documents],
    )
    # Save the vector store to a directory
    vector_store.save_local("./temp_dir/faiss_index")
    print("Vector store created and stored in local drive 'temp_dir'.")
    return None


def get_llm_response(usr_question):

    # Load the vector store from the directory
    vector_store = FAISS.load_local(
        "./temp_dir/faiss_index",
        embeddings=HuggingFaceEmbeddings(),
        allow_dangerous_deserialization=True,
    )

    # Get the query and find the similar content from vector db

    context_docs = vector_store.similarity_search(usr_question, k=10)
    context = ""
    for doc in context_docs:
        context += doc.page_content + "\n"

    result = invoke_llm_chain(usr_question, context)

    return result
