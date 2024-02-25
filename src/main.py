import streamlit as st
from langchain.chains.question_answering import load_qa_chain

from data import load_vector_store, split_text, parse_pdf
from model import get_llm, get_embeddings
from ui_components import (
    init_session, handle_assistant_output, handle_user_input, display_messages, display_sidebar_header, upload_pdf
)


def main():
    st.set_page_config(page_title="Athena")

    display_sidebar_header()
    pdf = upload_pdf()

    if pdf is not None:
        # temporary for testing purposes
        if 'embeddings' not in st.session_state:
            st.session_state.embeddings = get_embeddings()

        init_session()
        display_messages()

        # TODO: model recreates text chunks, vector stores and embeddings after each prompt in a single conversation
        text = parse_pdf(pdf)
        text_chunks = split_text(text, chunk_size=3000, chunk_overlap=200)

        vector_store = load_vector_store(text_chunks, st.session_state.embeddings)

        prompt = handle_user_input()
        if prompt:
            docs = vector_store.similarity_search(prompt)

            llm = get_llm()

            chain = load_qa_chain(llm, chain_type='stuff')
            response = chain.run(input_documents=docs, question=prompt)

            handle_assistant_output(response)


if __name__ == "__main__":
    main()
