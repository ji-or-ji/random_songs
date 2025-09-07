#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import json

# 模拟 import_external_playlist 函数的文件创建部分
def test_file_creation():
    print("测试文件创建功能")
    print("=" * 30)
    
    # 模拟 import_external_playlist 函数中的代码
    playlist_id = "playlist_3"
    external_songs = [
        {"song_name": "测试歌曲1", "artist": "测试歌手1"},
        {"song_name": "测试歌曲2", "artist": "测试歌手2"}
    ]
    
    # 使用相同的文件路径
    file_path = f"main_data/{playlist_id}.json"
    
    print(f"当前工作目录: {os.getcwd()}")
    print(f"尝试创建文件: {file_path}")
    print(f"绝对路径: {os.path.abspath(file_path)}")
    
    # 检查目录是否存在
    dir_path = os.path.dirname(file_path)
    print(f"目录路径: {dir_path}")
    print(f"目录是否存在: {os.path.exists(dir_path)}")
    
    if not os.path.exists(dir_path):
        print(f"尝试创建目录: {dir_path}")
        try:
            os.makedirs(dir_path, exist_ok=True)
            print("目录创建成功")
        except Exception as e:
            print(f"目录创建失败: {e}")
            return
    
    # 尝试创建文件
    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump({'songs': external_songs}, f, ensure_ascii=False, indent=2)
        print("✅ 文件创建成功!")
        print(f"文件已创建在: {os.path.abspath(file_path)}")
    except Exception as e:
        print(f"❌ 文件创建失败: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_file_creation()
