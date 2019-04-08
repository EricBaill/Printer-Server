# import qrcode
# from PIL import Image
#
# url = "www.zhuanzhuan.com"
# qr = qrcode.QRCode(
#     version=2,
#     error_correction=qrcode.constants.ERROR_CORRECT_L,
#     box_size=8,
#     border=2
# )
# qr.add_data(url)
# qr.make(fit=True)
# img = qr.make_image()
# img = img.convert("RGBA")
# icon = Image.open("./logo.png")
# img_w, img_h = img.size
# factor = 4
# size_w = int(img_w / factor)
# size_h = int(img_h / factor)
#
# icon_w, icon_h = icon.size
# if icon_w > size_w:
#     icon_w = size_w
# if icon_h > size_h:
#     icon_h = size_h
# icon = icon.resize((icon_w, icon_h), Image.ANTIALIAS)
#
# w = int((img_w - icon_w) / 2)
# h = int((img_h - icon_h) / 2)
# img.paste(icon, (w, h), icon)
#
# img.save("./test.png")

import qrcode
if __name__ == "__main__":
    url = "https://zhuanlan.zhihu.com/python2018"
    print(url)
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )

    qr.add_data(url)
    qr.make(fit=True)

    img = qr.make_image()
    img.show()