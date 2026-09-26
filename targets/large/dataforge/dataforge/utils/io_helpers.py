import os

def ensure_dir(path: str) -> None:
    os.makedirs(path, exist_ok=True)

def file_exists(path: str) -> bool:
    return os.path.isfile(path)

def read_text(path: str, encoding: str = "utf-8") -> str:
    with open(path, "r", encoding=encoding) as f:
        return f.read()

def write_text(path: str, content: str, encoding: str = "utf-8") -> None:
    with open(path, "w", encoding=encoding) as f:
        f.write(content)
