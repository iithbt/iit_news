from django.contrib import admin
from .models import NewsArticle
# Register your models here.

class NewsArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'pub_date', 'source')
admin.site.register(NewsArticle, NewsArticleAdmin)