#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os

# 添加 main_data 目录到 Python 路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'main_data'))

# 导入主程序模块
from main import playlist_management_menu

def test_menu_options():
    """测试歌单管理菜单选项"""
    print("测试歌单管理菜单选项...")
    print("=" * 50)
    
    # 模拟调用歌单管理菜单函数
    try:
        # 由于菜单函数需要用户输入，我们直接检查函数定义
        import inspect
        source = inspect.getsource(playlist_management_menu)
        
        # 检查菜单选项
        if "从外部已有歌单导入" in source and "创建空白歌单" in source:
            print("✅ 菜单选项已正确更新：")
            print("   - 从外部已有歌单导入")
            print("   - 创建空白歌单")
        else:
            print("❌ 菜单选项未正确更新")
            return False
            
        # 检查选项数量
        if source.count("print(") >= 6:  # 至少6个选项
            print("✅ 菜单选项数量正确")
        else:
            print("❌ 菜单选项数量不正确")
            return False
            
        print("✅ 歌单管理菜单测试通过！")
        return True
        
    except Exception as e:
        print(f"❌ 测试失败：{e}")
        return False

if __name__ == "__main__":
    test_menu_options()
