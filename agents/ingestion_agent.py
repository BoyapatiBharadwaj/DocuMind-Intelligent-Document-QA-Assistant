
import os 

class IngestionAgent:
    def __init__(self):
        self.supported_types = ['pdf', 'csv', 'docx', 'pptx', 'txt', 'md']

    def load_documents(self, file_paths):
        from langchain.document_loaders import (
            PyPDFLoader,
            CSVLoader,
            Docx2txtLoader,
            UnstructuredPowerPointLoader,
            TextLoader
        )

        documents = []
        for path in file_paths:
            ext = os.path.splitext(path)[-1].lower()
            if ext == '.pdf':
                loader = PyPDFLoader(path)
            elif ext == '.csv':
                loader = CSVLoader(path)
            elif ext == '.docx':
                loader = Docx2txtLoader(path)
            elif ext == '.pptx':
                loader = UnstructuredPowerPointLoader(path)
            elif ext in ['.txt', '.md']:
                loader = TextLoader(path)
            else:
                continue
            docs = loader.load_and_split()
            documents.extend(docs)
        return documents
