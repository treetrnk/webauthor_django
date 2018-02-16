from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from autoslug import AutoSlugField
from .tools import recursive_parents

class Page(models.Model):
	TEMPLATE_CHOICES = [
		('page', 'Page'),
		('blog', 'Blog'),
		('post', 'Post'),
		('story', 'Story'),
		('chapter', 'Chapter'),
	]
	title = models.CharField(max_length=200)
	slug = AutoSlugField(null=True, populate_from='title')
	parent = models.ForeignKey('self', on_delete=models.PROTECT, blank=True, null=True)
	template = models.CharField(max_length=100, choices=TEMPLATE_CHOICES)
	banner = models.CharField(max_length=1000, blank=True)
	tags = models.CharField(max_length=1000, blank=True)
	sidebar = models.TextField(blank=True)
	body = models.TextField()
	pub_date = models.DateTimeField(auto_now_add=True)
	author = models.ForeignKey(User, null=True, blank=True)

	def __str__(self):
		return self.title

	def save_model(self, request, obj, form, change):
		"""When creating a new object, set the creator field.
		"""
		if not change:
			obj.author = request.user
		obj.save()

	def children(self):
		return Page.objects.filter(parent=self, pub_date__lte=timezone.now())

	def all_parents(self):
		if self.parent:
			return recursive_parents(self.parent)
		else:
			return False

	def show_story_title(self):
		display_in = ['chapter', 'post']
		if self.parent:
			if self.template == 'story':
				return "<h1>" + self.title + "</h1>"
			elif self.template in display_in:
				return "<h1>" + self.parent.title + "</h1>"
		return ''
