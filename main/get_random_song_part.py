###导入模块
import random
import datetime

###导入自定义函数
from main.config_part import load_playlist_config
from main.config_part import save_playlist_config
###

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


def get_random_song(songs):
    """随机选择一首歌曲（兼容旧版本）"""
    return get_random_song_with_prevention(songs)

def get_random_song_with_prevention(songs, playlist_id=None):
    """带防重复功能的随机选择歌曲"""
    if not songs:
        return None
    
    valid_songs = filter_valid_songs(songs)
    if not valid_songs:
        return None
    
    # 获取当前歌单的防重复配置
    config = load_playlist_config()
    if playlist_id:
        playlist_config = config['playlists'].get(playlist_id)
    else:
        playlist_config = config['playlists'].get(config['current_playlist'])
    
    if not playlist_config or not playlist_config['duplicate_prevention']['enabled']:
        # 防重复功能未启用，直接随机选择
        return random.choice(valid_songs)
    
    prevention_config = playlist_config['duplicate_prevention']
    
    # 检查是否需要重置播放记录
    if prevention_config['reset_on_all_played']:
        current_time = datetime.datetime.now()
        last_reset_time = prevention_config.get('last_reset_time')
        
        # 如果所有歌曲都已播放过，或者从未重置过，则重置
        played_count = len(prevention_config['played_songs'])
        total_songs = len(valid_songs)
        
        if played_count >= total_songs or last_reset_time is None:
            prevention_config['played_songs'] = []
            prevention_config['last_reset_time'] = current_time.strftime("%Y-%m-%d %H:%M:%S")
            save_playlist_config(config)
    
    # 获取时间窗口内的已播放歌曲
    played_songs_in_window = []
    if prevention_config['mode'] == 'time_window':
        time_window_hours = prevention_config['time_window_hours']
        time_window_minutes = prevention_config['time_window_minutes']
        time_window_seconds = time_window_hours * 3600 + time_window_minutes * 60
        
        current_time = datetime.datetime.now()
        for song_info in prevention_config['played_songs']:
            play_time = datetime.datetime.strptime(song_info['play_time'], "%Y-%m-%d %H:%M:%S")
            time_diff = (current_time - play_time).total_seconds()
            
            if time_diff <= time_window_seconds:
                played_songs_in_window.append(song_info['song_id'])
    
    # 过滤出未在时间窗口内播放过的歌曲
    available_songs = [song for song in valid_songs 
                      if song.get('id') not in played_songs_in_window]
    
    if not available_songs:
        # 所有歌曲都在时间窗口内播放过，根据配置决定是否重置
        if prevention_config['reset_on_all_played']:
            prevention_config['played_songs'] = []
            prevention_config['last_reset_time'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            save_playlist_config(config)
            available_songs = valid_songs
        else:
            # 不重置，返回None表示无可用歌曲
            return None
    
    # 随机选择一首歌曲
    selected_song = random.choice(available_songs)
    
    # 记录播放历史
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    prevention_config['played_songs'].append({
        'song_id': selected_song.get('id'),
        'song_name': selected_song.get('song_name', '未知'),
        'play_time': current_time
    })
    
    save_playlist_config(config)
    
    return selected_song

