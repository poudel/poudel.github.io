#!/usr/bin/env python
"""
NotFancy: Static site generator.
"""
import os
import shutil
import re
import sys
from datetime import datetime
from markdown2 import markdown
from dateutil.parser import parse
from jinja2 import Environment, FileSystemLoader
from rcssmin import cssmin

CONTENT_PATTERN = re.compile(r"---(?P<front>.*)---(?P<content>.*)", re.S)
INTERLINK_PATTERN = re.compile(r"\[il:(?P<slug>.+):(?P<anchor>.+)\]")
WORKING_DIR = os.path.abspath(os.path.dirname(__file__))
OUTPUT_DIR = os.path.join(WORKING_DIR, 'p')
CONTENT_DIR = os.path.join(WORKING_DIR, 'content')
STATIC_DIR = os.path.join(WORKING_DIR, 'static')


def interlink_sub(match):
    slug, anchor = match.groups()
    return "<a href='{}.html'>{}</a>".format(slug, anchor)


class Post:

    def __init__(self, filename, env):
        self.env = env
        self.slug = os.path.splitext(filename)[0]
        self.output_path = os.path.join(OUTPUT_DIR, "{}".format(self.slug))
        self.draft = False

        path = os.path.join(CONTENT_DIR, filename)
        with open(path, 'r') as fi:
            match = CONTENT_PATTERN.match(fi.read())

            if not match:
                print("There is something wrong with {}".format(filename))
                sys.exit(1)

            groupdict = match.groupdict()
            for matter in groupdict['front'].strip().split('\n'):
                key, value = map(str.strip, matter.split(':'))
                if key == 'date':
                    value = parse(value).date()
                elif key == 'draft':
                    value = True if value == 'true' else False
                setattr(self, key, value)

            self.raw_content = groupdict['content'].strip()

    def __repr__(self):
        return "<Post: {}>".format(self.page_title)

    @property
    def url(self):
        return "/p/{}/".format(self.slug)

    def render(self):
        content = INTERLINK_PATTERN.sub(interlink_sub, self.raw_content)
        self.content = markdown(
            content,
            extras=["code-friendly", "fenced-code-blocks", "target-blank-links"]
        )
        template = self.env.get_template('detail.html')
        context = {'post': self, 'page_title': self.title, 'description': self.description}
        return template.render(context)

    def publish(self):
        if not os.path.exists(self.output_path):
            os.makedirs(self.output_path)

        with open(os.path.join(self.output_path, 'index.html'), 'w') as output:
            output.write(self.render())

    def unpublish(self):
        if os.path.exists(self.output_path):
            shutil.rmtree(self.output_path)

    @classmethod
    def get_all(cls, env):
        posts = []
        for filename in os.listdir(CONTENT_DIR):
            if filename.endswith('.md'):
                post = cls(filename, env)
                posts.append(post)
        return sorted(posts, key=lambda p: p.date, reverse=True)


def build_site():
    env = Environment(loader=FileSystemLoader(os.path.join(WORKING_DIR, 'templates')))
    posts = Post.get_all(env)

    # first, publish the non-draft posts
    published_posts = []
    for post in posts:
        if post.draft:
            post.unpublish()
        else:
            published_posts.append(post)
            post.publish()

    # build the index page
    index = env.get_template('index.html')
    with open(os.path.join(WORKING_DIR, 'index.html'), 'w') as fi:
        context = {
            "object_list": published_posts,
            "page_title": "keshaB Paudel",
            "description": "Web developer. Python, Django, JavaScript",
            "is_index": True
        }
        fi.write(index.render(context))

    # compile the styles
    css = []
    for filename in os.listdir(STATIC_DIR):
        with open(os.path.join(STATIC_DIR, filename), 'r') as fi:
            css.append(cssmin(fi.read()))

    with open(os.path.join(OUTPUT_DIR, 'style.css'), 'w') as fi:
        fi.write("\n".join(css))


if __name__ == "__main__":
    if not os.path.exists(OUTPUT_DIR):
        print("Creating output directory...")
        os.mkdir(OUTPUT_DIR)

    build_site()
