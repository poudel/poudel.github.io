#!/usr/bin/env python

from string import Template
from pygments import highlight
from pygments.lexers import PythonLexer
from pygments.formatters import HtmlFormatter


def get_index_template():
    with open('index_tpl.html') as tpl:
        return Template(tpl.read())


def get_code():
    with open('index.py') as codefile:
        return codefile.read()


def generate(about):
    code = get_code()
    formatter = HtmlFormatter(linenos='inline', style='gruvbox')

    template = get_index_template()

    about['style'] = formatter.get_style_defs()
    about['body'] = highlight(code, PythonLexer(), formatter)

    index_html = template.substitute(about)

    with open('index.html', 'w') as index_html_file:
        index_html_file.write(index_html)
