from pathlib import Path

def load_spec(path):
    return Path(path).read_text()
