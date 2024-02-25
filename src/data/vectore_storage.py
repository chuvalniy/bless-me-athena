from langchain_community.vectorstores import Chroma


def load_vector_store(text_chunks, embeddings):
    """
    Create an instance of vector store and return it.
    :param text_chunks: Chunks of text.
    :param embeddings: Vector representations of tokens.
    :return:
    """
    vector_store = Chroma.from_texts(text_chunks, embeddings)
    return vector_store
