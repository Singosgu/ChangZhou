import win32print, win32api

printers = win32print.EnumPrinters(win32print.PRINTER_ENUM_LOCAL | win32print.PRINTER_ENUM_CONNECTIONS)

printer_data = []
for printer in range(len(printers)):
    print(printers[printer][2])
    if printers[printer][2].startswith('TSC'):
        hPrinter = win32print.OpenPrinter(printers[printer][2])
        # win32print.SetDefaultPrinter(hPrinter)
        # printer_info = win32print.GetPrinter(hPrinter, 2)
        # printer_name = printer_info['pPrinterName']
        # driver_name = printer_info['pDriverName']
        # location = printer_info['pLocation']
        # attributes = printer_info['Attributes']
        filename = "1.pdf"
        try:
            hJob = win32print.StartDocPrinter(hPrinter, 1, ('PrintJobName', None, 'RAW'))
            try:
                handle = hPrinter.handle
                tasks = win32print.EnumJobs(handle, 0, -1, 1)
                for task in tasks:
                    taskName = task["pDocument"]
                    print(taskName)
                win32print.SetDefaultPrinter(printers[printer][2])
                win32api.ShellExecute(0, "print", filename, None, ".", 1)
                # win32print.StartPagePrinter(hPrinter)
                # win32print.WritePrinter(hPrinter, "RAW")  # Instead of raw text is there a way to print PDF File ?
                # win32print.EndPagePrinter(hPrinter)
            finally:
                win32print.EndDocPrinter(hPrinter)
        finally:
            win32print.ClosePrinter(hPrinter)

        # printer_data.append({
        #     'Printer Name': printer_name,
        #     'Driver Name': driver_name,
        #     'Location': location,
        #     'Attributes': attributes
        # })


# 获取默认打印机
# default_printer = win32print.GetPrinter()
# print(default_printer)

# 连接到打印机
# printer = win32print.OpenPrinter(default_printer)

# 打印文档
# win32print.StartDocPrinter(printer, 1, ('My Document', None, 'TEXT'))
# win32print.StartPagePrinter(printer)
# win32print.WritePrinter(printer, 'Hello, World!')
# win32print.EndPagePrinter(printer)
# win32print.EndDocPrinter(printer)

# 关闭打印机连接
# win32print.ClosePrinter(printer)