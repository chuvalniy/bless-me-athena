import streamlit as st


def init_session():
    """
    Initialize session state.
    :return: None
    """
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "assistant", "content": "How can I help you?"}
        ]

    # TODO: may be redundant
    if "conversation" not in st.session_state:
        st.session_state.conversation = None


def display_messages():
    """
    Display messages from session state.
    :return:
    """
    for message in st.session_state.messages:
        with st.chat_message(message['role']):
            st.write(message['content'])


def handle_user_input() -> str:
    """
    Take user input, store in the session state and write it.
    :return: User input.
    """
    prompt = st.chat_input()
    if prompt:
        st.session_state.messages.append(
            {'role': 'user', 'content': prompt}
        )
        with st.chat_message('user'):
            st.write(prompt)

    return prompt


def handle_assistant_output(response: str):
    """
    Display LLM response.
    :param response: LLM response for user's prompt.
    :return:
    """
    if st.session_state.messages[-1]["role"] != "assistant":
        with st.chat_message('assistant'):
            st.markdown(response)
            st.session_state.messages.append({"role": "assistant", "content": response})
