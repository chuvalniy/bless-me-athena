import streamlit as st

from model import get_agent


def init_session():
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "assistant", "content": "How can I help you?"}
        ]

    if "conversation" not in st.session_state:
        st.session_state.conversation = get_agent()


def display_messages():
    for message in st.session_state.messages:
        with st.chat_message(message['role']):
            st.write(message['content'])


def handle_user_input():
    prompt = st.chat_input()
    if prompt:
        st.session_state.messages.append(
            {'role': 'user', 'content': prompt}
        )
        with st.chat_message('user'):
            st.write(prompt)

    return prompt


def handle_assistant_output(prompt):
    if st.session_state.messages[-1]["role"] != "assistant":
        with st.chat_message('assistant'):
            with st.spinner("Thinking..."):
                response = st.session_state.conversation.invoke({"input": prompt})['output']
                st.markdown(response)

                st.session_state.messages.append(
                    {"role": "assistant", "content": response}
                )


def chat():
    init_session()
    display_messages()
    prompt = handle_user_input()  # optimize
    handle_assistant_output(prompt)  # optimize
