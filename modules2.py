#!/usr/bin/env python

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
