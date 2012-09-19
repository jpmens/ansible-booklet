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
import re
import argparse
import time
import datetime

MODULEDIR="/Users/jpm/Auto/pubgit/ansible/ansible/library"

def clever():
    return "Hello WORLD"

# There is a better way of doing this!

_ITALIC = re.compile(r"I\(([^)]+)\)")
_BOLD   = re.compile(r"B\(([^)]+)\)")
_MODULE = re.compile(r"M\(([^)]+)\)")
_URL    = re.compile(r"U\(([^)]+)\)")
_CONST  = re.compile(r"C\(([^)]+)\)")

def latex_ify(text):

    t = _ITALIC.sub("\\I{" + r"\1" + "}", text)
    t = _BOLD.sub("\\B{" + r"\1" + "}", t)
    t = _MODULE.sub("\\M{" + r"\1" + "}", t)
    t = _URL.sub("\\url{" + r"\1" + "}", t)
    t = _CONST.sub("\\C{" + r"\1" + "}", t)

    return t

def html_ify(text):

    t = _ITALIC.sub("<em>" + r"\1" + "</em>", text)
    t = _BOLD.sub("<b>" + r"\1" + "</b>", t)
    t = _MODULE.sub("<span class='module'>" + r"\1" + "</span>", t)
    t = _URL.sub("<a href='" + r"\1" + "'>" + r"\1" + "</a>", t)
    t = _CONST.sub("<code>" + r"\1" + "</code>", t)

    return t

def manpage_ify(text):

    t = _ITALIC.sub(r'\\fI' + r"\1" + r"\\fR", text)
    t = _BOLD.sub(r'\\fB' + r"\1" + r"\\fR", t)
    t = _MODULE.sub(r'\\fI' + r"\1" + r"\\fR", t)
    t = _URL.sub(r'\\fI' + r"\1" + r"\\fR", t)
    t = _CONST.sub(r'\\fC' + r"\1" + r"\\fR", t)

    return t

env = Environment(loader=FileSystemLoader('templates'),
        variable_start_string="@{",
        variable_end_string="}@",
    )

env.globals['clever'] = clever


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
        raise
    return doc

def main():

    p = argparse.ArgumentParser(description="Convert Ansible module DOCUMENTATION strings to other formats")

    p.add_argument("-M", "--module-dir",
            action="store",
            dest="module_dir",
            default=MODULEDIR,
            help="Ansible modules/ directory")
    p.add_argument("-t", "--type",
            action='store',
            dest='type',
            choices=['html', 'latex', 'manpage'],
            default='latex',
            help="Output type")
    p.add_argument("-m", "--module",
            action='append',
            default=[],
            dest='module_list',
            help="Add modules to process in module_dir")
    p.add_argument("-v", "--verbose",
            action='store_true',
            default=False,
            help="Verbose")
    p.add_argument("-o", "--output-dir",
            action="store",
            dest="output_dir",
            default=None,
            help="Output directory for module files")
    p.add_argument('-V', '--version', action='version', version='%(prog)s 1.0')

    module_dir = None
    args = p.parse_args()
    
    # print "M: %s" % args.module_dir
    # print "t: %s" % args.type
    # print "m: %s" % args.module_list
    # print "v: %s" % args.verbose

    if not args.module_dir:
        print "Need module_dir"
        sys.exit(1)

    if args.type == 'latex':
        env.filters['jpfunc'] = latex_ify
        template = env.get_template('latex.j2')
        outputname = "%s.tex"
    if args.type == 'html':
        env.filters['jpfunc'] = html_ify
        template = env.get_template('html.j2')
        outputname = "%s.html"
    if args.type == 'manpage':
        env.filters['jpfunc'] = manpage_ify
        template = env.get_template('manpage.j2')
        outputname = "%s.man"

    for module in os.listdir(args.module_dir):
        if len(args.module_list):
            if not module in args.module_list:
                continue

        fname = os.path.join(args.module_dir, module)
        extra = os.path.join("inc", "%s.tex" % module)

        # FIXME: html/manpage/latex
        print "%% modules2.py ---> %s" % fname

        doc = get_docstring(fname)
        if not doc is None:
            
            doc['filename'] = fname
            doc['docuri'] = doc['module'].replace('_', '-')
            doc['now_date']     = datetime.date.today()

            if args.verbose:
                print json.dumps(doc, indent=4)


            if args.type == 'latex':
                if os.path.exists(extra):
                    f = open(extra)
                    extradata = f.read()
                    f.close()
                    doc['extradata'] = extradata

            text = template.render(doc)
            if args.output_dir is not None:
                f = open(os.path.join(args.output_dir, outputname % module), 'w')
                f.write(text)
                f.close()
            else:
                print text

if __name__ == '__main__':
    main()
