from datetime import datetime
from pages.models import Page,Tag

def baseurl(request):
    """
    Return a BASE_URL template context for the current request.
    """
    if request.is_secure():
            scheme = "https://"
    else:
            scheme = "http://"
    return {'BASE_URL': scheme + request.get_host(),}

def nav(request):
    return {'nav': Page.objects.filter(parent__isnull=True).filter(pub_date__lte=datetime.now())}

def tags(request):
    return {'tags': Tag.objects.all().order_by('name')}

def theme(request):
    try:
        request.session['theme'] = request.GET['theme']
    except KeyError:
        if not 'theme' in request.session:
           request.session['theme'] = ''
    return {'theme': request.session['theme']}

