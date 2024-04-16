import usb.core
import usb.util

# 替换以下VID和PID为你的打印机的实际值
VID = '0xXXXX'
PID = '0xXXXX'

# 找到打印机设备
dev = usb.core.find(idVendor=VID, idProduct=PID)

# 确保设备已经找到
if dev is None:
    raise ValueError('打印机未发现')

# 打开设备
dev.set_configuration()

# 需要发送到打印机的数据
data = b'Hello, USB Printer!'

# 发送数据到打印机（这里的接口号和端点需要根据你的打印机进行调整）
interface = dev[0]
endpoint = interface[0]
res = endpoint.write(data)

if res != len(data):
    raise ValueError('数据发送失败')

print('数据已发送到打印机')