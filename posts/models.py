from django.db import models
from django.core.urlresolvers import reverse
from django.db.models.signals import pre_save 
from django.template.defaultfilters import slugify

class Post(models.Model):
	topic = models.CharField(max_length=100)
	content = models.TextField()
	update = models.DateField(auto_now=True)
	timestamp = models.TimeField(auto_now_add=True)
	slug = models.SlugField(unique=True )
	img = models.ImageField(null=True , blank=True, upload_to="post_images")

	def __str__(self):
		return self.topic

	def get_detail_url(self):
		return reverse("posts:detail", kwargs={"post_slug": self.slug })
	
	class Meta:
		ordering = ['topic']

def create_slug(instance, new_slug=None):
	slug_value = slugify(instance.topic)
	if new_slug is not None:
		slug_value = new_slug
	query = Post.objects.filter(slug=slug_value)
	if query.exists():
		slug_value = "%s-%s"%(slug_value, query.last().id)
		return create_slug(instance, new_slug= slug_value)
	return slug_value

def pre_save_some_function(*args, **kwargs):
	instance = kwargs['instance']
	if not instance.slug:
		instance.slug = create_slug(instance)

pre_save.connect(pre_save_some_function, sender=Post)
