
import os.path
from subprocess import *
import shlex
import yaml

class Pypit(object):
    def __init__(self, config):
        self._programmes = []
        for prog in config:
            self._programmes.append(prog)

    def run(self):
        for prog in self._programmes:
            args = [os.path.join(prog['path'], prog['name'])]
            if prog.get('options'):
                args.extend(shlex.split(prog['options']))
            kwargs = {}
            if prog.get('shell'):
                kwargs['shell'] = True
            output = prog.get('output')
            if output:
                kwargs['stdout'] = open(output, 'w')
            else:
                kwargs['stdout'] = PIPE
            input = prog.get('input')
            if input == 'STDIN':
                kwargs['stdin'] = p.stdout
            elif input:
                kwargs['stdin'] = open(input, 'r')
            p = Popen(args, **kwargs)
        return p.communicate()[0]

            
        
