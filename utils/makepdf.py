import traceback
from traceback import format_exc

import barcode
from barcode.codex import Code128
from barcode.writer import ImageWriter
import os
from django.conf import settings
from fpdf import FPDF

data = [{
    'id': 1,
    'patch_number': 'WH21-Z-2225-1',
    'brand': 'MADE IN CHINA',
    'barcode': '876e09fb76428b0beede86fbefe3a866',
    'total': 5,
    'goods_code': 'AT-68',
    'address': 'EA',
    'country': 'US',
},{
    'id': 2,
    'patch_number': 'WH21-Z-3333-5',
    'brand': 'MADE IN CHINA',
    'barcode': '12d81a624d62d77e1eb057c118c95141',
    'total': 10,
    'goods_code': 'AT-50',
    'address': 'BO',
    'country': 'AS',
},
]

base_dir = os.path.join(settings.BASE_DIR, 'media/asn_label/')

class Draw:
    def __init__(self, data, pdf_file_name):
        self.data = data
        self.pdf_file_name = pdf_file_name
        self.pdf = FPDF(format=(83, 48))
        self.pdf.set_auto_page_break(False)
        self.pdf.set_display_mode('real', 'default')

    def draw_barcode(self, patch_number, code):
        folder = os.path.join(base_dir, patch_number)
        if not os.path.exists(folder):
            os.mkdir(folder)
        ph = os.path.join(folder, f'{code}')
        if os.path.exists(f"{ph}.png"):
            return f"{ph}.png"
        CODE128 = barcode.get_barcode_class('code128')
        # CODE128 = Code128
        bc = CODE128(code, writer=ImageWriter())
        opt = {'write_text': False, 'quiet_zone': 2, 'text_distance': 10}
        bc.save(ph, opt)
        return f"{ph}.png"

    def generate(self, data_index, page_number, page_data, barcode_path):
        # 绘制矩形
        self.pdf.rect(1, 1, self.pdf.w - 2, self.pdf.h - 2, )
        self.pdf.t_margin = 0
        self.pdf.b_margin = 0
        self.pdf.y = 3
        # 第一行内容
        self.pdf.set_font('arial', 'B', 22)
        self.pdf.cell(20, 8, f"{page_data.get('country')}")
        # 第一行中间文字
        self.pdf.set_fill_color(0, 0, 0)
        self.pdf.set_text_color(255, 255, 255)
        self.pdf.set_font('arial', '', 22)
        self.pdf.cell(20, 8, f"{data_index}", fill=True, align='C')
        # 第一行最后文字
        self.pdf.set_fill_color(255, 255, 255)
        self.pdf.set_text_color(0, 0, 0)
        self.pdf.set_font('arial', 'B', 22)
        self.pdf.cell(0, 8, f"{page_data.get('address')}", align="R")
        # 第二行
        self.pdf.ln(9)
        self.pdf.set_font('arial', 'B', 20)
        self.pdf.cell(0, 8, f"{page_data.get('patch_number')}", fill=True, align='C')
        # 第三行
        self.pdf.ln()
        self.pdf.image(barcode_path, 5, 20, 73, h=10, type='png')
        # 第四行
        self.pdf.ln(12)
        self.pdf.set_font('arial', '', 18)
        self.pdf.cell(0, 8, f"{page_data.get('goods_code')}", align="C")
        # 第五行
        self.pdf.ln()
        self.old_pdf_l_margin = self.pdf.l_margin
        self.old_pdf_r_margin = self.pdf.r_margin
        self.old_pdf_x = self.pdf.x
        self.pdf.x = 3
        self.pdf.r_margin = 3
        self.pdf.l_margin = 0
        self.pdf.set_font('arial', '', 14)
        # self.pdf.cell(0, 8, f"{page_number}/{page_data.get('total')}")
        self.pdf.cell(0, 8, f"{page_data.get('brand')}", align="R")
        self.pdf.l_margin = self.old_pdf_l_margin
        self.pdf.r_margin = self.old_pdf_r_margin
        self.pdf.x = self.old_pdf_x
        # self.pdf.cell(3, 0, f"{data_index}", align='R')
        # self.pdf.cell(5, 0, f"{data_index}", align='')
        # self.pdf.cell(0, 0, f"{page_data.get('country')}", align='R')
        # pdf.set_font('simsunb', '', 20)
        # pdf.cell(40, 10, 'Hello, World!')

    def main(self):
        for data_index, ele in enumerate(self.data):
            # 生成对应的二维码
            barcode_path = self.draw_barcode(ele.get('patch_number'), ele.get('goods_code'))
            for page_number, page in enumerate(range(ele.get('total'))):
                self.pdf.add_page()
                self.generate(data_index + 1, page_number + 1, page_data=ele, barcode_path=barcode_path)
        self.pdf.output(self.pdf_file_name, 'F')
