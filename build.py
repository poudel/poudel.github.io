#!/usr/bin/env python
"""
NotFancy: Static site generator.
"""
import os
import shutil
import re
import sys
import yaml
import htmlmin
from datetime import datetime
from markdown2 import markdown
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
    return f"<a href='/p/{slug}/'>{anchor}</a>"


class Post:

    def __init__(self, filename, env, context):
        self.env = env
        self.context = context.copy()
        self.slug = os.path.splitext(filename)[0]
        self.output_path = os.path.join(OUTPUT_DIR, "{}".format(self.slug))
        self.draft = False
        self.code = False

        self.path = os.path.join(CONTENT_DIR, filename)
        with open(self.path, 'r') as fi:
            match = CONTENT_PATTERN.match(fi.read())

            if not match:
                print("There is something wrong with {}".format(filename))
                sys.exit(1)

            groupdict = match.groupdict()
            try:
                data = yaml.load(groupdict['front'])
            except Exception as e:
                print("There is something wrong with the front matter")
                print(str(e))
                sys.exit(1)
            else:
                for k, v in data.items():
                    setattr(self, k, v)
            self.raw_content = groupdict['content'].strip()

        if not self.code:
            self.context['css_chunk'] = self.context['css']['style']

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
        self.context.update({
            'post': self,
            'page_title': self.title,
            'description': self.description
        })
        return htmlmin.minify(template.render(self.context))

    def publish(self):
        if not os.path.exists(self.output_path):
            os.makedirs(self.output_path)

        with open(os.path.join(self.output_path, 'index.html'), 'w') as output:
            output.write(self.render())

    def unpublish(self):
        if os.path.exists(self.output_path):
            shutil.rmtree(self.output_path)

    def spellcheck(self):
        print("Spellchecking...")
        os.system(f"hunspell -l {self.path} | sort | uniq >words")

    @classmethod
    def get_all(cls, env, context):
        posts = []
        for filename in os.listdir(CONTENT_DIR):
            if filename.endswith('.md') and not filename.startswith(".#"):
                post = cls(filename, env, context)
                posts.append(post)
        return sorted(posts, key=lambda p: p.date, reverse=True)


def build_site():
    # compile and cache all the css files
    css = {}
    for filename in os.listdir(STATIC_DIR):
        with open(os.path.join(STATIC_DIR, filename), 'r') as fi:
            fname = os.path.splitext(filename)[0]
            css[fname] = cssmin(fi.read())

    css_chunk = "\n".join(css.values())

    env = Environment(loader=FileSystemLoader(os.path.join(WORKING_DIR, 'templates')))
    posts = Post.get_all(env, {"css_chunk": css_chunk, "css": css})

    # first, publish the non-draft posts
    published_posts = []
    for post in posts:
        if post.draft:
            post.unpublish()
        else:
            published_posts.append(post)
            # post.spellcheck()
            post.publish()

    # build the index page
    index = env.get_template('index.html')
    with open(os.path.join(WORKING_DIR, 'index.html'), 'w') as fi:
        context = {
            "object_list": published_posts,
            "description": "Web developer. Python, Django, JavaScript",
            "is_index": True,
            "css_chunk": css["style"] # no need for pygments css here
        }
        fi.write(htmlmin.minify(index.render(context)))

    sitemaps = env.get_template('sitemaps.txt')
    with open(os.path.join(WORKING_DIR, 'sitemaps.xml'), 'w') as fi:
        fi.write(sitemaps.render({'object_list': published_posts}))


if __name__ == "__main__":
    if not os.path.exists(OUTPUT_DIR):
        print("Creating output directory...")
        os.mkdir(OUTPUT_DIR)

    build_site()
