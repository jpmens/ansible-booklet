#!/usr/bin/env python
# (c) 2012, Jan-Piet Mens <jpmens () gmail.com>
#
# This file is part of Ansible
#
# Ansible is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Ansible is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Ansible.  If not, see <http://www.gnu.org/licenses/>.
#

import os
import sys
import yaml
import codecs
import json
import ast
from jinja2 import Environment, FileSystemLoader

env = Environment(loader=FileSystemLoader('templates'),
        variable_start_string="@{",
        variable_end_string="}@",
    )
template = env.get_template('latex.j2')

def get_docstring(filename):
    """
    Search for assignment of the DOCUMENTATION variable in the given file.
    Parse that from YAML and return the YAML doc or None.
    """

    doc = None

    try:
        # Thank you, Habbie, for this bit of code :-)
        M = ast.parse(''.join(open(filename)))
        for child in M.body:
            if isinstance(child, ast.Assign):
                if 'DOCUMENTATION' in (t.id for t in child.targets):
                    doc = yaml.load(child.value.s)
    except:
        pass
    return doc

dir = '/Users/jpm/Auto/pubgit/ansible/ansible/library'

for module in os.listdir(dir):
    fname = os.path.join(dir, module)
    extra = os.path.join("inc", "%s.tex" % module)

    print "%% modules2.py ---> %s" % fname

    doc = get_docstring(fname)
    if not doc is None:
        d = doc[module]

        d['module'] = module
        d['filename'] = fname
        d['docuri'] = d['module'].replace('_', '-')

        # print json.dumps(d, indent=4)


        if os.path.exists(extra):
            f = open(extra)
            extradata = f.read()
            f.close()
            d['extradata'] = extradata

        print template.render(d)
