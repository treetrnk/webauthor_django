from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from datetime import datetime
#from .tools import recursive_parents
import hashlib
import markdown

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
        body = models.TextField(max_length=10000)
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
                if self.parent:
                        return recursive_parents(self.parent)
                else:
                        return False

        def clean_body(self):
            pattern = '(?:\<[\s\S]*?\>)|(?:\!\[[\s\S]*?\]\([\s\S]*?\))|\#|\*|(?:\[)|(?:\]\([\s\S]*?\))|(?:[\n\r]{2,})'
            return re.sub(pattern, '', self.body)

        def banner_url(self):
            if self.banner is None:
                return '/static/images/forest.png'
            return '/media/' + self.banner.filename()

        def full_path(self):
            return self.path + self.slug + '/'

        def description(self):
            if self.summary is None or not self.summary:
                return self.clean_body()[0:295] + '...'
            return self.summary + '...'

        def code(self):
            return hashlib.sha512(str(self.slug + 
                str(datetime.now().month) + 
                str(datetime.now().day)).encode('utf-8')).hexdigest()

        def show_story_title(self):
                display_in = ['chapter', 'post']
                if self.parent:
                        if self.template == 'story':
                                return "<h1>" + self.title + "</h1>"
                        elif self.template in display_in:
                                return "<h1>" + self.parent.title + "</h1>"
                return ''
