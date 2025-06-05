"""工具函数测试。"""

import json
import pickle
import os
from pathlib import Path

import pytest

from {{cookiecutter.project_slug}}.utils.file_utils import (
    ensure_dir,
    load_json,
    save_json,
    load_pickle,
    save_pickle,
    list_files,
    get_file_size
)
from {{cookiecutter.project_slug}}.utils.data_utils import (
    generate_random_string,
    calculate_md5,
    clean_text,
    chunk_list,
    flatten_dict
)


def test_ensure_dir(temp_dir):
    """测试确保目录存在。"""
    # 动态导入，避免模板变量替换问题
    from {{cookiecutter.project_slug}}.utils.file_utils import ensure_dir

    test_dir = temp_dir / "test_dir" / "nested"
    path = ensure_dir(test_dir)

    assert path.exists()
    assert path.is_dir()


def test_json_roundtrip(temp_dir, sample_data):
    """测试JSON数据的保存和加载。"""
    from {{cookiecutter.project_slug}}.utils.file_utils import load_json, save_json

    json_file = temp_dir / "test.json"

    # 保存数据
    save_json(sample_data, json_file)
    assert json_file.exists()

    # 加载数据
    loaded_data = load_json(json_file)
    assert loaded_data == sample_data


def test_pickle_roundtrip(temp_dir, sample_data):
    """测试Pickle数据的保存和加载。"""
    from {{cookiecutter.project_slug}}.utils.file_utils import load_pickle, save_pickle

    pickle_file = temp_dir / "test.pkl"

    # 保存数据
    save_pickle(sample_data, pickle_file)
    assert pickle_file.exists()

    # 加载数据
    loaded_data = load_pickle(pickle_file)
    assert loaded_data == sample_data


def test_list_files(temp_dir):
    """测试列出文件。"""
    from {{cookiecutter.project_slug}}.utils.file_utils import ensure_dir, list_files

    # 创建测试文件
    file1 = temp_dir / "file1.txt"
    file2 = temp_dir / "file2.txt"
    file3 = temp_dir / "subdir" / "file3.txt"

    file1.touch()
    file2.touch()
    ensure_dir(file3.parent)
    file3.touch()

    # 非递归测试
    files = list_files(temp_dir, "*.txt")
    assert len(files) == 2
    assert set(f.name for f in files) == {"file1.txt", "file2.txt"}

    # 递归测试
    files = list_files(temp_dir, "*.txt", recursive=True)
    assert len(files) == 3
    assert set(f.name for f in files) == {"file1.txt", "file2.txt", "file3.txt"}


def test_get_file_size(temp_dir):
    """测试获取文件大小。"""
    from {{cookiecutter.project_slug}}.utils.file_utils import get_file_size

    # 创建固定大小的文件
    test_file = temp_dir / "size_test.dat"
    with open(test_file, "wb") as f:
        f.write(b"0" * 1024)  # 1KB的文件

    assert get_file_size(test_file) == 1024
    assert get_file_size(test_file, "KB") == 1.0
    assert get_file_size(test_file, "MB") == 1.0 / 1024

    # 测试无效单位
    with pytest.raises(ValueError):
        get_file_size(test_file, "invalid_unit")


def test_generate_random_string():
    """测试生成随机字符串。"""
    from {{cookiecutter.project_slug}}.utils.data_utils import generate_random_string

    # 默认设置
    s1 = generate_random_string()
    assert len(s1) == 8
    assert s1.isalnum()  # 包含字母和数字

    # 自定义长度
    s2 = generate_random_string(length=12)
    assert len(s2) == 12

    # 不包含数字
    s3 = generate_random_string(include_digits=False)
    assert s3.isalpha()  # 只包含字母

    # 两次生成的字符串应该不同
    assert s1 != generate_random_string()


def test_calculate_md5():
    """测试MD5哈希计算。"""
    from {{cookiecutter.project_slug}}.utils.data_utils import calculate_md5

    # 字符串输入
    assert calculate_md5("hello") == "5d41402abc4b2a76b9719d911017c592"

    # 字节输入
    assert calculate_md5(b"hello") == "5d41402abc4b2a76b9719d911017c592"


def test_clean_text():
    """测试文本清理。"""
    from {{cookiecutter.project_slug}}.utils.data_utils import clean_text

    assert clean_text("  hello  world  ") == "hello world"
    assert clean_text("\t\nhello\n\tworld\n") == "hello world"
    assert clean_text("multiple    spaces    here") == "multiple spaces here"


def test_chunk_list():
    """测试列表分块。"""
    from {{cookiecutter.project_slug}}.utils.data_utils import chunk_list

    # 空列表
    assert chunk_list([], 3) == []

    # 正常分块
    assert chunk_list([1, 2, 3, 4, 5], 2) == [[1, 2], [3, 4], [5]]

    # 块大小等于列表长度
    assert chunk_list([1, 2, 3], 3) == [[1, 2, 3]]

    # 块大小大于列表长度
    assert chunk_list([1, 2], 5) == [[1, 2]]


def test_flatten_dict():
    """测试字典扁平化。"""
    from {{cookiecutter.project_slug}}.utils.data_utils import flatten_dict

    nested_dict = {
        "a": 1,
        "b": {
            "c": 2,
            "d": {
                "e": 3
            }
        },
        "f": 4
    }

    flat_dict = flatten_dict(nested_dict)

    assert flat_dict == {
        "a": 1,
        "b.c": 2,
        "b.d.e": 3,
        "f": 4
    }

    # 自定义分隔符
    flat_dict_custom = flatten_dict(nested_dict, separator="_")
    assert flat_dict_custom == {
        "a": 1,
        "b_c": 2,
        "b_d_e": 3,
        "f": 4
    }
