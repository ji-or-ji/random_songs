import os
import json
import datetime

# 模拟 import_external_playlist 函数的完整流程
def test_import_simulation():
    print("模拟外部歌单导入流程")
    print("=" * 40)
    
    # 模拟外部文件路径（用户输入）
    external_file_path = "C:\\Users\\A\\Desktop\\新建 文本文档 (2).json"
    print(f"外部文件路径: {external_file_path}")
    
    # 检查文件是否存在
    if not os.path.exists(external_file_path):
        print(f"❌ 文件不存在: {external_file_path}")
        return
    
    try:
        # 读取外部歌单文件
        with open(external_file_path, 'r', encoding='utf-8') as f:
            external_data = json.load(f)
        
        # 检查文件格式
        if 'songs' not in external_data:
            print("❌ 文件格式错误: 缺少 'songs' 字段")
            return
        
        external_songs = external_data['songs']
        if not isinstance(external_songs, list):
            print("❌ 文件格式错误: 'songs' 字段应该是一个列表")
            return
        
        print(f"✅ 成功读取外部歌单，共 {len(external_songs)} 首歌曲")
        
        # 模拟加载配置
        config = {
            "current_playlist": "playlist_2",
            "playlists": {
                "default": {
                    "name": "默认歌单",
                    "description": "主歌单",
                    "file_path": "main_data/songs_list.json",
                    "created_at": "2025/09/06",
                    "song_count": 60
                },
                "playlist_2": {
                    "name": "内定qwb",
                    "description": "just_for_play",
                    "file_path": "main_data/playlist_2.json",
                    "created_at": "2025/09/06",
                    "song_count": 1
                }
            }
        }
        
        # 模拟用户输入
        playlist_name = "qwb"
        playlist_description = "qwb"
        
        # 检查名称是否已存在
        for playlist_info in config['playlists'].values():
            if playlist_info['name'] == playlist_name:
                print("❌ 歌单名称已存在!")
                return
        
        # 生成唯一的歌单ID
        playlist_id = f"playlist_{len(config['playlists']) + 1}"
        while playlist_id in config['playlists']:
            playlist_id = f"playlist_{len(config['playlists']) + 1}"
        
        print(f"生成歌单ID: {playlist_id}")
        
        # 创建歌单文件路径
        file_path = f"main_data/{playlist_id}.json"
        print(f"歌单文件路径: {file_path}")
        
        # 保存导入的歌曲到新歌单
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump({'songs': external_songs}, f, ensure_ascii=False, indent=2)
            print("✅ 歌单文件创建成功!")
            
        except Exception as e:
            print(f"❌ 创建歌单文件失败: {e}")
            print(f"错误类型: {type(e).__name__}")
            return
        
        # 添加到配置
        config['playlists'][playlist_id] = {
            'name': playlist_name,
            'description': playlist_description,
            'file_path': file_path,
            'created_at': datetime.datetime.now().strftime("%Y/%m/%d"),
            'song_count': len(external_songs)
        }
        
        print("✅ 模拟导入完成!")
        print(f"新歌单: {playlist_name} ({len(external_songs)}首歌曲)")
            
    except json.JSONDecodeError:
        print("❌ 文件格式错误: 不是有效的JSON文件")
    except Exception as e:
        print(f"❌ 导入失败: {e}")
        print(f"错误类型: {type(e).__name__}")

if __name__ == "__main__":
    test_import_simulation()
