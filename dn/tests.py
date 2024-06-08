import img2pdf
import glob
import os

# 输出的PDF文件名
output_pdf_path = 'output.pdf'

# 获取所有JPG文件路径
jpg_files = glob.glob('1.jpg')

# 读取JPG文件并转换为PDF
with open(output_pdf_path, 'wb') as f:
    f.write(img2pdf.convert(jpg_files))

print(f'PDF file "{output_pdf_path}" created.')