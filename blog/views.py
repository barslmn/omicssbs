from django.shortcuts import render
from django.http import HttpResponse, Http404
from django.template import Template, Context
from pathlib import Path
import subprocess

POST_DIR = Path(__file__).resolve().parent.joinpath('posts')

def get_posts():
    def get_title(post):
        title = subprocess.check_output(f'grep -m1 "<title>" "{post}" | sed "s/<[^>]*>//g;"', shell=True)
        return title.decode('utf-8').strip()
    def get_abstract(post):
        with open(post) as f:
            html = f.read()
        abstract_index = html.find('class="abstract"')
        if abstract_index < 0:
            return ""
        abstract_start = html[:abstract_index].rfind('<div')
        abstract_length = html[abstract_start:].find('</div>')
        return html[abstract_start: abstract_start + abstract_length + 6]


    posts = [{"path": post.name, 'title': get_title(post), 'abstract': get_abstract(post)} for post in list(POST_DIR.glob('*.html'))]
    return posts

def index(request):
    return render(request, 'blog/index.html', context={'posts': get_posts()})


def post(request, path):
    if not path.endswith('.html'):
        path += '.html'

    with open(POST_DIR.joinpath(path)) as f:
        template = f.read()

    template = '{% extends "base/base.html" %}\n' + \
        '{% block content %}\n' + \
        template + \
        '{% include "blog/includes/posts.html" %}' + \
        '\n{% endblock %}'

    context = Context({'posts': get_posts()})
    return HttpResponse(
        Template(template).render(context)
    )
