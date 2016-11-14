from django.utils.encoding import python_2_unicode_compatible
from django.db import models

# Create your models here.

@python_2_unicode_compatible
class NewsArticle(models.Model):
	post_id = models.CharField(max_length=200)
	title = models.CharField(max_length=200)
	pub_date = models.DateTimeField('date published')
	summary = models.CharField(max_length=500)
	img_src = models.CharField(max_length=200,blank=True,null=True)
	url = models.CharField(max_length=200)
	source = models.CharField(max_length=50)

	def __str__(self):
		return self.title