#导入模块
import subprocess
import time

# 启动程序
process = subprocess.Popen(
    ['python', 'main_data/main.py'],
    stdin=subprocess.PIPE,
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
    text=True
)

# 等待程序初始化
time.sleep(1)

# 发送命令序列来测试歌单切换
commands = [
    "7\n",  # 进入设置菜单
    "1\n",  # 选择歌单管理
    "3\n",  # 选择切换歌单
    "2\n",  # 选择第二个歌单（内定qwb）
    "5\n",  # 返回设置菜单
    "4\n",  # 返回主菜单
    "1\n",  # 随机点歌（应该使用新歌单的歌曲）
    "8\n"   # 退出
]

for cmd in commands:
    process.stdin.write(cmd)
    process.stdin.flush()
    time.sleep(0.5)

# 获取输出
stdout, stderr = process.communicate()
print("程序输出:")
print(stdout)
if stderr:
    print("错误输出:")
    print(stderr)
