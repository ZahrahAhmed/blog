from django.contrib import admin
from .models import Post

class ZahrahAdmin(admin.ModelAdmin):
	list_display = ["id","topic","update"]
	search_fields = ["topic", "content"]
	list_filter = ["update", "timestamp"]
	list_display_links = ["id"]
	list_editable = ["topic"]

	class Meta:
		model = Post
admin.site.register(Post, ZahrahAdmin)
