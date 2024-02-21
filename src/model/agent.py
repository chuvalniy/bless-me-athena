import os

from dotenv import load_dotenv
from langchain import hub
from langchain.agents import AgentExecutor
from langchain.agents.format_scratchpad import format_log_to_str
from langchain.agents.output_parsers import ReActSingleInputOutputParser
from langchain.memory import ConversationBufferMemory
from langchain.tools.render import render_text_description
from langchain_community.tools.ddg_search import DuckDuckGoSearchRun
from langchain_community.tools.arxiv.tool import ArxivQueryRun
from model.llm import G4F

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_BASE_URL = os.getenv("OPENAI_BASE_URL")

os.environ['LANGCHAIN_API_KEY'] = os.getenv('LANGCHAIN_API_KEY')
os.environ['LANGCHAIN_TRACING_V2'] = os.getenv('LANGCHAIN_TRACING_V2')
os.environ['LANGCHAIN_PROJECT'] = os.getenv('LANGCHAIN_PROJECT')


def _get_llm():
    llm = G4F()
    llm_with_stop = llm.bind(stop=["\nObservation"])

    return llm_with_stop


def _get_prompt(tools):
    # optimize due to very high cost
    agent_prompt = hub.pull("hwchase17/react-chat")

    prompt = agent_prompt.partial(
        tools=render_text_description(tools),
        tool_names=", ".join([t.name for t in tools]),
    )

    return prompt


def get_agent():
    tools = [
        DuckDuckGoSearchRun(),
        ArxivQueryRun()
    ]

    llm = _get_llm()
    prompt = _get_prompt(tools)

    agent = (
            {
                "input": lambda x: x["input"],
                "agent_scratchpad": lambda x: format_log_to_str(x["intermediate_steps"]),
                "chat_history": lambda x: x["chat_history"],
            }
            | prompt
            | llm
            | ReActSingleInputOutputParser()
    )

    agent_executor = AgentExecutor(
        agent=agent,
        tools=tools,
        memory=ConversationBufferMemory(memory_key="chat_history", max_token_limit=5000),  # optimize
        handle_parsing_errors=True,
    )

    return agent_executor
