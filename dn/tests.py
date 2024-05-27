import psutil

# 列出所有正在运行的进程及其CPU和内存使用情况
for proc in psutil.process_iter(['pid', 'name', 'username']):
    p = psutil.Process(proc.info['pid'])
    print(f"PID: {proc.info['pid']}, Name: {proc.info['name']}, User: {proc.info['username']}")
    print(f"  CPU: {p.cpu_percent()}%, Memory: {p.memory_info().rss / 1024 ** 2:.2f} MB")