import math

class Integration():
    name = None

    def __init__(self, name):
        self.name = name
        print(f"Started... with '{name}' integration!")
    
    def splitToChunks(self, text, size=2000):
        count  = math.ceil(len(text) / size)
        chunks = []

        for i in range(0, count):
            start = i * size
            end   = min(len(text), (i+1) * size)

            chunks.append(text[start:end])
        
        return chunks
