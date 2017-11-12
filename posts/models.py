from django.db import models
from django.core.urlresolvers import reverse

class Post(models.Model):
	topic = models.CharField(max_length=100)
	content = models.TextField()
	update = models.DateField(auto_now=True)
	timestamp = models.TimeField(auto_now_add=True)
	img = models.ImageField(null=True , blank=True, upload_to="post_images")

	def __str__(self):
		return self.topic

	def get_detail_url(self):
		return reverse("posts:detail", kwargs={"post_id": self.id })
	
	class Meta:
		ordering = ['topic']