from django.conf.urls import include, url
from rest_framework import routers, serializers, viewsets, pagination
from .models import NewsArticle
from . import views

# Serializers define the API representation.
class NewsArticleSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = NewsArticle 
        fields = ('title', 'pub_date', 'summary', 'img_src', 'source', 'url')

class StandardResultsSetPagination(pagination.PageNumberPagination):
    page_size = 50
    page_size_query_param = 'page_size'
    max_page_size = 1000

# ViewSets define the view behavior.
class NewsArticleViewSet(viewsets.ModelViewSet):
    queryset = NewsArticle.objects.all().order_by('-pub_date')
    serializer_class = NewsArticleSerializer
    pagination_class = StandardResultsSetPagination

# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r'api', NewsArticleViewSet)

urlpatterns = [
	url(r'^$', views.index, name="news_index"),
	url(r'^fetch$', views.fetch, name="news_fetch"),
    url(r'^notif_reg', views.reg_notif, name="notif_reg"),
	url(r'^', include(router.urls)),
]