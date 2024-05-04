import subprocess

# 运行一个简单的命令，如ipconfig，并且打开cmd窗口
result = subprocess.run('ipconfig', shell=False)