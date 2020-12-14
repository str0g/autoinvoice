from io import BytesIO
import base64

import qrcode


class QRCode_zbp2d:
    def __init__(self, data: dict):
        self.taxpayerid = data['ref_taxpayerid']
        self.country = data['country_iso']
        self.accountnum = data['ref_accountnumber']
        self.amount = data['amount'].replace('.','')
        self.companyname = data['ref_companyname']
        self.invoice = data['invoice_number']
        #
        assert(not (len(self.taxpayerid) > 10))
        assert(not (len(self.country) > 2))
        assert(not (len(self.accountnum) > 26))
        assert(not (len(self.amount) > 6))
        assert(not (len(self.companyname) > 20))
        assert(not (len(self.invoice) > 32))

    def __call__(self) -> dict:
        tmp = f"\
{self.taxpayerid}|\
{self.country}|\
{self.accountnum}|\
{self.amount}|\
{self.companyname}|\
{self.invoice}|\
|\
|"
        qr = qrcode.make(tmp)
        io = BytesIO()
        #qr.save('test_qr.png')
        qr.save(io, format='png')
        io.seek(0)
        b64 = base64.b64encode(io.getvalue())

        return {'qrcode': b64}


def get():
    return QRCode_zbp2d

