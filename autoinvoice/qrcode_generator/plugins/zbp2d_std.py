from io import BytesIO
import base64

import qrcode

from .iface import IQRCode


class QRCode_zbp2d(IQRCode):
    """
    Done with
    https://zbp.pl/public/repozytorium/dla_bankow/rady_i_komitety/bankowosc_elektroczniczna/rada_bankowosc_elektr/zadania/2013.12.03_-_Rekomendacja_-_Standard_2D.pdf
    """
    def __init__(self, options, data: dict):
        super(IQRCode, self).__init__()

        amount = data['total'].replace('.','')
        companyname = data['companyname']
        invoice = data['invoice_number']
        #
        if len(str(options.taxpayerid)) > 10:
            raise ValueError('to long taxpayerid')
        if len(options.QRCode.country_iso) > 2:
            raise ValueError('Country code should be 2 characters wide')
        if 22 > len(options.QRCode.accountnumber) < 26:
            raise ValueError('range 22 to 26')
        if len(amount) > 6:
            raise ValueError('to high amount for this operation')
        if len(companyname) > 20:
            raise ValueError('to long company name')
        if len(invoice) > 32:
            raise ValueError('to long invoice id')

        self.to_qrcode = f"\
{options.taxpayerid}|\
{options.QRCode.country_iso}|\
{options.QRCode.accountnumber}|\
{amount}|\
{companyname}|\
{invoice}|\
|\
|"


def get():
    return QRCode_zbp2d

