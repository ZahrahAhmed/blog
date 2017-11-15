from django.shortcuts import render, get_object_or_404, redirect 
from .models import Post 
from .forms import PostForm 
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from urllib.parse import quote
from django.http import Http404


def post_list(request):
	objects = Post.objects.all()
	paginator = Paginator(objects, 2)
	number = request.GET.get('page')
	try:
		objects = paginator.page(number)
	except PageNotAnInteger:
		objects = paginator.page(1)
	except EmptyPage:
		objects = paginator.page(paginator.num_pages)
	con = {
		"post_items": objects,
	}
	return render(request, "list.html", con)

def post_detail(request, post_slug):
	item = get_object_or_404(Post, slug=post_slug)
	text = {
		"item" :item,
		"share_string": quote(item.content)
	}
	return render(request, "detail.html", text)

def post_create(request):
	if not request.user.is_staff:
		raise Http404
	form = PostForm(request.POST or None, request.FILES or None)
	if form.is_valid():
		form.save()
		messages.success(request, "you added a blog post")
		return redirect("posts:list")
	context = { 
		"form": form,
	 }
	return render(request, 'create.html', context)

def post_update(request, post_slug):
	item = Post.objects.get(slug=post_slug)

	form = PostForm(request.POST or None, request.FILES or None, instance=item )
	if form.is_valid():
		form.save()
		messages.info(request, "you updated a blog post")
		return redirect("posts:detail", post_slug=item.slug)
	context = { 
		"form": form,
		"item": item,
	 }
	return render(request, 'update.html', context)

def post_delete(request, post_slug):
	Post.objects.get(slug=post_slug).delete()
	messages.warning(request, "Y THO")
	return redirect("posts:list")












def home(request):
	context = {
		"key1": "hello",
		"key2": "bye",
	}
	return render (request, 'home.html', context)