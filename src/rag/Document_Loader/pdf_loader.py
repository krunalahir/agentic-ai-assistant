from PyPDF2 import PdfReader
from .base import BaseLoader

class PdfLoader(BaseLoader):

    def load(self, path):
        try:
            reader = PdfReader(path)
            documents = []

            for page in reader.pages:
                text = page.extract_text()
                if text:
                    documents.append(text)

            if not documents:
                raise ValueError(f"No text extracted from PDF: {path}")

            return documents

        except FileNotFoundError:
            raise FileNotFoundError(f"PDF file not found: {path}")
        except Exception as e:
            raise RuntimeError(f"Failed to load PDF '{path}': {str(e)}")
