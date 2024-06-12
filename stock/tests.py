import pandas as pd

# 创建一个DataFrame
data = {
    'Column1': [1, 2, 3, 4],
    'Column2': ['A', 'B', 'C', 'D']
}
df = pd.DataFrame(data)

# 将DataFrame写入Excel文件
df.to_excel('output.xlsx', index=False)