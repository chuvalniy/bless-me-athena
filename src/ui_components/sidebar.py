from typing import Optional

import streamlit as st
from streamlit.runtime.uploaded_file_manager import UploadedFile


def display_sidebar_header():
    """
    Display sidebar
    :return:
    """
    with st.sidebar:
        st.title(":tropical_drink: Chat with PDF")


def upload_pdf() -> Optional[UploadedFile]:
    """
    Upload PDF in the user interface.
    :return: PDF file.
    """
    pdf = st.sidebar.file_uploader("Upload PDF", type='pdf')
    return pdf
