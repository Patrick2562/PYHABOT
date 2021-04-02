import json
import os

class DataBank():
    data = False

    def __init__(self, raw):
        if raw:
            self.data = json.loads(raw)

    def get(self, key, default=False):
        return self.data[key] if (self.data and key and self.data[key]) else default

def save(file, data, tojson=False):
    try:
        if not os.path.exists("./databank"):
            os.makedirs("./databank")

        f = open(f"./databank/{file}", "w+")
        f.write(json.dumps(data, indent=4, sort_keys=True) if tojson else data)
        f.close()
        return True

    except Exception as err:
        print(f'Exception: {err}')
    
    return False

def load(file, isjson=False):
    try:
        if not os.path.exists("./databank"):
            os.makedirs("./databank")

        if os.path.exists("./databank"):
            f = open(f"./databank/{file}", "r")
            data = f.read()
            f.close()
            return DataBank(data) if isjson else data
        
    except Exception as err:
        print(f'Exception: {err}')

    return DataBank(False) if isjson else False