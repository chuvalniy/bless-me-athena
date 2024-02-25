from PyPDF2 import PdfReader
from langchain.text_splitter import CharacterTextSplitter


def parse_pdf(pdf) -> str:
    """
    Given PDF file parse it into a single python string object.
    :param pdf: PDF file.
    :return:
    """
    text = ""

    pdf_reader = PdfReader(pdf)
    for page in pdf_reader.pages:
        text += page.extract_text()

    return text


def split_text(text: str, chunk_size: int, chunk_overlap: int):
    """
    Take documents and split them into chunks
    :param text: Documents with content.
    :param chunk_size: The size of each chunk of text
    :param chunk_overlap: Overlap parameter for a chunk.
    :return:
    """
    text_splitter = CharacterTextSplitter(
        separator='\n',
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        length_function=len
    )

    chunks = text_splitter.split_text(text)
    return chunks
