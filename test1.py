import win32print
import win32api
import time


class PrintPDF:
    def __init__(self, desc=False):
        self.files = '1.pdf'
        printers = win32print.EnumPrinters(win32print.PRINTER_ENUM_LOCAL | win32print.PRINTER_ENUM_CONNECTIONS)
        for printer in range(len(printers)):
            if printers[printer][2].startswith('TSC'):
                self.print_name = printers[printer][2]
                self.handle = win32print.OpenPrinter(self.print_name)
                self.sort_file_by_time(desc)
                print(f"打印完毕，本次共打印{len(self.files)}个文件")

    def sort_file_by_time(self, desc):
        file_dict = dict()
        for file in self.files:
            print(file)
            file_dict[file] = file.stat().st_mtime
        res = sorted(file_dict.keys(), key=file_dict.get, reverse=desc)
        print("开始打印------")
        for r in res:
            print("正在打印：", r)
            self.print_file(r)

    def print_file(self, file):
        file = str(file)
        win32api.ShellExecute(0, "print", file, '/d:"%s"' % self.print_name, ".", 0)
        time.sleep(2)
        tasks = win32print.EnumJobs(self.handle, 0, -1, 1)
        if tasks:
            print("打印阻塞，请稍等")
        while tasks:
            time.sleep(1)
            tasks = win32print.EnumJobs(self.handle, 0, -1, 1)


if __name__ == '__main__':
    my_pdf_printer = PrintPDF()