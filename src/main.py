import os

import streamlit as st
from dotenv import load_dotenv
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory
from langchain_openai import ChatOpenAI

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_BASE_URL = os.getenv("OPENAI_BASE_URL")


def handle_user_input(prompt):
    response = st.session_state.conversation.predict(input=prompt)
    st.markdown(response)
    st.session_state.messages.append({'role': 'assistant', 'content': response})


def get_chain():
    llm = ChatOpenAI(
        openai_api_key=OPENAI_API_KEY,
        base_url=OPENAI_BASE_URL,
        model_name='mistralai/mixtral-8x7b-instruct',
    )
    conversation = ConversationChain(
        llm=llm,
        memory=ConversationBufferMemory(),
    )

    return conversation


def main():
    st.title("Chat with Mixtral")

    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "assistant", "content": "How can I help you?"}
        ]
    if "conversation" not in st.session_state:
        st.session_state.conversation = get_chain()

    for message in st.session_state.messages:
        with st.chat_message(message['role']):
            st.write(message['content'])

    if prompt := st.chat_input():
        st.session_state.messages.append({'role': 'user', 'content': prompt})

        with st.chat_message('user'):
            st.write(prompt)
        with st.chat_message('assistant'):
            handle_user_input(prompt)


if __name__ == "__main__":
    main()
