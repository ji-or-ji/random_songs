###例行公事
def main():
    pass
if __name__ == '__main__':
    main() 
###

# 导入模块
import json
import os
import random
import datetime
import time
import webbrowser

def record_history(action_type, action_details, result="成功"):
    """记录操作历史到文件"""
    history_record = {
        "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "action": action_type,
        "details": action_details,
        "result": result
    }
    
    # 在多个可能的位置查找history_records.json
    possible_paths = [
        'history_records.json',
        '../history_records.json',
        './main_data/history_records.json',
        'main_data/history_records.json'
    ]
    
    for json_path in possible_paths:
        try:
            # 尝试读取现有历史记录
            with open(json_path, 'r', encoding='utf-8') as f:
                history_data = json.load(f)
                history_data.append(history_record)
                
                # 保存更新后的历史记录
                with open(json_path, 'w', encoding='utf-8') as f_out:
                    json.dump(history_data, f_out, ensure_ascii=False, indent=2)
                return True
        except FileNotFoundError:
            continue
        except json.JSONDecodeError:
            # 文件存在但格式错误，重新创建
            try:
                with open(json_path, 'w', encoding='utf-8') as f_out:
                    json.dump([history_record], f_out, ensure_ascii=False, indent=2)
                return True
            except Exception:
                continue
    
    # 如果所有路径都失败，尝试在当前目录创建
    try:
        with open('history_records.json', 'w', encoding='utf-8') as f:
            json.dump([history_record], f, ensure_ascii=False, indent=2)
        return True
    except Exception as e:
        print(f"记录历史失败: {e}")
        return False

def view_history():
    """查看历史记录"""
    possible_paths = [
        'history_records.json',
        '../history_records.json',
        './main_data/history_records.json',
        'main_data/history_records.json'
    ]
    
    for json_path in possible_paths:
        try:
            with open(json_path, 'r', encoding='utf-8') as f:
                history_data = json.load(f)
                
                if not history_data:
                    print("暂无历史记录")
                    return
                
                print("\n📜 操作历史记录 📜")
                print("=" * 60)
                for i, record in enumerate(history_data, 1):
                    print(f"{i}. [{record['timestamp']}] {record['action']}")
                    print(f"   详情: {record['details']}")
                    print(f"   结果: {record['result']}")
                    print("-" * 40)
                return
        except FileNotFoundError:
            continue
        except json.JSONDecodeError:
            print(f"历史记录文件已损坏: {json_path}")
            return
    
    print("暂无历史记录")

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

def load_auto_jump_config():
    """加载自动跳转配置文件"""
    config_paths = [
        'auto_jump_config.json',
        '../auto_jump_config.json',
        './main_data/auto_jump_config.json',
        'main_data/auto_jump_config.json'
    ]
    
    for config_path in config_paths:
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                config = json.load(f)
                return config
        except FileNotFoundError:
            continue
        except json.JSONDecodeError:
            print(f'自动跳转配置文件已损坏: {config_path}')
            # 创建默认配置
            return {
                "auto_jump_enabled": False,
                "jump_mode": "search",
                "custom_url": "",
                "jump_delay": 3
            }
    
    # 如果配置文件不存在，创建默认配置
    default_config = {
        "auto_jump_enabled": False,
        "jump_mode": "search",
        "custom_url": "",
        "jump_delay": 3
    }
    save_auto_jump_config(default_config)
    return default_config

def save_auto_jump_config(config):
    """保存自动跳转配置文件"""
    config_path = 'main_data/auto_jump_config.json'
    try:
        with open(config_path, 'w', encoding='utf-8') as f:
            json.dump(config, f, ensure_ascii=False, indent=2)
        return True
    except Exception as e:
        print(f'保存自动跳转配置失败: {e}')
        return False

def execute_auto_jump(song):
    """执行自动网页跳转"""
    config = load_auto_jump_config()
    
    if not config['auto_jump_enabled']:
        return
    
    print(f"\n⏰ 将在 {config['jump_delay']} 秒后自动跳转...")
    time.sleep(config['jump_delay'])
    
    # 优先检查歌曲是否有URL，如果有则优先跳转URL
    song_url = song.get('url_list', '').strip() if song else ''
    if song_url:
        # 跳转到歌曲URL
        print(f"🌐 跳转到歌曲URL: {song_url}")
        webbrowser.open(song_url)
        record_history("网页跳转", f"跳转到歌曲URL: {song_url}")
        return
    
    # 如果没有歌曲URL，则根据配置的模式跳转
    if config['jump_mode'] == 'url' and config['custom_url']:
        # 跳转到自定义URL
        print(f"🌐 跳转到: {config['custom_url']}")
        webbrowser.open(config['custom_url'])
        record_history("网页跳转", f"跳转到自定义URL: {config['custom_url']}")
        
    elif config['jump_mode'] == 'search' and song:
        # 跳转到B站搜索
        song_name = song.get('song_name', '').strip()
        artist = song.get('artist', '').strip()
        
        if song_name:
            search_query = f"{song_name}"
            if artist:
                search_query += f" {artist}"
            
            # URL编码搜索查询
            import urllib.parse
            encoded_query = urllib.parse.quote(search_query)
            bilibili_url = f"https://search.bilibili.com/all?keyword={encoded_query}"
            
            print(f"🔍 跳转到B站搜索: {search_query}")
            webbrowser.open(bilibili_url)
            record_history("网页跳转", f"跳转到B站搜索: {search_query}")
        else:
            print("无法执行搜索跳转: 歌曲名为空")
            
    else:
        print("自动跳转配置无效或未设置")

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

def get_random_song(songs):
    """随机选择一首歌曲（兼容旧版本）"""
    return get_random_song_with_prevention(songs)

def display_song_info(song):
    """显示歌曲信息"""
    if not song:
        print("没有找到有效的歌曲")
        return
    
    print("\n🎵 随机点歌结果 🎵")
    print("=" * 30)
    print(f"歌曲名: {song.get('song_name', '未知')}")
    print(f"歌手: {song.get('artist', '未知') or '未知'}")
    print(f"点歌人: {song.get('requested_by', '未知')}")
    if song.get('url_list'):
        print(f"链接: {song.get('url_list')}")
    print("=" * 30)
    
    # 记录历史
    record_history("随机点歌", f"歌曲: {song.get('song_name', '未知')} - 歌手: {song.get('artist', '未知')}")
    
    # 执行自动网页跳转
    execute_auto_jump(song)

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

def get_all_requesters(songs):
    """获取所有点歌人列表"""
    requesters = set()
    for song in songs:
        requester = song.get('requested_by', '').strip()
        if requester:
            requesters.add(requester)
    return sorted(list(requesters))

def add_requester(songs):
    """增加点歌人"""
    requester = input("请输入点歌人姓名: ").strip()
    if not requester:
        print("点歌人姓名不能为空!")
        return songs
    
    # 检查是否已存在
    existing_requesters = get_all_requesters(songs)
    if requester in existing_requesters:
        print(f"点歌人 '{requester}' 已存在!")
        return songs
    
    print(f"成功添加点歌人: {requester}")
    # 记录历史
    record_history("添加点歌人", f"点歌人: {requester}")
    return songs

def delete_requester(songs):
    """删除点歌人"""
    requesters = get_all_requesters(songs)
    if not requesters:
        print("没有可删除的点歌人!")
        return songs
    
    print("\n当前点歌人列表:")
    for i, requester in enumerate(requesters, 1):
        print(f"{i}. {requester}")
    
    try:
        choice = int(input("\n请选择要删除的点歌人编号: ").strip())
        if 1 <= choice <= len(requesters):
            requester_to_delete = requesters[choice - 1]
            
            # 确认删除
            confirm = input(f"确定要删除点歌人 '{requester_to_delete}' 吗? (y/N): ").strip().lower()
            if confirm == 'y':
                # 删除该点歌人的所有歌曲
                new_songs = [song for song in songs if song.get('requested_by') != requester_to_delete]
                if save_songs(new_songs):
                    print(f"已删除点歌人 '{requester_to_delete}' 及其所有歌曲")
                    # 记录历史
                    record_history("删除点歌人", f"点歌人: {requester_to_delete} - 删除歌曲数量: {len(songs) - len(new_songs)}")
                    return new_songs
                else:
                    print("保存失败!")
            else:
                print("取消删除")
        else:
            print("无效的选择!")
    except ValueError:
        print("请输入有效的数字!")
    
    return songs

def modify_requester(songs):
    """修改点歌人"""
    requesters = get_all_requesters(songs)
    if not requesters:
        print("没有可修改的点歌人!")
        return songs
    
    print("\n当前点歌人列表:")
    for i, requester in enumerate(requesters, 1):
        print(f"{i}. {requester}")
    
    try:
        choice = int(input("\n请选择要修改的点歌人编号: ").strip())
        if 1 <= choice <= len(requesters):
            old_requester = requesters[choice - 1]
            new_requester = input(f"请输入新的点歌人姓名 (原姓名: {old_requester}): ").strip()
            
            if not new_requester:
                print("新点歌人姓名不能为空!")
                return songs
            
            if new_requester == old_requester:
                print("新姓名与原姓名相同!")
                return songs
            
            # 修改所有相关歌曲的点歌人
            modified = False
            for song in songs:
                if song.get('requested_by') == old_requester:
                    song['requested_by'] = new_requester
                    modified = True
            
            if modified:
                if save_songs(songs):
                    print(f"已将点歌人 '{old_requester}' 修改为 '{new_requester}'")
                    # 记录历史
                    record_history("修改点歌人", f"原姓名: {old_requester} -> 新姓名: {new_requester}")
                    return songs
                else:
                    print("保存失败!")
            else:
                print("未找到相关歌曲!")
        else:
            print("无效的选择!")
    except ValueError:
        print("请输入有效的数字!")
    
    return songs

def manage_requesters(songs):
    """点歌人管理菜单"""
    while True:
        print("\n🎤 点歌人管理 🎤")
        print("=" * 20)
        print("1. 增加点歌人")
        print("2. 删除点歌人")
        print("3. 修改点歌人")
        print("4. 查看点歌人列表")
        print("5. 返回主菜单")
        
        choice = input("请输入选项 (1-5): ").strip()
        
        if choice == '1':
            songs = add_requester(songs)
        elif choice == '2':
            songs = delete_requester(songs)
        elif choice == '3':
            songs = modify_requester(songs)
        elif choice == '4':
            requesters = get_all_requesters(songs)
            if requesters:
                print("\n📋 点歌人列表:")
                for i, requester in enumerate(requesters, 1):
                    print(f"{i}. {requester}")
            else:
                print("暂无点歌人")
        elif choice == '5':
            break
        else:
            print("无效选项，请重新选择!")
    
    return songs

def get_next_song_id(songs):
    """获取下一个可用的歌曲ID"""
    if not songs:
        return 1
    max_id = max(song.get('id', 0) for song in songs)
    return max_id + 1

def add_song(songs):
    """添加新歌曲"""
    print("\n🎵 添加新歌曲 🎵")
    print("=" * 20)
    
    song_id = get_next_song_id(songs)
    song_name = input("请输入歌曲名: ").strip()
    if not song_name:
        print("歌曲名不能为空!")
        return songs
    
    artist = input("请输入歌手名 (可选): ").strip()
    url_list = input("请输入外链URL (可选): ").strip()
    
    # 显示当前点歌人列表
    requesters = get_all_requesters(songs)
    if requesters:
        print("\n📋 当前点歌人列表:")
        for i, requester in enumerate(requesters, 1):
            print(f"{i}. {requester}")
        print(f"{len(requesters) + 1}. 输入新点歌人")
    else:
        print("暂无点歌人，请输入新点歌人")
    
    try:
        choice = input("请选择点歌人编号或输入新点歌人: ").strip()
        if choice.isdigit():
            choice_num = int(choice)
            if 1 <= choice_num <= len(requesters):
                requested_by = requesters[choice_num - 1]
            elif choice_num == len(requesters) + 1:
                requested_by = input("请输入新点歌人姓名: ").strip()
                if not requested_by:
                    print("点歌人姓名不能为空!")
                    return songs
            else:
                print("无效的选择!")
                return songs
        else:
            requested_by = choice
            if not requested_by:
                print("点歌人姓名不能为空!")
                return songs
    except ValueError:
        print("请输入有效的选择!")
        return songs
    
    # 创建新歌曲
    new_song = {
        'id': song_id,
        'song_name': song_name,
        'artist': artist,
        'url_list': url_list,
        'requested_by': requested_by
    }
    
    songs.append(new_song)
    if save_songs(songs):
        print(f"成功添加歌曲: {song_name}")
        # 记录历史
        record_history("添加歌曲", f"歌曲: {song_name} - 歌手: {artist or '未知'} - 点歌人: {requested_by}")
    else:
        print("保存失败!")
        songs.pop()  # 移除刚刚添加的歌曲
    
    return songs

def modify_song(songs):
    """修改歌曲信息"""
    if not songs:
        print("没有可修改的歌曲!")
        return songs
    
    print("\n📝 修改歌曲信息 📝")
    print("=" * 25)
    
    # 显示歌曲列表
    for i, song in enumerate(songs, 1):
        print(f"{i}. {song.get('song_name', '未知')} - {song.get('artist', '未知')}")
    
    try:
        choice = int(input("\n请选择要修改的歌曲编号: ").strip())
        if 1 <= choice <= len(songs):
            song_to_modify = songs[choice - 1]
            
            print(f"\n当前歌曲信息:")
            print(f"歌曲名: {song_to_modify.get('song_name', '未知')}")
            print(f"歌手: {song_to_modify.get('artist', '未知')}")
            print(f"外链URL: {song_to_modify.get('url_list', '无')}")
            print(f"点歌人: {song_to_modify.get('requested_by', '未知')}")
            
            print("\n请选择要修改的内容:")
            print("1. 修改歌名")
            print("2. 修改歌手")
            print("3. 修改外链URL")
            print("4. 修改点歌人")
            print("5. 取消")
            
            mod_choice = input("请输入选项 (1-5): ").strip()
            
            if mod_choice == '1':
                new_name = input("请输入新的歌曲名: ").strip()
                if new_name:
                    song_to_modify['song_name'] = new_name
                    print("歌名修改成功!")
                    # 记录历史
                    record_history("修改歌曲", f"修改歌名: {song_to_modify.get('song_name', '未知')} -> {new_name}")
                else:
                    print("歌曲名不能为空!")
                    
            elif mod_choice == '2':
                new_artist = input("请输入新的歌手名: ").strip()
                old_artist = song_to_modify.get('artist', '未知')
                song_to_modify['artist'] = new_artist
                print("歌手修改成功!")
                # 记录历史
                record_history("修改歌曲", f"修改歌手: {old_artist} -> {new_artist}")
                
            elif mod_choice == '3':
                new_url = input("请输入新的外链URL: ").strip()
                old_url = song_to_modify.get('url_list', '无')
                song_to_modify['url_list'] = new_url
                print("外链URL修改成功!")
                # 记录历史
                record_history("修改歌曲", f"修改外链URL: {old_url} -> {new_url}")
                
            elif mod_choice == '4':
                requesters = get_all_requesters(songs)
                if requesters:
                    print("\n📋 当前点歌人列表:")
                    for i, requester in enumerate(requesters, 1):
                        print(f"{i}. {requester}")
                    print(f"{len(requesters) + 1}. 输入新点歌人")
                
                try:
                    req_choice = input("请选择点歌人编号或输入新点歌人: ").strip()
                    if req_choice.isdigit():
                        req_choice_num = int(req_choice)
                        if 1 <= req_choice_num <= len(requesters):
                            new_requester = requesters[req_choice_num - 1]
                            old_requester = song_to_modify.get('requested_by', '未知')
                            song_to_modify['requested_by'] = new_requester
                            print("点歌人修改成功!")
                            # 记录历史
                            record_history("修改歌曲", f"修改点歌人: {old_requester} -> {new_requester}")
                        elif req_choice_num == len(requesters) + 1:
                            new_requester = input("请输入新点歌人姓名: ").strip()
                            if new_requester:
                                old_requester = song_to_modify.get('requested_by', '未知')
                                song_to_modify['requested_by'] = new_requester
                                print("点歌人修改成功!")
                                # 记录历史
                                record_history("修改歌曲", f"修改点歌人: {old_requester} -> {new_requester}")
                            else:
                                print("点歌人姓名不能为空!")
                        else:
                            print("无效的选择!")
                    else:
                        if req_choice:
                            old_requester = song_to_modify.get('requested_by', '未知')
                            song_to_modify['requested_by'] = req_choice
                            print("点歌人修改成功!")
                            # 记录历史
                            record_history("修改歌曲", f"修改点歌人: {old_requester} -> {req_choice}")
                        else:
                            print("点歌人姓名不能为空!")
                except ValueError:
                    print("请输入有效的选择!")
                    
            elif mod_choice == '5':
                print("取消修改")
                return songs
            else:
                print("无效选项!")
                return songs
            
            # 保存修改
            if save_songs(songs):
                print("修改已保存!")
            else:
                print("保存失败!")
                
        else:
            print("无效的选择!")
    except ValueError:
        print("请输入有效的数字!")
    
    return songs

def delete_song(songs):
    """删除歌曲"""
    if not songs:
        print("没有可删除的歌曲!")
        return songs
    
    print("\n🗑️ 删除歌曲 🗑️")
    print("=" * 15)
    
    # 显示歌曲列表
    for i, song in enumerate(songs, 1):
        print(f"{i}. {song.get('song_name', '未知')} - {song.get('artist', '未知')}")
    
    try:
        choice = int(input("\n请选择要删除的歌曲编号: ").strip())
        if 1 <= choice <= len(songs):
            song_to_delete = songs[choice - 1]
            
            # 确认删除
            confirm = input(f"确定要删除歌曲 '{song_to_delete.get('song_name', '未知')}' 吗? (y/N): ").strip().lower()
            if confirm == 'y':
                del songs[choice - 1]
                if save_songs(songs):
                    print("歌曲删除成功!")
                    # 记录历史
                    record_history("删除歌曲", f"歌曲: {song_to_delete.get('song_name', '未知')} - 歌手: {song_to_delete.get('artist', '未知')} - 点歌人: {song_to_delete.get('requested_by', '未知')}")
                else:
                    print("保存失败!")
                    # 恢复删除的歌曲
                    songs.insert(choice - 1, song_to_delete)
            else:
                print("取消删除")
        else:
            print("无效的选择!")
    except ValueError:
        print("请输入有效的数字!")
    
    return songs

def manage_songs(songs):
    """歌曲管理菜单"""
    while True:
        print("\n🎵 歌曲管理 🎵")
        print("=" * 15)
        print("1. 添加歌曲")
        print("2. 修改歌曲")
        print("3. 删除歌曲")
        print("4. 查看所有歌曲")
        print("5. 返回主菜单")
        
        choice = input("请输入选项 (1-5): ").strip()
        
        if choice == '1':
            songs = add_song(songs)
        elif choice == '2':
            songs = modify_song(songs)
        elif choice == '3':
            songs = delete_song(songs)
        elif choice == '4':
            if songs:
                print("\n📋 所有歌曲列表:")
                for i, song in enumerate(songs, 1):
                    print(f"{i}. {song.get('song_name', '未知')} - {song.get('artist', '未知')} - {song.get('requested_by', '未知')}")
            else:
                print("暂无歌曲")
        elif choice == '5':
            break
        else:
            print("无效选项，请重新选择!")
    
    return songs

def switch_playlist():
    """切换当前歌单"""
    config = load_playlist_config()
    playlists = config['playlists']
    
    if len(playlists) <= 1:
        print("当前只有一个歌单，无法切换")
        return config, None
    
    print("\n🎵 歌单切换 🎵")
    print("=" * 20)
    print("当前歌单:", playlists[config['current_playlist']]['name'])
    print("\n可用歌单:")
    
    playlist_items = list(playlists.items())
    for i, (playlist_id, playlist_info) in enumerate(playlist_items, 1):
        print(f"{i}. {playlist_info['name']} ({playlist_info['song_count']}首歌曲)")
    
    try:
        choice = int(input("\n请选择要切换到的歌单编号: ").strip())
        if 1 <= choice <= len(playlist_items):
            selected_playlist_id = playlist_items[choice - 1][0]
            selected_playlist_name = playlist_items[choice - 1][1]['name']
            
            if selected_playlist_id == config['current_playlist']:
                print("已经是当前歌单!")
                return config, None
            
            config['current_playlist'] = selected_playlist_id
            if save_playlist_config(config):
                print(f"已切换到歌单: {selected_playlist_name}")
                # 记录历史
                record_history("切换歌单", f"从 {playlists[config['current_playlist']]['name']} 切换到 {selected_playlist_name}")
                # 重新加载歌曲列表
                songs = load_songs()

                print("歌曲列表重新加载成功!")
                stats = get_songs_statistics(songs)
                display_statistics(stats)
                return config, songs
            else:
                print("保存配置失败!")
        else:
            print("无效的选择!")
    except ValueError:
        print("请输入有效的数字!")
    
    return config, None

def create_playlist():
    """创建空白歌单"""
    config = load_playlist_config()
    
    print("\n🎵 创建空白歌单 🎵")
    print("=" * 20)
    
    playlist_name = input("请输入歌单名称: ").strip()
    if not playlist_name:
        print("歌单名称不能为空!")
        return config
    
    # 检查名称是否已存在
    for playlist_info in config['playlists'].values():
        if playlist_info['name'] == playlist_name:
            print("歌单名称已存在!")
            return config
    
    playlist_description = input("请输入歌单描述 (可选): ").strip()
    
    # 生成唯一的歌单ID
    playlist_id = f"playlist_{len(config['playlists']) + 1}"
    while playlist_id in config['playlists']:
        playlist_id = f"playlist_{len(config['playlists']) + 1}"
    
    # 创建歌单文件路径
    file_path = f"main_data/{playlist_id}.json"
    
    # 创建空的歌单文件
    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump({'songs': []}, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"创建歌单文件失败: {e}")
        return config
    
    # 添加到配置
    config['playlists'][playlist_id] = {
        'name': playlist_name,
        'description': playlist_description,
        'file_path': file_path,
        'created_at': datetime.datetime.now().strftime("%Y/%m/%d"),
        'song_count': 0
    }
    
    if save_playlist_config(config):
        print(f"成功创建歌单: {playlist_name}")
        # 记录历史
        record_history("创建歌单", f"歌单名称: {playlist_name}")
    else:
        print("保存配置失败!")
    
    return config

def delete_playlist():
    """删除歌单"""
    config = load_playlist_config()
    playlists = config['playlists']
    
    if len(playlists) <= 1:
        print("至少需要保留一个歌单!")
        return config
    
    print("\n🗑️ 删除歌单 🗑️")
    print("=" * 15)
    print("当前歌单:", playlists[config['current_playlist']]['name'])
    print("\n可用歌单:")
    
    playlist_items = list(playlists.items())
    for i, (playlist_id, playlist_info) in enumerate(playlist_items, 1):
        print(f"{i}. {playlist_info['name']} ({playlist_info['song_count']}首歌曲)")
    
    try:
        choice = int(input("\n请选择要删除的歌单编号: ").strip())
        if 1 <= choice <= len(playlist_items):
            selected_playlist_id = playlist_items[choice - 1][0]
            selected_playlist_name = playlist_items[choice - 1][1]['name']
            
            if selected_playlist_id == config['current_playlist']:
                print("不能删除当前正在使用的歌单!")
                return config
            
            # 确认删除
            confirm = input(f"确定要删除歌单 '{selected_playlist_name}' 吗? 此操作将永久删除所有歌曲数据! (y/N): ").strip().lower()
            if confirm == 'y':
                # 删除歌单文件
                file_path = playlists[selected_playlist_id]['file_path']
                try:
                    os.remove(file_path)
                except FileNotFoundError:
                    print(f"歌单文件不存在: {file_path}")
                except Exception as e:
                    print(f"删除歌单文件失败: {e}")
                
                # 从配置中移除
                del config['playlists'][selected_playlist_id]
                
                if save_playlist_config(config):
                    print(f"已删除歌单: {selected_playlist_name}")
                    # 记录历史
                    record_history("删除歌单", f"歌单名称: {selected_playlist_name}")
                else:
                    print("保存配置失败!")
            else:
                print("取消删除")
        else:
            print("无效的选择!")
    except ValueError:
        print("请输入有效的数字!")
    
    return config

def view_playlists():
    """查看所有歌单"""
    config = load_playlist_config()
    playlists = config['playlists']
    
    print("\n📋 所有歌单 📋")
    print("=" * 25)
    print(f"当前歌单: {playlists[config['current_playlist']]['name']}")
    print("\n歌单列表:")
    
    for playlist_id, playlist_info in playlists.items():
        current_marker = " ✅" if playlist_id == config['current_playlist'] else ""
        print(f"• {playlist_info['name']}{current_marker}")
        print(f"  描述: {playlist_info['description'] or '无'}")
        print(f"  歌曲数量: {playlist_info['song_count']}")
        print(f"  创建时间: {playlist_info['created_at']}")
        print()
    
    # 记录历史
    record_history("查看歌单", f"查看所有歌单信息，共{len(playlists)}个歌单")

def settings_menu():
    """设置菜单"""
    while True:
        config = load_playlist_config()
        current_playlist = config['playlists'][config['current_playlist']]['name']
        
        print(f"\n⚙️ 设置菜单 ⚙️ (当前歌单: {current_playlist})")
        print("=" * 30)
        print("1. 歌单管理")
        print("2. 自动网页跳转开关")
        print("3. 防重复功能设置")
        print("4. 返回主菜单")
        
        choice = input("请输入选项 (1-4): ").strip()
        
        if choice == '1':
            new_songs = playlist_management_menu()
            if new_songs is not None:
                # 返回新的歌曲列表给调用者
                return new_songs
        elif choice == '2':
            auto_jump_settings_menu()
        elif choice == '3':
            duplicate_prevention_settings_menu()
        elif choice == '4':
            break
        else:
            print("无效选项，请重新选择!")
    
    return None

def auto_jump_settings_menu():
    """自动网页跳转设置菜单"""
    while True:
        config = load_auto_jump_config()
        status = "✅ 启用" if config['auto_jump_enabled'] else "❌ 关闭"
        mode = "🌐 跳转URL" if config['jump_mode'] == 'url' else "🔍 搜索跳转"
        
        print(f"\n🌐 自动网页跳转设置 🌐")
        print("=" * 30)
        print(f"当前状态: {status}")
        print(f"跳转模式: {mode}")
        print(f"跳转延时: {config['jump_delay']}秒")
        if config['jump_mode'] == 'url' and config['custom_url']:
            print(f"自定义URL: {config['custom_url']}")
        print("\n请选择操作:")
        print("1. 启用自动跳转")
        print("2. 关闭自动跳转")
        print("3. 跳转模式设置")
        print("4. 返回设置菜单")
        
        choice = input("请输入选项 (1-4): ").strip()
        
        if choice == '1':
            config['auto_jump_enabled'] = True
            if save_auto_jump_config(config):
                print("✅ 自动跳转已启用")
                record_history("自动跳转设置", "启用自动网页跳转")
            else:
                print("保存配置失败!")
                
        elif choice == '2':
            config['auto_jump_enabled'] = False
            if save_auto_jump_config(config):
                print("❌ 自动跳转已关闭")
                record_history("自动跳转设置", "关闭自动网页跳转")
            else:
                print("保存配置失败!")
                
        elif choice == '3':
            jump_mode_menu()
            
        elif choice == '4':
            break
            
        else:
            print("无效选项，请重新选择!")

def jump_mode_menu():
    """跳转模式设置菜单"""
    while True:
        config = load_auto_jump_config()
        current_mode = config['jump_mode']
        
        print(f"\n🔧 跳转模式设置 🔧")
        print("=" * 25)
        print(f"当前模式: {'🌐 跳转URL' if current_mode == 'url' else '🔍 搜索跳转'}")
        print("\n请选择模式:")
        print("1. 跳转URL")
        print("2. 跳转搜索界面")
        print("3. 设置跳转延时")
        print("4. 返回上一级")
        
        choice = input("请输入选项 (1-4): ").strip()
        
        if choice == '1':
            config['jump_mode'] = 'url'
            # 设置自定义URL
            custom_url = input("请输入要跳转的URL (留空则不设置): ").strip()
            if custom_url:
                config['custom_url'] = custom_url
                if save_auto_jump_config(config):
                    print("✅ 已设置为跳转URL模式")
                    record_history("跳转模式设置", f"设置为跳转URL模式，URL: {custom_url}")
                else:
                    print("保存配置失败!")
            else:
                if save_auto_jump_config(config):
                    print("✅ 已设置为跳转URL模式 (未设置URL)")
                    record_history("跳转模式设置", "设置为跳转URL模式 (未设置URL)")
                else:
                    print("保存配置失败!")
                    
        elif choice == '2':
            config['jump_mode'] = 'search'
            if save_auto_jump_config(config):
                print("✅ 已设置为搜索跳转模式")
                record_history("跳转模式设置", "设置为搜索跳转模式")
            else:
                print("保存配置失败!")
                
        elif choice == '3':
            set_jump_delay()
            
        elif choice == '4':
            break
            
        else:
            print("无效选项，请重新选择!")

def set_jump_delay():
    """设置跳转延时"""
    config = load_auto_jump_config()
    
    print(f"\n⏰ 当前跳转延时: {config['jump_delay']}秒")
    print("请输入新的跳转延时 (1-60秒):")
    
    try:
        delay = int(input("延时秒数: ").strip())
        if 1 <= delay <= 60:
            config['jump_delay'] = delay
            if save_auto_jump_config(config):
                print(f"✅ 跳转延时已设置为 {delay}秒")
                record_history("跳转延时设置", f"设置跳转延时为 {delay}秒")
            else:
                print("保存配置失败!")
        else:
            print("延时必须在1-60秒之间!")
    except ValueError:
        print("请输入有效的数字!")

def import_external_playlist():
    """从外部已有歌单导入"""
    print("\n🎵 从外部已有歌单导入 🎵")
    print("=" * 25)
    
    # 获取外部歌单文件路径
    external_file_path = input("请输入外部歌单文件路径 (支持JSON格式): ").strip()
    if not external_file_path:
        print("文件路径不能为空!")
        return
    
    # 检查文件是否存在
    if not os.path.exists(external_file_path):
        print(f"文件不存在: {external_file_path}")
        return
    
    try:
        # 读取外部歌单文件
        with open(external_file_path, 'r', encoding='utf-8') as f:
            external_data = json.load(f)
        
        # 检查文件格式
        if 'songs' not in external_data:
            print("文件格式错误: 缺少 'songs' 字段")
            return
        
        external_songs = external_data['songs']
        if not isinstance(external_songs, list):
            print("文件格式错误: 'songs' 字段应该是一个列表")
            return
        
        print(f"成功读取外部歌单，共 {len(external_songs)} 首歌曲")
        
        # 创建新歌单
        config = load_playlist_config()
        
        playlist_name = input("请输入新歌单名称: ").strip()
        if not playlist_name:
            print("歌单名称不能为空!")
            return
        
        # 检查名称是否已存在
        for playlist_info in config['playlists'].values():
            if playlist_info['name'] == playlist_name:
                print("歌单名称已存在!")
                return
        
        playlist_description = input("请输入歌单描述 (可选): ").strip()
        
        # 生成唯一的歌单ID
        playlist_id = f"playlist_{len(config['playlists']) + 1}"
        while playlist_id in config['playlists']:
            playlist_id = f"playlist_{len(config['playlists']) + 1}"
        
        # 创建歌单文件路径 - 使用基于脚本目录的绝对路径
        script_dir = os.path.dirname(os.path.abspath(__file__))
        main_data_dir = os.path.join(os.path.dirname(script_dir), 'main_data')
        file_path = os.path.join(main_data_dir, f"{playlist_id}.json")
        
        # 确保main_data目录存在
        os.makedirs(main_data_dir, exist_ok=True)
        
        # 保存导入的歌曲到新歌单
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump({'songs': external_songs}, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"创建歌单文件失败: {e}")
            return
        
        # 添加到配置 - 使用相对路径存储
        config['playlists'][playlist_id] = {
            'name': playlist_name,
            'description': playlist_description,
            'file_path': f"main_data/{playlist_id}.json",
            'created_at': datetime.datetime.now().strftime("%Y/%m/%d"),
            'song_count': len(external_songs)
        }
        
        if save_playlist_config(config):
            print(f"✅ 成功导入外部歌单: {playlist_name} ({len(external_songs)}首歌曲)")
            # 记录历史
            record_history("导入外部歌单", f"歌单名称: {playlist_name} - 歌曲数量: {len(external_songs)} - 来源文件: {external_file_path}")
        else:
            print("保存配置失败!")
            
    except json.JSONDecodeError:
        print("文件格式错误: 不是有效的JSON文件")
    except Exception as e:
        print(f"导入失败: {e}")

def duplicate_prevention_settings_menu():
    """防重复功能设置菜单"""
    config = load_playlist_config()
    current_playlist_id = config['current_playlist']
    prevention_config = config['playlists'][current_playlist_id]['duplicate_prevention']
    
    while True:
        status = "✅ 启用" if prevention_config['enabled'] else "❌ 关闭"
        mode = "⏰ 时间窗口模式" if prevention_config['mode'] == 'time_window' else "❓ 未知模式"
        time_window = f"{prevention_config['time_window_hours']}小时{prevention_config['time_window_minutes']}分钟"
        reset_status = "✅ 是" if prevention_config['reset_on_all_played'] else "❌ 否"
        played_count = len(prevention_config['played_songs'])
        
        print(f"\n🔄 防重复功能设置 🔄 (当前歌单: {config['playlists'][current_playlist_id]['name']})")
        print("=" * 50)
        print(f"1. 功能状态: {status}")
        print(f"2. 模式: {mode}")
        print(f"3. 时间窗口: {time_window}")
        print(f"4. 所有歌曲播放后重置: {reset_status}")
        print(f"5. 当前已播放歌曲: {played_count}首")
        print(f"6. 查看播放记录")
        print(f"7. 手动重置播放记录")
        print(f"8. 返回设置菜单")
        print("输入相应数字以显示更多信息/操作")
        
        choice = input("\n请选择操作 (1-8): ").strip()
        
        if choice == '1':
            # 切换启用状态
            prevention_config['enabled'] = not prevention_config['enabled']
            if save_playlist_config(config):
                status = "启用" if prevention_config['enabled'] else "关闭"
                print(f"✅ 防重复功能已{status}")
                record_history("防重复设置", f"{status}防重复功能")
            else:
                print("保存配置失败!")
                
        elif choice == '2':
            # 切换模式
            if prevention_config['mode'] == 'time_window':
                prevention_config['mode'] = 'time_window'  # 目前只有一种模式
                print("当前只有时间窗口模式可用")
            else:
                prevention_config['mode'] = 'time_window'
                print("已设置为时间窗口模式")
            
            if save_playlist_config(config):
                record_history("防重复设置", "设置防重复模式")
                
        elif choice == '3':
            # 设置时间窗口
            print(f"\n⏰ 当前时间窗口: {prevention_config['time_window_hours']}小时{prevention_config['time_window_minutes']}分钟")
            print("请输入新的时间窗口设置:")
            
            try:
                hours = int(input("小时 (0-999999999): ").strip())
                minutes = int(input("分钟 (0-59): ").strip())
                
                if 0 <= hours <= 999999999 and 0 <= minutes <= 59:
                    prevention_config['time_window_hours'] = hours
                    prevention_config['time_window_minutes'] = minutes
                    
                    if save_playlist_config(config):
                        print(f"✅ 时间窗口已设置为 {hours}小时{minutes}分钟")
                        record_history("防重复设置", f"设置时间窗口: {hours}小时{minutes}分钟")
                    else:
                        print("保存配置失败!")
                else:
                    print("时间范围无效! 小时: 0-999999999, 分钟: 0-59")
            except ValueError:
                print("请输入有效的数字!")
                
        elif choice == '4':
            # 切换重置设置
            prevention_config['reset_on_all_played'] = not prevention_config['reset_on_all_played']
            if save_playlist_config(config):
                status = "启用" if prevention_config['reset_on_all_played'] else "关闭"
                print(f"✅ 所有歌曲播放后重置已{status}")
                record_history("防重复设置", f"{status}所有歌曲播放后重置")
            else:
                print("保存配置失败!")
                
        elif choice == '5':
            # 显示当前播放统计
            songs = load_songs()
            total_songs = len(filter_valid_songs(songs))
            played_count = len(prevention_config['played_songs'])
            print(f"\n📊 播放统计:")
            print(f"总歌曲数: {total_songs}")
            print(f"已播放歌曲: {played_count}")
            print(f"剩余歌曲: {total_songs - played_count}")
            
        elif choice == '6':
            # 查看播放记录
            if not prevention_config['played_songs']:
                print("暂无播放记录")
            else:
                print("\n📜 播放记录:")
                print("=" * 60)
                for i, record in enumerate(prevention_config['played_songs'][-50:], 1):  # 显示最近50条
                    print(f"{i}. [{record['play_time']}] {record['song_name']} (ID: {record['song_id']})")
                if len(prevention_config['played_songs']) > 50:
                    print(f"... 还有 {len(prevention_config['played_songs']) - 50} 条记录")
                    
        elif choice == '7':
            # 手动重置播放记录
            confirm = input("确定要手动重置播放记录吗? 这将清除所有播放历史! (y/N): ").strip().lower()
            if confirm == 'y':
                prevention_config['played_songs'] = []
                prevention_config['last_reset_time'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                if save_playlist_config(config):
                    print("✅ 播放记录已重置")
                    record_history("防重复设置", "手动重置播放记录")
                else:
                    print("保存配置失败!")
            else:
                print("取消重置")
                
        elif choice == '8':
            break
            
        else:
            print("无效选项，请重新选择!")

def playlist_management_menu():
    """歌单管理菜单"""
    while True:
        print("\n🎵 歌单管理 🎵")
        print("=" * 15)
        print("1. 从外部已有歌单导入")
        print("2. 创建空白歌单")
        print("3. 删除歌单")
        print("4. 切换歌单")
        print("5. 查看所有歌单")
        print("6. 返回设置菜单")
        
        choice = input("请输入选项 (1-6): ").strip()
        
        if choice == '1':
            import_external_playlist()
        elif choice == '2':
            create_playlist()
        elif choice == '3':
            delete_playlist()
        elif choice == '4':
            config, new_songs = switch_playlist()
            if new_songs is not None:
                # 返回新的歌曲列表给调用者
                return new_songs
        elif choice == '5':
            view_playlists()
        elif choice == '6':
            break
        else:
            print("无效选项，请重新选择!")
    
    return None

def main():
    """主函数"""
    print("🎵 随机点歌系统 🎵")
    print("正在加载歌曲列表...")
    
    songs = load_songs()
    if not songs:
        print("没有找到任何歌曲，程序退出")
        return
    
    # 显示统计信息
    stats = get_songs_statistics(songs)
    display_statistics(stats)
    
    while True:
        print("\n请选择操作:")
        print("1. 随机点歌")
        print("2. 重新加载歌曲列表")
        print("3. 查看统计信息")
        print("4. 点歌人管理")
        print("5. 歌曲管理")
        print("6. 查看历史记录")
        print("7. 设置")
        print("8. 退出")
        
        choice = input("请输入选项 (1-8): ").strip()
        
        if choice == '1':
            random_song = get_random_song(songs)
            display_song_info(random_song)
            
        elif choice == '2':
            songs = load_songs()
            if songs:
                print("歌曲列表重新加载成功!")
                stats = get_songs_statistics(songs)
                display_statistics(stats)
            else:
                print("重新加载失败!")
                
        elif choice == '3':
            stats = get_songs_statistics(songs)
            display_statistics(stats)
            
        elif choice == '4':
            songs = manage_requesters(songs)
            
        elif choice == '5':
            songs = manage_songs(songs)
            
        elif choice == '6':
            view_history()
            
        elif choice == '7':
            new_songs = settings_menu()
            if new_songs is not None:
                songs = new_songs
                print("歌单已切换，歌曲列表已更新!")
                stats = get_songs_statistics(songs)
                display_statistics(stats)
            
        elif choice == '8':
            print("天空属于哈夫克~！")
            break
            
        else:
            print("无效选项，请重新选择!")

if __name__ == "__main__":
    main()
    input("\n按回车键退出程序...")
