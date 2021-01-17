from os.path import expanduser

class ConfigurationCreator:
    def __init__(self, input_options: dict = None):
        self.input_options = {
            'url': '',
            'key': '',
            'mod_invoice_numbering': '',
            'mod_qrcodes': '',
            'taxpayerid': '',
            'name': '',
            'account_number': '',
            'register': 'apiregon',
            'database': expanduser('~/.autoinvoice/dbase.db'),
            'template': '/usr/share/polishinvoice/templates/simple.tex',
            'verbose': False,
            'email': ''
        }
        if input_options:
            self.input_options.update(input_options)
        self.config_template = '''\
[Common]
url = {url}
key = {key}

[Plugins]
mod_company_register = {register}
mod_invoice_numbering = {mod_invoice_numbering}
mod_qrcodes = {mod_qrcodes}

[Paths]
database = {database}
template = {template}

[Refere]
taxpayerid = {taxpayerid}
name = {name}
account_number = {account_number}
email = {email}

[Options]\
'''

    def get_configuration(self):
        out = self.config_template.format(**self.input_options)
        if self.input_options['verbose']:
            out = '''\
{}
verbose = True\
'''.format(out)
        return out

    def __str__(self):
        input_options = {
            'taxpayerid': self.input_options['taxpayerid'],
            'database': self.input_options['database'],
            'template': self.input_options['template'],
        }
        out = '''[Input options]\
%s
[Configuration]
%s''' % (self.input_options, self.get_configuration())
        return out

#{'generate': None, 'update': [5261044039, 5261044039], 'configuration': 'tests/data/config_apiregon', 'database': None, 'template': None, 'output': None, 'taxpayerid': None, 'items': None, 'verbose': True}