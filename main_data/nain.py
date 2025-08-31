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
                for i, record in enumerate(reversed(history_data), 1):
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

def load_songs():
    """加载歌曲列表文件"""
    # 在多个可能的位置查找songs_list.json
    possible_paths = [
        'songs_list.json',  # 当前目录
        '../songs_list.json',  # 父目录
        './main_data/songs_list.json',  # main_data子目录
        'main_data/songs_list.json'  # main_data子目录
    ]
    
    for json_path in possible_paths:
        try:
            with open(json_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                print(f'成功加载歌曲列表: {json_path}')
                return data.get('songs', [])
        except FileNotFoundError:
            continue
        except json.JSONDecodeError:
            print(f'歌曲列表文件已损坏，请检查文件格式: {json_path}')
            return []
    
    print('歌曲列表文件不存在，请先创建歌曲列表')
    return []

def save_songs(songs):
    """保存歌曲列表到文件"""
    json_path = 'songs_list.json'
    try:
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump({'songs': songs}, f, ensure_ascii=False, indent=2)
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

def get_random_song(songs):
    """随机选择一首歌曲"""
    if not songs:
        return None
    
    valid_songs = filter_valid_songs(songs)
    if not valid_songs:
        return None
    
    return random.choice(valid_songs)

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
        print("7. 退出")
        
        choice = input("请输入选项 (1-7): ").strip()
        
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
            print("天空属于哈夫克~！")
            break
            
        else:
            print("无效选项，请重新选择!")

if __name__ == "__main__":
    main()
    input("\n按回车键退出程序...")
