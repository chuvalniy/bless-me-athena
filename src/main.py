import os

import streamlit as st
from dotenv import load_dotenv
from langchain import hub
from langchain.agents import AgentExecutor
from langchain.agents.format_scratchpad import format_log_to_str
from langchain.agents.output_parsers import ReActSingleInputOutputParser
from langchain.memory import ConversationBufferMemory
from langchain.tools.render import render_text_description
from langchain_community.tools.ddg_search import DuckDuckGoSearchRun
from langchain_openai import ChatOpenAI

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_BASE_URL = os.getenv("OPENAI_BASE_URL")


def handle_user_input(prompt):
    response = st.session_state.conversation.invoke({"input": prompt})['output']
    st.markdown(response)

    st.session_state.messages.append(
        {"role": "assistant", "content": response}
    )


def get_agent():
    llm = ChatOpenAI(
        openai_api_key=OPENAI_API_KEY,
        base_url=OPENAI_BASE_URL,
        model_name='mistralai/mixtral-8x7b-instruct',
    )
    llm_with_stop = llm.bind(stop=["\nObservation"])

    tools = [DuckDuckGoSearchRun()]

    agent_prompt = hub.pull("hwchase17/react-chat")

    prompt = agent_prompt.partial(
        tools=render_text_description(tools),
        tool_names=", ".join([t.name for t in tools]),
    )

    agent = (
            {
                "input": lambda x: x["input"],
                "agent_scratchpad": lambda x: format_log_to_str(x["intermediate_steps"]),
                "chat_history": lambda x: x["chat_history"],
            }
            | prompt
            | llm_with_stop
            | ReActSingleInputOutputParser()
    )

    agent_executor = AgentExecutor(
        agent=agent,
        tools=tools,
        memory=ConversationBufferMemory(memory_key="chat_history"),
        handle_parsing_errors=True
    )

    return agent_executor


def main():
    st.title("Chat with Mixtral")

    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "assistant", "content": "How can I help you?"}
        ]

    if "conversation" not in st.session_state:
        st.session_state.conversation = get_agent()

    for message in st.session_state.messages:
        with st.chat_message(message['role']):
            st.write(message['content'])

    if prompt := st.chat_input():
        st.session_state.messages.append(
            {'role': 'user', 'content': prompt}
        )

        with st.chat_message('user'):
            st.write(prompt)
        with st.chat_message('assistant'):
            handle_user_input(prompt)


if __name__ == "__main__":
    main()
