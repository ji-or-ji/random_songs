### 导入模块
import json
import os
import random
import datetime
import time
import webbrowser
###
''''''
###导入自定义函数
# from

def save_playlist_config(config):
    """保存歌单配置文件"""
    # 使用与load_playlist_config相同的路径解析逻辑
    config_paths = [
        'playlists_config.json',
        '../playlists_config.json',
        './main_data/playlists_config.json',
        'main_data/playlists_config.json'
    ]
    
    # 尝试在所有可能的路径中保存
    for config_path in config_paths:
        try:
            with open(config_path, 'w', encoding='utf-8') as f:
                json.dump(config, f, ensure_ascii=False, indent=2)
            return True
        except Exception as e:
            # 如果这个路径失败，继续尝试下一个
            continue
    
    # 如果所有路径都失败，尝试在当前目录创建
    try:
        with open('playlists_config.json', 'w', encoding='utf-8') as f:
            json.dump(config, f, ensure_ascii=False, indent=2)
        return True
    except Exception as e:
        print(f'保存歌单配置失败: {e}')
        return False


def load_playlist_config():
    """加载歌单配置文件"""
    config_paths = [
        'playlists_config.json',
        '../playlists_config.json',
        './main_data/playlists_config.json',
        'main_data/playlists_config.json'
    ]
    
    for config_path in config_paths:
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                config = json.load(f)
                return config
        except FileNotFoundError:
            continue
        except json.JSONDecodeError:
            print(f'歌单配置文件已损坏: {config_path}')
            # 创建默认配置
            return {
                "current_playlist": "default",
                "playlists": {
                    "default": {
                        "name": "默认歌单",
                        "description": "主歌单",
                        "file_path": "songs_list.json",
                        "created_at": datetime.datetime.now().strftime("%Y/%m/%d"),
                        "song_count": 0
                    }
                }
            }
    
    # 如果配置文件不存在，创建默认配置
    default_config = {
        "current_playlist": "default",
        "playlists": {
            "default": {
                "name": "默认歌单",
                "description": "主歌单",
                "file_path": "songs_list.json",
                "created_at": datetime.datetime.now().strftime("%Y/%m/%d"),
                "song_count": 0
            }
        }
    }
    save_playlist_config(default_config)
    return default_config

def save_playlist_config(config):
    """保存歌单配置文件"""
    # 使用与load_playlist_config相同的路径解析逻辑
    config_paths = [
        'playlists_config.json',
        '../playlists_config.json',
        './main_data/playlists_config.json',
        'main_data/playlists_config.json'
    ]
    
    # 尝试在所有可能的路径中保存
    for config_path in config_paths:
        try:
            with open(config_path, 'w', encoding='utf-8') as f:
                json.dump(config, f, ensure_ascii=False, indent=2)
            return True
        except Exception as e:
            # 如果这个路径失败，继续尝试下一个
            continue
    
    # 如果所有路径都失败，尝试在当前目录创建
    try:
        with open('playlists_config.json', 'w', encoding='utf-8') as f:
            json.dump(config, f, ensure_ascii=False, indent=2)
        return True
    except Exception as e:
        print(f'保存歌单配置失败: {e}')
        return False
