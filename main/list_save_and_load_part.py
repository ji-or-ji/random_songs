###例行公事
def main():
    pass
if __name__ == '__main__':
    main() 
###
''''''
### 导入模块
import json
import os
###
''''''
###导入自定义函数
# from main.history_part import record_history
from main.config_part import load_playlist_config
from main.config_part import save_playlist_config

###

def display_statistics(statistics):
    """显示统计信息"""
    print("\n📊 歌曲统计信息 📊")
    print("=" * 40)
    print(f"总歌曲数: {statistics['total_songs']}")
    print(f"有效歌曲: {statistics['valid_songs']}")
    print(f"无效歌曲: {statistics['invalid_songs']}")
    print("\n👥 点歌人统计:")
    for requester, count in statistics['requesters'].items():
        print(f"  {requester}: {count}首")
    print("=" * 40)


def filter_valid_songs(songs):
    """过滤有效的歌曲（去除空歌名和空歌手名的歌曲）"""
    valid_songs = []
    for song in songs:
        song_name = song.get('song_name', '').strip()
        artist = song.get('artist', '').strip()
        # 只有当歌名不为空时才认为是有效歌曲
        if song_name:
            valid_songs.append(song)
    return valid_songs

def get_songs_statistics(songs):
    """获取歌曲统计信息"""
    valid_songs = filter_valid_songs(songs)
    total_songs = len(songs)
    valid_count = len(valid_songs)
    invalid_count = total_songs - valid_count
    
    # 统计点歌人
    requesters = {}
    for song in valid_songs:
        requester = song.get('requested_by', '未知')
        requesters[requester] = requesters.get(requester, 0) + 1
    
    return {
        'total_songs': total_songs,
        'valid_songs': valid_count,
        'invalid_songs': invalid_count,
        'requesters': requesters
    }

def save_songs(songs, playlist_id=None):
    """保存歌曲列表到文件"""
    config = load_playlist_config()
    
    if playlist_id:
        # 保存到指定歌单
        if playlist_id in config['playlists']:
            file_path = config['playlists'][playlist_id]['file_path']
        else:
            print(f'歌单不存在: {playlist_id}')
            return False
    else:
        # 保存到当前歌单
        current_playlist_id = config['current_playlist']
        file_path = config['playlists'][current_playlist_id]['file_path']
    
    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump({'songs': songs}, f, ensure_ascii=False, indent=2)
        
        # 更新歌单统计信息
        playlist_id_to_update = playlist_id if playlist_id else current_playlist_id
        config['playlists'][playlist_id_to_update]['song_count'] = len(songs)
        save_playlist_config(config)
        
        return True
    except Exception as e:
        print(f'保存文件失败: {e}')
        return False

def load_songs(playlist_id=None):
    """加载歌曲列表文件"""
    config = load_playlist_config()
    
    if playlist_id:
        # 加载指定歌单
        if playlist_id in config['playlists']:
            playlist = config['playlists'][playlist_id]
            file_path = playlist['file_path']
        else:
            print(f'歌单不存在: {playlist_id}')
            return []
    else:
        # 加载当前歌单
        current_playlist_id = config['current_playlist']
        playlist = config['playlists'][current_playlist_id]
        file_path = playlist['file_path']
    
    # 在多个可能的位置查找歌曲文件
    possible_paths = [
        file_path,  # 当前目录
        f'../{file_path}',  # 父目录
        f'./main_data/{file_path}',  # main_data子目录
        f'main_data/{file_path}'  # main_data子目录
    ]
    
    for json_path in possible_paths:
        try:
            with open(json_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                songs = data.get('songs', [])
                
                # 更新歌单统计信息
                if playlist_id or current_playlist_id:
                    playlist_id_to_update = playlist_id if playlist_id else current_playlist_id
                    config['playlists'][playlist_id_to_update]['song_count'] = len(songs)
                    save_playlist_config(config)
                
                print(f'成功加载歌曲列表: {json_path} (歌单: {playlist["name"]})')
                return songs
        except FileNotFoundError:
            continue
        except json.JSONDecodeError:
            print(f'歌曲列表文件已损坏，请检查文件格式: {json_path}')
            return []
    
    print('歌曲列表文件不存在，请先创建歌曲列表')
    return []
