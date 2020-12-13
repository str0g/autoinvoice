from io import BytesIO
import base64

import qrcode

class QRCode:
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
        qr = qrcode.make(tmp, error_correction=qrcode.constants.ERROR_CORRECT_L)
        io = BytesIO()
        #qr.save('test_qr.png')
        qr.save(io, format='png')
        io.seek(0)
        b64 = base64.b64encode(io.getvalue())

        if True:
            import numpy
            print('qr:', qr)
            print('io:', io)
            print('b64:', b64)

        return {'qrcode': b64}
 
def get_qrcode(data: dict) -> dict:
    #return QRCode(data)()
    tmp = f"\
{data['ref_taxpayerid']}\
|{data['country_iso']}\
|{data['ref_accountnumber']}\
|{data['amount'].replace('.','')}\
|{data['ref_companyname']}\
|{data['invoice_number']}\
|\
|\
|"
    qr = qrcode.make(tmp, error_correction=qrcode.constants.ERROR_CORRECT_L)
    io = BytesIO()
    qr.save('test_qr.png')
    qr.save(io, format='png')
    io.seek(0)
    b64 = base64.b64encode(io.getvalue())
    if True:
        import numpy
        print('qr:', qr)
        print('io:', io)
        print('b64:', b64)
    #    print('QRCode shape:', numpy.array(qr.get_matrix()).shape)
    return {'qrcode': b64}

