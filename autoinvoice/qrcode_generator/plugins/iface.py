from io import BytesIO
import base64

import qrcode


class IQRCode:
    def __init__(self):
        self.to_qrcode = ''

    def __call__(self) -> dict:
        qr = qrcode.make(self.to_qrcode)
        io = BytesIO()
        #qr.save('test_qr.png')
        qr.save(io, format='png')
        io.seek(0)
        b64 = base64.b64encode(io.getvalue()).decode('utf-8')

        return {'qrcode': b64}


def get() -> IQRCode:
    raise NotImplemented
    # Suppose to return class not allocation
    # return IQRCode
