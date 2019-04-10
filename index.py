#!/usr/bin/env python

from collections import namedtuple


about = {
    'name': 'keshab paudel',
    'timezone': 'Europe/Berlin',
    'birth_timezone': 'Asia/Kathmandu',
    'description': 'software development and Lowercase',
}


Link = namedtuple('Link', ['url', 'description'])

about['links'] = [
    Link('mailto:self@<this-domain>', 'Email'),
    Link('https://keshab.net', 'Website'),
    Link('https://github.com/poudel', 'Github'),
]


Work = namedtuple('Work', ['company', 'url', 'start', 'end'])

about['works'] = [
    Work('Seerene', 'https://seerene.com', 'Dec 2018', None),
    Work('Khalti', 'https://khalti.com', 'Sep 2017', 'Nov 2018'),
    Work('AayuLogic', 'https://aayulogic.com', 'Jan 2017', 'Sep 2017'),
    Work('Real Solutions', 'https://realsolutions.com.np', 'May 2015', 'Dec 2016'),
]


Tech = namedtuple('Tech', ['title', 'type', 'skill_level', 'more'])

about['tech'] = [
    Tech('Python', 'language', 'pretty_good', 'bread and butter'),
    Tech('Django/DRF/Flask', 'web_framework', 'pretty_good', 'bread and butter'),

    Tech('PostgreSQL', 'database', 'good_enough', 'it stares back'),
    Tech('MySQL', 'database', 'good_enough', 'use postgres'),

    Tech('Emacs', 'operating_system', 'pretty_good', 'work environment of choice'),
    Tech('ArchLinux', 'bootloader', 'good', 'work environment'),

    Tech('JavaScript', 'sicilian_bull', 'pretty_good', 'find someone else'),
    Tech('PHP', '', '', ''),
]


about['keywords'] = [
    'Go', 'Elixir', 'Erlang', 'Emacs Lisp', 'Elm', 'TypeScript',
    'Ubuntu', 'Debian', 'CentOS',
]


if __name__ == '__main__':
    from generator import generate
    generate(about)
