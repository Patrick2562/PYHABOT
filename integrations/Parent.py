import math

class Parent():
    def __init__(self, type_):
        print(f"Started... with '{type_}' integration!")
    
    def splitToChunks(self, text, **kwargs):
        size   = kwargs.get("size", 2000)
        count  = math.ceil(len(text) / size)
        chunks = []
        for i in range(0, count):
            start = i * size
            end   = min(len(text), (i+1) * size)
            chunks.append(text[start:end])
        return chunks