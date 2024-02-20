import streamlit as st

from ui_components import chat
from ui_components import sidebar


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
