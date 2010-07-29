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
import os
from subprocess import *

class Pypit(object):
    def __init__(self, config):
        """
        config: a python dict which describes the config to use (please, see the doc)
        """
        self._programmes = []
        self.last_output_ext = None
        self.cmdline = None
        for prog in config:
            self._programmes.append(prog)

    def run(self, file_name=None, cwd=None):
        """
        run the pipeline from config.

        input: an input file. Usefull to set up a pipe with a dynamic file
        returns the final results
        """
        self.input_name = file_name
        results = []
        for prog in self._programmes:
            kwargs = {}
            if file_name:
                if prog.get('output_ext'): 
                    self.last_output_ext = prog.get('output_ext')
                    output_name = '%s.%s' % (self.input_name, prog.get('output_ext'))
                else:
                    output_name = self.input_name
                prog['cmd'] = prog['cmd'].replace('{{input}}', self.input_name).replace('{{output}}', output_name)
                prog['cmd'] = prog['cmd'].replace('{{cwd}}', cwd)
                self.input_name = output_name
            args = prog['cmd']
            if prog.get('use_stdin'):
                if results:
                    results.append('|')
                else:
                    results.append('cat %s |' % self.input_name)
            elif results:
                if prog.get('skip_errors'):
                    results.append(';')
                else:
                    results.append('&&')
            results.append(args)
        self.cmdline = " ".join(results)
        pype = Popen(self.cmdline, stdout = PIPE, stderr=PIPE, shell=True, cwd=cwd)
        self.errors = pype.stderr
        return pype.stdout.read()


