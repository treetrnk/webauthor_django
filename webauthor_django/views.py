from django.shortcuts import render
from pages.models import Page,Tag

def default_meta(title='', image='/static/images/logo.png', description='A blog by Nathan Hare about Fate Core and other roleplaying games.'):
    title_suffix = '' if len(title) else ' - A blog by Nathan Hare'
    return {
        'title': str(title) + 'rpg stuff' + str(title_suffix),
        'image': str(image),
        'favicon': '/static/images/favicon.png',
        'description': str(description),
    }

def index(request):
    return render(request, 'index.html') 

def about(request):
    page = Page.objects.get(slug='about')
    meta = default_meta()
    tags = Tag.objects.all().order_by('name')
    return render(request, 'page.html', {'page': page, 'meta': meta, 'tags': tags}) 

def handler404(request):
    page = Page.objects.get(slug='404-error')
    meta = default_meta()
    tags = Tag.objects.all().order_by('name')
    return render(request, 'pages/page.html', {'page': page, 'meta': meta, 'tags': tags}) 

