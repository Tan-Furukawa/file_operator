#%%
import seaborn as sns
import save
import yaml
from typing import Callable, Any
import re
import pandas as pd
import numpy as np
import os
import glob
import matplotlib.pylab as plt
import cupy as cp
from phase_field_2d_ternary.matrix_plot_tools import Ternary

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

def generate_file_path_and_yaml_info(file_name_list: list[str]) -> list[dict[str, Any]]:
    """
    Generates a list of dictionaries where each dictionary contains a file path as the key,
    the file name as the value, and additional YAML information if a YAML file exists in the same directory.

    Args:
        file_name_list (list[str]): A list of file names.

    Returns:
        list[dict[str, Any]]: A list of dictionaries where each dictionary contains
                              {"file_path": file_name, "information": yaml_data (if available)}.
    """
    file_info_list = []

    for file_name in file_name_list:
        file_path = os.path.abspath(file_name)
        file_info = {"file_path": file_name}

        # Check for YAML files in the same directory
        dir_name = os.path.dirname(file_path)
        for yaml_file in os.listdir(dir_name):
            if yaml_file.endswith(".yaml") or yaml_file.endswith(".yml"):
                yaml_path = os.path.join(dir_name, yaml_file)
                with open(yaml_path, 'r') as f:
                    yaml_data = yaml.safe_load(f)
                    file_info["information"] = yaml_data
                    break
        file_info_list.append(file_info)
    return file_info_list

def apply_function_to_file_list(file_list: list[str], fun: Callable[[str], None]) -> None:
    for file in file_list:
        fun(file)

def extract_directory_information(dir_path: str):
    result = []
    
    # ディレクトリの中を走査
    for subdir_name in os.listdir(dir_path):
        subdir_path = os.path.join(dir_path, subdir_name)
        
        if os.path.isdir(subdir_path):
            # 各サブディレクトリの情報を格納する辞書を作成
            dir_info = {
                "dir_name": subdir_name,
                "file_list": [],
                "information": None
            }
            
            con1_files = []
            con2_files = []
            
            # サブディレクトリ内のファイルを走査
            for file_name in os.listdir(subdir_path):
                file_path = os.path.join(subdir_path, file_name)
                
                if file_name.startswith('con1') and file_name.endswith('.npy'):
                    con1_files.append(file_name)
                elif file_name.startswith('con2') and file_name.endswith('.npy'):
                    con2_files.append(file_name)
                elif file_name == "test.yaml":
                    with open(file_path, 'r') as yaml_file:
                        dir_info["information"] = yaml.safe_load(yaml_file)
            
            # con1とcon2のファイルをペアにする
            for con1_file in sorted(con1_files):
                matching_number = con1_file.split('_')[1].split('.')[0]
                con2_file = next((f for f in con2_files if f.split('_')[1].split('.')[0] == matching_number), None)
                if con2_file:
                    dir_info["file_list"].append([con1_file, con2_file])
            result.append(dir_info)
    return result


#%%

if __name__ == "__main__":
    print(get_files_with_extension("tmp/test", "txt"))
    print(get_files_with_extension("tmp-no-exist", "txt"))

    path = "tmp/result_tmp"
    files = get_files_with_extension(path, "npy")
    # a = generate_file_path_dict(files)

    directory_info = extract_directory_information("tmp/result_tmp")
    #%%
    for file in directory_info:
        con1 = np.load(f"tmp/result_tmp/{file["dir_name"]}/{file["file_list"][-1][0]}")
        con2 = np.load(f"tmp/result_tmp/{file["dir_name"]}/{file["file_list"][-1][1]}")
        Ternary.imshow3(con1, con2)
        plt.show()
    a = generate_file_path_and_yaml_info(files)
    b = yaml.dump(a)
    save.save_str("tmp/test.yaml", b)

    # print(files[2])
# %%
