from django.shortcuts import render,get_object_or_404
from datetime import datetime
from .models import Page,Tag
import pytz
from webauthor_django.views import handler404,set_meta
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
    contect['meta'] = default_meta()
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
    # now return the rendered template
    return render(request, 'pages/page.html', context)

def page(request):
    path = request.path + '/' if request.path[-1] != '/' else request.path
    #path_list = path.split('/')
    #path_list = list(filter(bool, path_list))
    print('Path: ' + path)
    page = Page.objects.get(slug='home') if not len(path) > 1 else get_object_or_404(Page, path=path)
    print('Page Path: ' + page.path)
    matched_path = True if not len(path) > 1 or page.path == path else False
    if page and page.pub_date <= utc.localize(datetime.now()) and matched_path:
        meta = set_meta(page.title, page.banner_url, page.description)
        return render(request, 'pages/' + page.template + '.html', {'page': page, 'meta': meta})
    elif request.method == 'GET' and 'code' in request.GET:
        print(page.code())
        if request.GET['code'] == page.code():
            return render(request, 'pages/' + page.template + '.html', {'page': page, 'meta': set_meta()})
        else:
            return handler404(request)
    else:
        return handler404(request)

def rss(request):
    pages = Page.objects.filter(pub_date__lte=datetime.now()).order_by('-pub_date')
    return render(request, 'pages/rss.xml', {'pages': pages, 'meta': set_meta()})
