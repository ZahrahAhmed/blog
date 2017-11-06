from django.shortcuts import render, get_object_or_404
from .models import Post 

def home(request):
	context = {
	"key1": "hello",
	"key2": "bye",
	}
	return render (request, 'home.html', context)

def post_list(request):
	objects = Post.objects.all()
	con = {
		"post_items": objects,
	}
	return render(request, "list.html", con)

def post_detail(request, post_id):
	item = get_object_or_404(Post, id=post_id)
	text = {
		"item" :item,
	}
	return render(request, "detail.html", text)












	

def home1(request):
	text = {
	"key3": "back",
	"key4": "again",
	}
	return render(request, 'home1.html', text)

def home2(request):
	txt = { 
	"key5": "the",
	"key6": "END",
	}
	return render (request, 'home2.html', txt)