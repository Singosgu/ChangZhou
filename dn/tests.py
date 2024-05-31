from PIL import Image, ImageDraw, ImageFont
import qrcode

qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=10, border=4)
data = "Hello, World!"
qr.add_data(data)
qr.make(fit=True)
img = qr.make_image(fill_color="black", back_color="white")
img.save("qrcode.png")
image = Image.open('qrcode.png')
resized_image = image.resize((150, 150))
resized_image.save('new_qrcode.png')


width, height = 350, 525
image = Image.new('RGB', (width, height), color='white')
draw = ImageDraw.Draw(image)

font = ImageFont.truetype('ChillRoundGothic_Medium.ttf', 20, encoding="unic")
draw.text((20, 30), "TxnID：", font=font, fill='black', spacing=800)
draw.text((20, 50), "26-11616-09560", font=font, fill='black')
draw.text((20, 70), "拣货员：", font=font, fill='black')
draw.text((20, 90), "张三", font=font, fill='black')

draw.text((20, 160), "库位名", font=font, fill='black')
draw.text((20, 190), "X01", font=font, fill='black')

draw.text((225, 160), "待件货数量", font=font, fill='black')
draw.text((225, 190), "3", font=font, fill='black')

image.save('test.png')

base_image = Image.open('test.png')
overlay_image = Image.open("new_qrcode.png")
base_image.paste(overlay_image, (200, 0))
base_image.save('example.png')