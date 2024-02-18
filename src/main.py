import streamlit as st

from agent import get_agent


def init_session_state():
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "assistant", "content": "How can I help you?"}
        ]

    if "conversation" not in st.session_state:
        st.session_state.conversation = get_agent()


def handle_user_input(prompt):
    st.session_state.messages.append(
        {'role': 'user', 'content': prompt}
    )

    with st.chat_message('user'):
        st.write(prompt)
    with st.chat_message('assistant'):
        response = st.session_state.conversation.invoke({"input": prompt})['output']
        st.markdown(response)

        st.session_state.messages.append(
            {"role": "assistant", "content": response}
        )


def main():
    st.set_page_config(
        page_title="Chat with Mixtral",
        page_icon=":parrot:"
    )
    st.title("Chat with Mixtral")

    init_session_state()

    for message in st.session_state.messages:
        with st.chat_message(message['role']):
            st.write(message['content'])

    prompt = st.chat_input()
    if prompt:
        handle_user_input(prompt)


if __name__ == "__main__":
    main()
