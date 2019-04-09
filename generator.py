#!/usr/bin/env python

from pygments import highlight
from pygments.lexers import PythonLexer
from pygments.formatters import HtmlFormatter


index_html_tpl = '''
<!DOCTYPE html>
<html lang="en">
    <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
        <title>{about[name]} - {about[description]}</title>
        <meta name="description" content="{about[description]}">
        <style>
            body {{background: #1d2021; font-family: monospace}}
            .lineno {{color: grey; margin-right: 10px;}}
            {style}
        </style>
    </head>
    <body>{body}</body>
</html>
'''


def get_code():
    with open('index.py') as codefile:
        return codefile.read()


def generate(about):
    code = get_code()
    formatter = HtmlFormatter(linenos='inline', style='monokai')

    index_html = index_html_tpl.format(
        about=about,
        style=formatter.get_style_defs(),
        body=highlight(code, PythonLexer(), formatter),
    )

    with open('index.html', 'w') as index_html_file:
        index_html_file.write(index_html)
