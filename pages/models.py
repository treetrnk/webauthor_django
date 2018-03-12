from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from datetime import datetime
#from .tools import recursive_parents
import hashlib
import markdown
import os
import re

def get_child_list(obj, current_id=""):
    children = Page.objects.filter(parent=obj.parent, pub_date__lte=timezone.now())
    child_list = "<ul>"
    for child in children:
        print(child.title)
        if current_id and current_id is child.id:
            child_list += "<li>" + child.title
        else:
            child_list += "<li><a href='" + child.full_path + "'>" + child.title + "</a>"
        if child.children():
            child_list += get_child_list(child, current_id)
        child_list += "</li>"
    return child_list + "</ul>"

class Tag(models.Model):
        name = models.CharField(max_length=50)

        def __str__(self):
            return self.name

        class Meta:
            ordering = ['name']

class Image(models.Model):
        name = models.CharField(max_length=50)
        file = models.ImageField()
        credit = models.TextField(max_length=300, blank=True, null=True)

        def filename(self):
            return os.path.basename(self.file.name)

        def file_path(self):
            return '/media/' + str(self.filename())

        def html_credit(self):
            if self.credit is not None:
                return markdown.markdown(self.credit)
            return ''

        def __str__(self):
            return self.name

        def save(self, *args, **kwargs):
            super(Image, self).save(*args, **kwargs)
            filename = self.file.url

        class Meta:
            ordering = ['name']

class Page(models.Model):
        TEMPLATE_CHOICES = [
                ('page', 'Page'),
                ('blog', 'Blog'),
                ('post', 'Post'),
                ('story', 'Story'),
                ('chapter', 'Chapter'),
        ]
        title = models.CharField(max_length=200)
        slug = models.SlugField(max_length=200, null=True)
        dir_path = models.CharField(max_length=500, editable=False, blank=True, null=True)
        path = models.CharField(max_length=500, editable=False, blank=True, null=True)
        parent = models.ForeignKey('self', on_delete=models.PROTECT, blank=True, null=True)
        template = models.CharField(max_length=100, choices=TEMPLATE_CHOICES)
        banner = models.ForeignKey(Image, blank=True, null=True, on_delete=models.SET_NULL)
        body = models.TextField(max_length=10000000)
        tags = models.ManyToManyField(Tag, blank=True)
        summary = models.TextField(max_length=300, blank=True)
        sidebar = models.TextField(max_length=1000, blank=True)
        author = models.ForeignKey(User, on_delete=models.PROTECT)
        sort = models.IntegerField(default=75)
        pub_date = models.DateTimeField()
        edit_date = models.DateTimeField(auto_now=True)

        def __str__(self):
                return self.title

        class Meta:
            #order_with_respect_to = 'parent'
            ordering = ['dir_path', 'sort', 'pub_date', 'title']

        def clean(self):
            path = '/'
            parent = self.parent
            while parent:
                path = '/' + parent.slug + path
                parent = parent.parent
            self.dir_path = path
            self.path = path + self.slug + '/'

        def html_body(self):
            return markdown.markdown(self.body)

        def children(self):
                return Page.objects.filter(parent=self, pub_date__lte=timezone.now())

        def all_parents(self):
            parent_list = []
            current_parent = self.parent
            while current_parent:
                parent_list.append(current_parent)
                current_parent = current_parent.parent
            return parent_list

        def clean_body(self):
            pattern = '(?:\<[\s\S]*?\>)|(?:\!\[[\s\S]*?\]\([\s\S]*?\))|\#|\*|(?:\[)|(?:\]\([\s\S]*?\))|(?:[\n\r]{2,})'
            return re.sub(pattern, '', self.body)

        def banner_url(self):
            parents = self.all_parents()
            if self.banner:
                return '/media/' + self.banner.filename()
            for parent in parents[::-1]:
                if parent.banner:
                    return '/media/' + parent.banner.filename()
            return '/static/images/forest.png'

        def full_path(self):
            return self.path + self.slug + '/'

        def description(self):
            if self.summary is None or not self.summary:
                return self.clean_body()[0:295] + '...'
            return self.summary + '...'

        def word_count(self):
            return len(re.split(r'\w+', self.clean_body()))

        def read_time(self):
            minimum = int(self.word_count() / 200)
            maximum = int(self.word_count() / 150)
            return str(minimum) + ' - ' + str(maximum) + ' mins.' if minimum > 0 else '< 1 min.'

        def code(self):
            return hashlib.sha512(str(self.slug +
                str(datetime.now().month) +
                str(datetime.now().day)).encode('utf-8')).hexdigest()

        def full_sidebar(self):
            full_sidebar = self.sidebar 
            if self.template is "story" or self.template is "blog":
                full_sidebar += "<h2>Table of Contents</h2>"
                try:
                    full_sidebar += get_child_list(self.children()[0])
                except IndexError:
                    full_sidebar += "</ul><p>Nothing here yet...</p>"
            elif self.template is "chapter" or self.template is "post":
                full_sidebar += "<h2>Table of Contents</h2>" + get_child_list(self, self.id)
            return full_sidebar

        def show_story_title(self):
                display_in = ['chapter', 'post']
                if self.parent:
                        if self.template == 'story':
                                return "<h1>" + self.title + "</h1>"
                        elif self.template in display_in:
                                return "<h1>" + self.parent.title + "</h1>"
                return ''
