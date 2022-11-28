from typing import Any, List


def chunker(list: List[Any], chunk_size: int):
    """
    Iterate over a list in chunks

    Args:
        - `list`: List to iter over
        - `chunk_size`: Chunk size
    """
    return (
        list[pos : pos + chunk_size] for pos in range(0, len(list), chunk_size)
    )
