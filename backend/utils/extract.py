from io import BytesIO
from PyPDF2 import PdfReader
from langchain.text_splitter import RecursiveCharacterTextSplitter

def extract_doc_meta_from_pdf(file_data: BytesIO):
    pdfreader = PdfReader(file_data)
    documents = []
    metadatas = []
    
    for page_number, page in enumerate(pdfreader.pages, start=1):
        content = page.extract_text()
        if content:
            text_splitter = RecursiveCharacterTextSplitter(
                chunk_size=800,
                chunk_overlap=200,
                add_start_index=True
            )
            page_chunks = text_splitter.split_text(content)
            
            for text in page_chunks:
                documents.append(text)
                metadatas.append({"page_number": page_number})
    
    return documents, metadatas