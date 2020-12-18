from subprocess import Popen, PIPE

class CmdlineCreator:
    def __init__(self, cmd: dict = None, extra_cmd: dict = {}):
        self.cmdline = None
        self.extra_cmd = extra_cmd
        self.cmd = {
            'generate': None, #should be [] as input
            'update': None,
            'configuration': '',
            'database': '/tmp/.autoinvoice/dbase.db',
            'template': '',
            'output': None,
            'taxpayerid': '',
            'items': None,
            'verbose': True,
            'name': '',
            'url': '',
            'key': '',
            'register': 'apiregon',
            'invoice_numbering': '',
            'qrcode_generator': ''
        }
        if cmd:
            self.cmd.update(cmd)

    def run(self):
        self.cmdline = ['python3', '-m', 'autoinvoice']
        if self.cmd['verbose']:
            self.cmdline.append('-v')

        self.cmdline.append('-c')
        self.cmdline.append(self.cmd['configuration'])

        if 'generate' in self.cmd and self.cmd['generate']:
            for c in self.cmd['generate']:
                self.cmdline.append('-g')
                self.cmdline.append(c)

        if '-u' in self.extra_cmd:
            for u in self.extra_cmd['-u']:
                self.cmdline.append('-u')
                self.cmdline.append(str(u))

        if '-d' in self.extra_cmd:
            self.cmdline.append('-d')
            self.cmdline.append(self.extra_cmd['-d'])

        if self.cmd['output']:
            self.cmdline.append('-o')
            self.cmdline.append(self.cmd['output'])

        if self.cmd['items']:
            self.cmdline.append('-i')
            self.cmdline.append(self.cmd['items'])

        with Popen(self.cmdline, stdout=PIPE) as proc:
            out = proc.stdout.read().decode('utf-8').split('\n')

        return proc.returncode, out

    def command_line_input(self):
        return self.cmdline

    def command_output(self):
        return self.cmd
