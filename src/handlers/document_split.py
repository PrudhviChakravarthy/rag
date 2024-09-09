import os
from langchain.document_loaders import PyPDFLoader
from langchain.document_loaders import UnstructuredWordDocumentLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter

class DocumentProcessor:
    def __init__(self, file_path):
        self.file_path = file_path

    def load(self):
        # Determine file type and load the document accordingly
        ext = os.path.splitext(self.file_path)[1].lower()
        if ext == ".pdf":
            return self._load_pdf()
        elif ext == ".docx":
            return self._load_docx()
        else:
            raise ValueError(f"Unsupported file format: {ext}")
        
    def _load_pdf(self):
        loader = PyPDFLoader(self.file_path)
        return loader.load()

    def _load_docx(self):
        loader = UnstructuredWordDocumentLoader(self.file_path)
        return loader.load()

    def split_text(self, chunk_size, chunk_overlap):
        file = self.load()
        splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
        return splitter.split_documents(file)
    
