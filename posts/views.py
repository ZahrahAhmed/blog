from django.shortcuts import render, get_object_or_404, redirect 
from .models import Post 
from .forms import PostForm 
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


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

def post_detail(request, post_id):
	item = get_object_or_404(Post, id=post_id)
	text = {
		"item" :item,
	}
	return render(request, "detail.html", text)

def post_create(request):
	form = PostForm(request.POST or None, request.FILES or None)
	if form.is_valid():
		form.save()
		messages.success(request, "you added a blog post")
		return redirect("posts:list")
	context = { 
		"form": form,
	 }
	return render(request, 'create.html', context)

def post_update(request, post_id):
	item = Post.objects.get(id=post_id)

	form = PostForm(request.POST or None, request.FILES or None, instance=item )
	if form.is_valid():
		form.save()
		messages.info(request, "you updated a blog post")
		return redirect("posts:detail", post_id=item.id)
	context = { 
		"form": form,
		"item": item,
	 }
	return render(request, 'update.html', context)

def post_delete(request, post_id):
	Post.objects.get(id=post_id).delete()
	messages.warning(request, "Y THO")
	return redirect("posts:list")























def home(request):
	context = {
		"key1": "hello",
		"key2": "bye",
	}
	return render (request, 'home.html', context)