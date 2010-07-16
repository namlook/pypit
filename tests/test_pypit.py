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

import unittest

from pypit import *
import os
import yaml

class PypitTestCase(unittest.TestCase):

    def setUp(self):
        open('tests/test_file.txt', 'w').write('1\n5\n3\n4\n6\n8\n9\n2\n7\n')

    def tearDown(self):
       if 'pypit_test_buf' in os.listdir('/tmp'):
           os.remove('/tmp/pypit_test_buf') 

    def test_pipe_via_stdin(self):
        config = """
- 
    cmd: cat {{input}}

- 
    cmd: sort 
    use_stdin: true
"""
        res = Pypit(config=yaml.load(config)).run(file_name='test_file.txt', cwd='tests')
        assert res  == '1\n2\n3\n4\n5\n6\n7\n8\n9\n', res

    def test_pipe_via_file(self):
        config = """
- 
    cmd: cat {{input}} > {{output}}
    output_ext:  bla
- 
    cmd: sort -r {{input}}
"""
        res =  Pypit(config=yaml.load(config)).run(file_name='test_file.txt', cwd='tests')
        assert res == '9\n8\n7\n6\n5\n4\n3\n2\n1\n', res

    def test_pipe_shell(self):
        config = """
- 
    cmd: echo "12345"

- 
    cmd: wc -c
    use_stdin: true
"""
        result = Pypit(config=yaml.load(config)).run()
        assert result == '6\n', '+'+result+'+'

    def test_pure_shell(self):
        config = """
- 
    cmd: echo $PWD

"""
        result = Pypit(config=yaml.load(config)).run()
        assert result.strip() == os.environ['PWD'], result

    def test_3_progs(self):
        config = """
- 
    cmd: cat {{input}} > {{output}}
    output_ext: buf

- 
    cmd: sort -r {{input}}
-
    cmd: wc -l
    use_stdin: true
"""
        result =  Pypit(config=yaml.load(config)).run(file_name='test_file.txt', cwd='/home/namlook/Documents/projets/pypit/tests')
        assert result == '9\n', "+"+result+"+"


    def test_dynamic_input(self):
        config = """
-
    cmd: sort -r
    use_stdin: true
-
    cmd: wc -l
    use_stdin: true
"""
        result = Pypit(config=yaml.load(config)).run(file_name='test_file.txt', cwd='tests')
        assert result == '9\n', "+"+result+"+"

    def test_dynamic_input2(self):
        config = """
-
    cmd: /usr/bin/sort -r
    use_stdin: true
-
    cmd: /usr/bin/wc -l
    use_stdin: true
"""
        result = Pypit(config=yaml.load(config)).run(file_name='test_file.txt', cwd="tests")
        assert result == '9\n', "+"+result+"+"

