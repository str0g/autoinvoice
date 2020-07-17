class ConfigurationCreator:
    def __init__(self, input_options: dict = None):
        self.input_options = {
            'url': '',
            'key': '',
            'invoice_numbering': '',
            'taxpayerid': '',
            'name': '',
            'register': 'apiregon',
            'database': '~/.autoinvoice/dbase.db',
            'template': '/usr/share/polishinvoice/templates/simple.tex'
        }
        if input_options:
            self.input_options.update(input_options)
        self.config_template = '''\
[Common]
url = {url}
key = {key}
register = {register}

[Plugins]
invoice_numbering = {invoice_numbering}

[Paths]
database = {database}
template = {template}

[Refere]
taxpayerid = {taxpayerid}
name = {name}\
'''

    def get_configuration(self):
        return self.config_template.format(**self.input_options)

    def __str__(self):
        out = '''[Input options]\
%s
[Configuration]
%s''' % (self.input_options, self.get_configuration())
        return out
