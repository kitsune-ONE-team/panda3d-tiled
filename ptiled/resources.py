from pathlib import Path


def resolve(path: str | Path) -> Path:
    if isinstance(path, str):
        return Path(path)

    return path
