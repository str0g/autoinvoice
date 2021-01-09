from os.path import expanduser

from autoinvoice import configs

default_configs_string = f"""\
[Common]
url = 
key = 

[Plugins]
mod_company_register = apiregon2
mod_invoice_numbering = 
mod_qrcodes = 

[Paths]
database = {expanduser('~/.autoinvoice/dbase.db')}
template = /usr/share/polishinvoice/templates/simple.tex

[Refere]
taxpayerid = 
name = 
account_number = 

[Options]

"""

def set_default_config():
    configs.config.set('Refere', 'taxpayerid', '5222680297')
    configs.config.set('Refere', 'account_number', '93114020040000320300621961')
    #
    #configs.config.set('QRCode', 'country_iso', 'PL')
    #
