import streamlit as st

from model import get_agent


def reset_session():
    st.session_state.messages = [
        {"role": "assistant", "content": "How can I help you?"}
    ]

    st.session_state.conversation = get_agent(st.session_state.options)


def sidebar():
    with st.sidebar:
        st.title(":tropical_drink: Chat with Mixtral")
        st.markdown(
            "Mixtral is a new large language model developed by Mistral AI, a French artificial intelligence company.")

    st.session_state.options = st.sidebar.multiselect(
        'Select tools to use',
        ['DuckDuckGo', 'arXiv'],
        ['DuckDuckGo'])

    st.sidebar.button("Clear chat history", on_click=reset_session, use_container_width=True)
