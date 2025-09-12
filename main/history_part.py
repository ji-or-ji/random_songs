# 导入模块
import json
import os
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
