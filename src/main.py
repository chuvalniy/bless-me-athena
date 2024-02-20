import streamlit as st

from src.ui_components import chat, sidebar


def set_page():
    st.set_page_config(
        page_title="Chat with Mixtral",
        page_icon=":parrot:"
    )


def main():
    set_page()
    sidebar()
    chat()


if __name__ == "__main__":
    main()
