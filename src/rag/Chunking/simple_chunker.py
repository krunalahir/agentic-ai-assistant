from .base import BaseChunker

class SimpleChunker(BaseChunker):

    def __init__(self,chunk_size=500,overlap=100):
        self.chunk_size = chunk_size
        self.overlap = overlap

    def chunk(self,documents):
        chunks=[]
        chunk_id=1

        for doc in documents:
            start=0
            text_length = len(doc)

            while start < text_length:
                end=start+self.chunk_size
                chunk=doc[start:end]

                chunk=" ".join(chunk.split())
                chunks.append({
                    "id":chunk_id,
                    "text":chunk
                })

                chunk_id=chunk_id+1
                start=end-self.overlap

        return chunks

