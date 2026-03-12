from abc import ABC, abstractmethod

class VectorStore(ABC):

    @abstractmethod
    def add(self,embedding,text):
        pass

    @abstractmethod
    def search(self,query_embedding,k=3):
        pass