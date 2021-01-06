from io import BytesIO
import base64

import qrcode

from .iface import IQRCode


class Zbp2d(IQRCode):
    """
    Done with
    https://zbp.pl/public/repozytorium/dla_bankow/rady_i_komitety/bankowosc_elektroczniczna/rada_bankowosc_elektr/zadania/2013.12.03_-_Rekomendacja_-_Standard_2D.pdf
    required:
    [Plugins]
    invoice_numbering = <plugin of choice>
    [QRCode]
    country_iso = <Country ISO code as two, three letters>
    """
    def __init__(self, options, data: dict):
        super(IQRCode, self).__init__()

        amount = data['total'].replace('.', '')
        companyname = data['companyname']
        invoice = data['invoice_number']
        #
        if len(str(options.taxpayerid)) > 10:
            raise ValueError('to long taxpayerid')
        _len = len(options.country_iso)
        if _len < 2 or 3 < _len:
            raise ValueError(f'Country code should be 2 characters wide {options.country_iso} {len(options.country_iso)}')
        _len = len(options.account_number)
        if _len < 22 or 26 < _len:
            raise ValueError('range 22 to 26')
        if len(invoice) > 32:
            raise ValueError('to long invoice id')

        self.to_qrcode = f"\
{options.taxpayerid}|\
{options.country_iso}|\
{options.account_number}|\
{amount}|\
{companyname}|\
{invoice}|\
|\
|"


def get():
    return Zbp2d

