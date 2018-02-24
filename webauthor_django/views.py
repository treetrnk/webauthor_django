from django.shortcuts import render
from pages.models import Page,Tag
from datetime import datetime

def set_meta(title='', image='/static/images/logo.png', description='A blog by Nathan Hare about Fate Core and other roleplaying games.'):
    title_suffix = '' if len(title) else ' - A blog by Nathan Hare'
    return {
        'title': str(title) + 'rpg stuff' + str(title_suffix),
        'image': str(image),
        'favicon': '/static/images/favicon.png',
        'description': str(description),
    }

def handler404(request):
    page = Page.objects.get(slug='404-error')
    tags = Tag.objects.all().order_by('name')
    return render(request, 'pages/page.html', {'page': page, 'meta': set_meta()}) 

