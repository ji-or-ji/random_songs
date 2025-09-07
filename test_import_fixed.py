#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import os
import sys

# 添加main_data目录到Python路径
sys.path.insert(0, 'main_data')

# 创建一个测试的外部歌单文件
test_external_playlist = {
    "songs": [
        {
            "id": 1,
            "song_name": "测试歌曲1",
            "artist": "测试歌手1",
            "url_list": "",
            "requested_by": "测试用户"
        },
        {
            "id": 2,
            "song_name": "测试歌曲2",
            "artist": "测试歌手2",
            "url_list": "",
            "requested_by": "测试用户"
        }
    ]
}

# 保存测试文件
test_file_path = "test_external_playlist.json"
with open(test_file_path, 'w', encoding='utf-8') as f:
    json.dump(test_external_playlist, f, ensure_ascii=False, indent=2)

print(f"创建测试文件: {test_file_path}")

# 现在测试导入功能
from main import import_external_playlist

# 模拟用户输入
def mock_input(prompt):
    if "请输入外部歌单文件路径" in prompt:
        return test_file_path
    elif "请输入新歌单名称" in prompt:
        return "测试导入歌单"
    elif "请输入歌单描述" in prompt:
        return "测试导入的歌单"
    return ""

# 替换input函数
original_input = __builtins__.input
__builtins__.input = mock_input

try:
    print("开始测试导入功能...")
    import_external_playlist()
    print("导入功能测试完成!")
finally:
    # 恢复原始input函数
    __builtins__.input = original_input
    # 清理测试文件
    if os.path.exists(test_file_path):
        os.remove(test_file_path)
        print(f"清理测试文件: {test_file_path}")
