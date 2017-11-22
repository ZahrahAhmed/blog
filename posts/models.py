from django.db import models
from django.core.urlresolvers import reverse
from django.db.models.signals import pre_save 
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User 

class Post(models.Model):
	topic = models.CharField(max_length=100)
	author = models.ForeignKey(User, default=1)
	content = models.TextField()
	update = models.DateField(auto_now=True)
	timestamp = models.TimeField(auto_now_add=True)
	draft = models.BooleanField(default=False)
	publish = models.DateField()
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

class Like(models.Model):
	user = models.ForeignKey(User)
	post = models.ForeignKey(Post)
	timestamp = models.DateTimeField(auto_now_add=True)
	
