from django.shortcuts import render
from datetime import datetime
from .models import Page,Tag
import pytz
from webauthor_django.views import handler404
import hashlib

utc = pytz.UTC

def index(request):
    try:
        tag = request.GET['tag'] 
    except KeyError:
        tag = ''
    try:
        search = request.GET['search'] 
    except KeyError:
        search = ''
    print('Tags: ' + str(tag))
    print('Search: ' + str(search))
    context = {}
    context['meta'] = {
        'title': 'rpg stuff - A blog by Nathan Hare',
        'image': '/static/images/logo.png',
        'favicon': '/static/images/favicon.png',
        'description': 'A blog by Nathan Hare about Fate Core and other roleplaying games.',
    }
    # get the blog pages that are published
    if tag:
        #tag_array = ','.join(tags)
        pages = Page.objects.filter(tags__name__in=[tag]).filter(pub_date__lte=datetime.now())
        context['searchtag'] = tag
    elif search:
        #search_array = ' '.join(search)
        pages = Page.objects.filter(body__icontains=search).filter(pub_date__lte=datetime.now())
        context['search'] = search 
    else:
        pages = Page.objects.filter(pub_date__lte=datetime.now()).order_by('-pub_date')
    context['pages'] = pages
    context['tags'] = Tag.objects.all().order_by('name')
    # now return the rendered template
    return render(request, 'pages/page.html', context)

def page(request, year, month, day, slug):
    page = Page.objects.filter(pub_date__year=year,
        pub_date__month=month,
        #pub_date__day=day,
        slug=slug)[0]
    meta = {
        'title': page.title + ' - rpg stuff',
        'image': str(page.banner_url()),
        'favicon': '/static/images/favicon.png',
        'description': page.description(),
    }
    print(request.GET)
    print(hasattr(request.GET, 'code'))
    tags = Tag.objects.all().order_by('name')
    if pae.pub_date <= utc.localize(datetime.now()):
        return render(request, 'blog/page.html', {'page': page, 'meta': meta, 'tags': tags})
    elif request.method == 'GET' and 'code' in request.GET:
        print(page.code())
        if request.GET['code'] == page.code():
            return render(request, 'pages/page.html', {'page': page, 'meta': meta, 'tags': tags})
        else:
            return handler404(request)
    else:
        return handler404(request)

def rss(request):
    meta = {
        'title': 'rpg stuff - A blog by Nathan Hare',
        'image': '/static/images/logo.png',
        'favicon': '/static/images/favicon.png',
        'description': 'A blog by Nathan Hare about Fate Core and other roleplaying games.',
    }
    pages = Page.objects.filter(pub_date__lte=datetime.now()).order_by('-pub_date')
    return render(request, 'pages/rss.xml', {'pages': pages, 'meta': meta})
