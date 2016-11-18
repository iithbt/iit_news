from django.conf.urls import include, url
from rest_framework import routers, serializers, viewsets
from .models import NewsArticle
from . import views

# Serializers define the API representation.
class NewsArticleSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = NewsArticle 
        fields = ('title', 'pub_date', 'summary', 'img_src', 'source', 'url')

# ViewSets define the view behavior.
class NewsArticleViewSet(viewsets.ModelViewSet):
    queryset = NewsArticle.objects.all().order_by('-pub_date')
    serializer_class = NewsArticleSerializer

# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r'api', NewsArticleViewSet)

urlpatterns = [
	url(r'^$', views.index, name="news_index"),
	url(r'^fetch$', views.fetch, name="news_fetch"),
	url(r'^', include(router.urls)),
]