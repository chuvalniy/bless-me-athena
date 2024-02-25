import os

from dotenv import load_dotenv
from g4f import Provider, models
from langchain_community.embeddings.sentence_transformer import SentenceTransformerEmbeddings

from model.llm import G4FLLM
from langchain.llms.base import LLM

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_BASE_URL = os.getenv("OPENAI_BASE_URL")

os.environ['LANGCHAIN_API_KEY'] = os.getenv('LANGCHAIN_API_KEY')
os.environ['LANGCHAIN_TRACING_V2'] = os.getenv('LANGCHAIN_TRACING_V2')
os.environ['LANGCHAIN_PROJECT'] = os.getenv('LANGCHAIN_PROJECT')


def get_llm() -> LLM:
    """
    Create and return an instance of LLM.
    :return: LLM.
    """
    llm = G4FLLM(
        model=models.gpt_35_turbo,
        provider=Provider.Aura,
    )
    return llm


def get_embeddings() -> SentenceTransformerEmbeddings:
    """
    Create and return an instance of vector embeddings.
    :return: Embeddings.
    """
    embeddings = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")
    return embeddings
