import os
import json

# 测试在main_data目录中创建文件
def test_file_creation():
    print("当前工作目录:", os.getcwd())
    
    # 测试创建playlist_3.json文件
    file_path = "main_data/playlist_3.json"
    print(f"尝试创建文件: {file_path}")
    
    try:
        # 创建测试数据
        test_data = {"songs": [{"song_name": "Test Song", "artist": "Test Artist"}]}
        
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(test_data, f, ensure_ascii=False, indent=2)
        
        print("✅ 文件创建成功!")
        
        # 检查文件是否存在
        if os.path.exists(file_path):
            print("✅ 文件确实存在")
        else:
            print("❌ 文件不存在")
            
    except Exception as e:
        print(f"❌ 文件创建失败: {e}")
        print(f"错误类型: {type(e).__name__}")

if __name__ == "__main__":
    test_file_creation()
