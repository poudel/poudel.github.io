#!/usr/bin/env python

from collections import namedtuple
from string import Template
from pygments import highlight, lexers, formatters


Link = namedtuple("Link", ["url", "description"])
Work = namedtuple("Work", ["company", "url", "start", "end"])

about = {
    "name": "Keshab Paudel",
    "timezone": "Europe/Berlin",
    "description": "I like abstractions, self-reference, and writing code",
    "links": [
        Link("mailto:self@<this-domain>", "Email"),
        Link("https://keshab.net", "Website"),
        Link("https://keshp.com", "Website"),
        Link("https://github.com/poudel", "Github"),
    ],
    "works": [
        Work("Zageno", "https://zageno.com", "Jul 2020", None),
        Work("Revolut", "https://revolut.com", "Feb 2020", "Jul 2020"),
        Work("Seerene", "https://seerene.com", "Dec 2018", "Jan 2020"),
        Work("Khalti", "https://khalti.com", "Sep 2017", "Nov 2018"),
        Work("AayuLogic", "https://aayulogic.com", "Jan 2017", "Sep 2017"),
        Work("Real Solutions", "https://realsolutions.com.np", "May 2015", "Dec 2016"),
    ],
    "tech": [
        "Python",
        "Django/DRF/Flask",
        "PostgreSQL",
        "JavaScript",
        "Elixir/Erlang"
        "Clojure/Emacs Lisp/Racket",
        "Linux",
    ],
}


def generate(about):
    with open("index.py") as codefile:
        code = codefile.read()

    with open("index_tpl.html") as tpl:
        template = Template(tpl.read())

    formatter = formatters.HtmlFormatter(linenos="inline", style="gruvbox")
    about["style"] = formatter.get_style_defs()
    about["body"] = highlight(code, lexers.PythonLexer(), formatter)

    index_html = template.substitute(about)

    with open("index.html", "w") as index_html_file:
        index_html_file.write(index_html)


if __name__ == "__main__":
    generate(about)
