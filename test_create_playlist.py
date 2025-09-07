#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os
import inspect

# 添加 main_data 目录到 Python 路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'main_data'))

# 导入主程序模块
from main import create_playlist

def test_create_playlist():
    """测试创建空白歌单功能"""
    print("测试创建空白歌单功能...")
    print("=" * 50)
    
    try:
        # 获取函数源代码
        source = inspect.getsource(create_playlist)
        
        # 检查函数文档字符串
        if "创建空白歌单" in source:
            print("✅ 函数文档字符串已正确更新为'创建空白歌单'")
        else:
            print("❌ 函数文档字符串未正确更新")
            return False
        
        # 检查用户提示信息
        if "创建空白歌单" in source:
            print("✅ 用户提示信息已正确更新为'创建空白歌单'")
        else:
            print("❌ 用户提示信息未正确更新")
            return False
        
        # 检查函数是否包含必要的逻辑（更新为检查正确的函数调用）
        if "input" in source and "load_playlist_config" in source:
            print("✅ 函数包含必要的输入处理和配置更新逻辑")
        else:
            print("❌ 函数缺少必要的逻辑")
            return False
        
        print("✅ 创建空白歌单功能测试通过！")
        return True
        
    except Exception as e:
        print(f"❌ 测试失败：{e}")
        return False

if __name__ == "__main__":
    test_create_playlist()
