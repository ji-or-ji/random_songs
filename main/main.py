
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
from main.history_part import record_history
from main.history_part import view_history
# from main.list_save_and_load_part import save_songs
from main.list_save_and_load_part import load_songs
from main.list_save_and_load_part import get_songs_statistics
from main.list_save_and_load_part import display_statistics
from main.get_random_song_part import get_random_song
# from main.config_part import save_playlist_config

###
def display_song_info(song):
    """显示歌曲信息"""
    if not song:
        print("没有找到有效的歌曲")
        return

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


###例行公事
def main():
    pass
if __name__ == '__main__':
    main() 
    input("\n按回车键退出程序...")
###