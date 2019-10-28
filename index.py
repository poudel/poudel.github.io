#!/usr/bin/env python

from collections import namedtuple
from string import Template
from pygments import highlight
from pygments.lexers import PythonLexer
from pygments.formatters import HtmlFormatter


Link = namedtuple('Link', ['url', 'description'])
Work = namedtuple('Work', ['company', 'url', 'start', 'end'])
Tech = namedtuple('Tech', ['title', 'skill_rating'])


about = {
    'name': 'keshab paudel',
    'timezone': 'Europe/Berlin',
    'description': 'I like abstractions, self-reference, and writing code',
    'links': [
        Link('mailto:self@<this-domain>', 'Email'),
        Link('https://keshab.net', 'Website'),
        Link('https://github.com/poudel', 'Github'),
    ],
    'works': [
        Work('Seerene', 'https://seerene.com', 'Dec 2018', None),
        Work('Khalti', 'https://khalti.com', 'Sep 2017', 'Nov 2018'),
        Work('AayuLogic', 'https://aayulogic.com', 'Jan 2017', 'Sep 2017'),
        Work('Real Solutions', 'https://realsolutions.com.np', 'May 2015', 'Dec 2016'),
    ],
    'tech': [
        Tech('Python', 'pretty_good'),
        Tech('Django/DRF/Flask', 'pretty_good'),
        Tech('PostgreSQL', 'good_enough'),
    ],
    'keywords': [
        'Python',
        'Linux',
        'JavaScript',
        'Elixir',
        'Erlang',
        'Emacs Lisp',
        'Elm',
        'TypeScript',
        'Ubuntu',
        'Debian',
        'CentOS',
        'MySQL',
    ],
}


def generate(about):
    formatter = HtmlFormatter(linenos='inline', style='gruvbox')

    with open('index.py') as codefile:
        code = codefile.read()

    with open('index_tpl.html') as tpl:
        template = Template(tpl.read())

    about['style'] = formatter.get_style_defs()
    about['body'] = highlight(code, PythonLexer(), formatter)

    index_html = template.substitute(about)

    with open('index.html', 'w') as index_html_file:
        index_html_file.write(index_html)


if __name__ == '__main__':
    generate(about)
