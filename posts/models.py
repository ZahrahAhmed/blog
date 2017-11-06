from django.db import models
from django.core.urlresolvers import reverse

class Post(models.Model):
	topic = models.CharField(max_length=100)
	content = models.TextField()
	update = models.DateField(auto_now=True)
	timestamp = models.TimeField(auto_now_add=True)

	def __str__(self):
		return self.topic

	def get_detail_url(self):
		return reverse("detail", kwargs={"post_id": self.id })