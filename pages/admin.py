from django.contrib import admin
from .models import Page,Tag,Image
from django.utils.html import format_html
from datetime import datetime
import hashlib

class PageAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'get_url', 'banner', 'get_banner', 'author', 'pub_date')
    prepopulated_fields = {'slug': ('title',)}
    def get_banner(self, obj):
        return format_html(
                '<a href="{}" target="banner">{}</a>',
                str(obj.banner_url()),
                str(obj.banner_url())
        )
    get_banner.short_description = 'Banner Path'
    get_banner.admin_order_field = "banner"

    def get_url(self, obj):
        return format_html(
                '<a href="{}" target="post">{}</a>',
                '/' + str(obj.pub_date.year) + '/' + 
                    str(obj.pub_date.month) + '/' + 
                    str(obj.pub_date.day) + '/' + 
                    obj.slug + '?code=' + obj.code(),
                'View Post'
        )
    get_url.short_description = 'URL'
    get_url.admin_order_field = "pub_date"

class ImageAdmin(admin.ModelAdmin):
    list_display = ('name', 'file')

# Register your models here.
admin.site.register(Page, PageAdmin)
admin.site.register(Tag)
admin.site.register(Image, ImageAdmin)
