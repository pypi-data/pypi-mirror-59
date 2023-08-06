from typing import Union, List

import arrayfiles

from lineflow import Dataset
from lineflow.core import ConcatDataset, ZipDataset


class TextDataset(Dataset):
    """Dataset of a line-oriented text file.

    Args:
        paths (Union[str, List[str]]): The path to the text file(s).
        encoding (str, optional): The name of the encoding used to decode.
        mode (str, optional): Controls how to combine the text files.
    """

    def __init__(self,
                 paths: Union[str, List[str]],
                 encoding: str = 'utf-8',
                 mode: str = 'zip') -> None:
        if isinstance(paths, str):
            dataset = arrayfiles.TextFile(paths, encoding)
        elif isinstance(paths, list):
            if mode == 'zip':
                dataset = ZipDataset(*[arrayfiles.TextFile(p, encoding) for p in paths])
            elif mode == 'concat':
                dataset = ConcatDataset(*[arrayfiles.TextFile(p, encoding) for p in paths])
            else:
                raise ValueError(f"only 'zip' and 'concat' are valid for 'mode', but '{mode}' is given.")

        super().__init__(dataset)


class CsvDataset(Dataset):
    """Dataset of a CSV file.

    Args:
        path (str): The path to the text file.
        encoding (str, optional): The name of the encoding used to decode.
        delimiter (str, optional): A one-character string used to separate fields. It defaults to ','.
        header (bool, optional): If ``True``, the csvfile will use the first line of the file as a header.
    """

    def __init__(self,
                 path: str,
                 encoding: str = 'utf-8',
                 delimiter: str = ',',
                 header: bool = False) -> None:

        super().__init__(
            arrayfiles.CsvFile(path=path, encoding=encoding, delimiter=delimiter, header=header))
