import streamlit as st
from langchain_helper import get_llm_response, create_vector_store

st.header("I am your :blue[Personal PDF - query] :red[Assistant] :sunglasses:")

# Initialize session state variables
if "button_clicked" not in st.session_state:
    st.session_state.button_clicked = False

if "pdf_content" not in st.session_state:
    st.session_state.pdf_content = None

if "uploaded_file" not in st.session_state:
    st.session_state.uploaded_file = None

with st.sidebar:
    uploaded_file = st.file_uploader(
        label="Upload your pdf file :blue[here] ",
        accept_multiple_files=False,
        type="pdf",
    )

    if uploaded_file:
        st.session_state.uploaded_file = uploaded_file
        if st.button(label="submit"):
            st.session_state.button_clicked = True
            create_vector_store(uploaded_file)
            # st.session_state.pdf_content = extract_pdf_content(uploaded_file)
            # st.write(st.session_state.pdf_content)

if st.session_state.button_clicked and st.session_state.uploaded_file:
    st.write(
        f"Great! your uploaded pdf file is :red[{st.session_state.uploaded_file.name}]"
    )
    # Create vector store from pdf file

    usr_question = st.text_input(
        "Query your PDF file.",
        max_chars=150,
        placeholder="Type your question here...",
    )

    if usr_question:
        with st.spinner("Please wait..."):
            # st.write(st.session_state.pdf_content)
            # Uncomment the lines below to invoke the LLM chain and display the answer
            response = get_llm_response(usr_question)
            st.subheader("Answer:")
            st.write(response)
