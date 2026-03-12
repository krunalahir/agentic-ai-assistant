from .base import BaseLoader

class TxTLoader(BaseLoader):

    def load(self,path):
        with open(path,"r",encoding="utf-8") as f:
            return [f.read()]