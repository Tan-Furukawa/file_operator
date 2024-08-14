# %%
import seaborn as sns
from typing import Callable
import re
import pandas as pd
import numpy as np
import os
import glob
import matplotlib.pylab as plt
import cupy as cp
# %%


def numerical_sort_by_underscore(value: str) -> int:
    value = os.path.basename(value)
    parts = value.split("_")  # ファイル名をアンダースコアで分割
    if len(parts) == 2:
        try:
            return int(parts[1].split(".")[0])  # 数字部分を抜き出して整数に変換
        except ValueError as e:
            raise ValueError(e)
    else:
        raise ValueError("invalid input. value should be xxxx_yyy.zzz")


def get_files_from_dir(dir_path: str, marker: str = "con") -> list[str]:
    file_pattern = os.path.join(dir_path, f"res/*{marker}*")
    file_list = glob.glob(file_pattern)
    sorted_file_list = sorted(file_list, key=numerical_sort_by_underscore)
    return sorted_file_list


def get_files_with_extension(dir_name: str, extension: str) -> list[str]:
    """
    Retrieves a list of file paths with the specified extension from the given directory and its subdirectories.

    Args:
        dir_name (str): The directory to search within.
        extension (str): The file extension to filter by (e.g., '.txt').

    Returns:
        List[str]: A list of file paths that have the specified extension.
    """
    matching_files = []
    for root, _, files in os.walk(dir_name):
        for file in files:
            if file.endswith(extension):
                matching_files.append(os.path.join(root, file))
    return matching_files

def apply_function_to_file_list(file_list: list[str], fun: Callable[[str], None]) -> None:
    for file in file_list:
        fun(file)

if __name__ == "__main__":
    print(get_files_with_extension("tmp/test", "txt"))
    print(get_files_with_extension("tmp-no-exist", "txt"))