from PyPDF2 import PdfReader
from .base import BaseLoader

class PdfLoader(BaseLoader):

    def load(self, path):

        reader = PdfReader(path)
        documents = []

        for page in reader.pages:
            text = page.extract_text()
            if text:
                documents.append(text)

        return documents
