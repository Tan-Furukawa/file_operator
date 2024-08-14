# %%
from typing import Callable
import os
import glob


def numerical_sort_by_underscore(value: str) -> int:
    """
    Extracts and returns the numerical value from a string formatted as "xxxx_yyy.zzz".

    The function expects a string input representing a file path or file name with a specific format:
    "xxxx_yyy.zzz", where "xxxx" can be any string, "yyy" is a numeric value, and "zzz" is the file
    extension. The function will:

    1. Extract the file name from the given path (if a full path is provided).
    2. Split the file name into two parts using an underscore ('_') as the delimiter.
    3. Extract the numeric portion (i.e., "yyy" part before the dot).
    4. Convert this numeric portion to an integer and return it.

    Args:
        value (str): A string representing a file path or file name in the format "xxxx_yyy.zzz".

    Returns:
        int: The integer extracted from the numeric portion of the input string.

    Raises:
        ValueError: If the input string does not contain exactly two parts separated by an underscore,
                    or if the numeric portion cannot be converted to an integer.

    Example:
        >>> numerical_sort_by_underscore("example_123.txt")
        123

        >>> numerical_sort_by_underscore("path/to/file_456.pdf")
        456

        >>> numerical_sort_by_underscore("invalid_format.txt")
        ValueError: invalid input. value should be xxxx_yyy.zzz
    """

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
    """
    Retrieves and returns a list of file paths from a specified directory, filtered and sorted based on a marker string.

    This function searches for files in the specified directory (and its "res" subdirectory) that contain the given
    marker string in their names. The found files are then sorted numerically based on the numeric portion of their
    filenames (as determined by the `numerical_sort_by_underscore` function) and returned as a list.

    Args:
        dir_path (str): The path to the directory where the search will be conducted.
        marker (str, optional): A substring to filter the files by. Only files containing this substring in their
                                names will be included in the result. Defaults to "con".

    Returns:
        list[str]: A list of file paths that match the marker string, sorted numerically by the numeric portion
                   of their filenames.

    Raises:
        ValueError: If `numerical_sort_by_underscore` raises a ValueError during sorting, this exception will be propagated.

    Example:
        >>> get_files_from_dir("/path/to/directory", marker="con")
        ['/path/to/directory/res/file_con_1.txt', '/path/to/directory/res/file_con_2.txt', '/path/to/directory/res/file_con_10.txt']

        >>> get_files_from_dir("/path/to/directory", marker="test")
        ['/path/to/directory/res/file_test_3.txt', '/path/to/directory/res/file_test_4.txt']

    Notes:
        - The search is conducted in the "res" subdirectory of the provided `dir_path`.
        - The sorting relies on the `numerical_sort_by_underscore` function, which expects filenames to follow the pattern "xxxx_yyy.zzz".
    """

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
        list[str]: A list of file paths that have the specified extension.
    """
    matching_files = []
    for root, _, files in os.walk(dir_name):
        for file in files:
            if file.endswith(extension):
                matching_files.append(os.path.join(root, file))
    return matching_files


def generate_file_path_dict(file_name_list: list[str]) -> list[dict[str, str]]:
    """
    Generates a list of dictionaries where each dictionary contains a file path as the key and the file name as the value.

    Args:
        file_name_list (list[str]): A list of file names.

    Returns:
        list[dict[str, str]]: A list of dictionaries where each dictionary contains {file_path: file_name}.
    """
    file_dict_list = []
    for file_name in file_name_list:
        file_dict_list.append({"file_path": file_name})
    return file_dict_list


def apply_function_to_file_list(
    file_list: list[str], fun: Callable[[str], None]
) -> None:
    """
    Applies a given function to each file path in the provided list.

    Args:
        file_list (list[str]): A list of file paths.
        fun (Callable[[str], None]): A function to apply to each file path.

    Returns:
        None
    """
    for file in file_list:
        fun(file)


if __name__ == "__main__":
    print(get_files_with_extension("tmp/test", "txt"))
    print(get_files_with_extension("tmp-no-exist", "txt"))

    path = "tmp/result_tmp"
    files = get_files_with_extension(path, "npy")
    # a = generate_file_path_dict(files)

# %%
