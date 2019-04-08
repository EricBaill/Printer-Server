# import qrcode
# img = qrcode.make('欧帆姐姐')
# img.save('./simpleqrcode.jpg')

import qrcode
qr=qrcode.QRCode(version = 2,error_correction = qrcode.constants.ERROR_CORRECT_L,box_size=10,border=10,)
qr.add_data('窗前明月光')
qr.make(fit=True)
img = qr.make_image()
# img.show()
img.save('./二维码.jpg')