#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2010, Nicolas Clairon
# All rights reserved.
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
#     * Redistributions of source code must retain the above copyright
#       notice, this list of conditions and the following disclaimer.
#     * Redistributions in binary form must reproduce the above copyright
#       notice, this list of conditions and the following disclaimer in the
#       documentation and/or other materials provided with the distribution.
#     * Neither the name of the University of California, Berkeley nor the
#       names of its contributors may be used to endorse or promote products
#       derived from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE REGENTS AND CONTRIBUTORS ``AS IS'' AND ANY
# EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE REGENTS AND CONTRIBUTORS BE LIABLE FOR ANY
# DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
# ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

import os.path
from subprocess import *
import shlex

class Pypit(object):
    def __init__(self, config):
        """
        config: a python dict which describes the config to use (please, see the doc)
        """
        self._programmes = []
        for prog in config:
            self._programmes.append(prog)

    def run(self, input_file=None):
        """
        run the pipeline from config.

        input: an input file. Usefull to set up a pipe with a dynamic file
        returns the final results
        """
        p = None
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
                if p is None:
                    if input_file is None:
                        raise ValueError('It seems like you want to use dynamic input. Please specify an input_file value')
                    kwargs['stdin'] = input_file
                else:
                    kwargs['stdin'] = p.stdout
            elif input:
                kwargs['stdin'] = open(input, 'r')
            p = Popen(args, **kwargs)
        return p.communicate()[0]

            
        
