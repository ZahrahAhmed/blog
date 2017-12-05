from django.shortcuts import render, get_object_or_404, redirect 
from .models import Post, Like
from .forms import PostForm, UserSignUp, UserLogin
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from urllib.parse import quote
from django.http import Http404, JsonResponse
from django.utils import timezone
from django.db.models import Q
from django.contrib.auth import login, logout, authenticate 

def usersignup(request):
	form = UserSignUp()
	context = {"form": form, }
	if request.method=="POST":
		form = UserSignUp(request.POST)
		if form.is_valid():
			user = form.save()
			x = user.username
			y = user.password

			user.set_password(y)
			user.save()
			auth = authenticate(username=x, password=y)
			login(request, auth)

			return redirect("posts:list")
		else:
			messages.warning(request, form.errors)
			return redirect("posts:signup")
	return render(request,"signup.html", context)

def userlogin(request):
	form = UserLogin()
	context = {"form": form, }
	if request.method=="POST":
		form = UserLogin(request.POST)
		if form.is_valid():
			some_username = form.cleaned_data['username']
			some_password = form.cleaned_data['password']

			auth = authenticate(username=some_username, password=some_password)

			if auth is not None:
				login(request, auth)
				return redirect("posts:list")
			else:
				messages.warning(request, 'Incorrect UserName/Password combination. noob')
				return redirect("posts:login")
		else:
			messages.warning(request, form.errors)
			return redirect("posts:login")

	return render(request,"login.html", context)

def userlogout(request):
	logout(request)
	return redirect("posts:login")

def post_list(request):
	today = timezone.now().date()

	if request.user.is_staff:
		objects = Post.objects.all()
	else: 
		objects = Post.objects.filter(draft=False, publish__lte=today)

	query = request.GET.get('q')
	if query:
		objects = objects.filter(
			Q(topic__icontains=query) |
			Q(content__icontains=query) |
			Q(author__first_name__icontains=query) |
			Q(author__last_name__icontains=query) |
			Q(author__username__icontains=query) 
			).distinct()


	paginator = Paginator(objects, 3)
	number = request.GET.get('page')
	try:
		objects = paginator.page(number)
	except PageNotAnInteger:
		objects = paginator.page(1)
	except EmptyPage:
		objects = paginator.page(paginator.num_pages)
	con = {
		"post_items": objects,
		"today": today,
	}
	return render(request, "list.html", con)

def post_detail(request, post_slug):
	item = get_object_or_404(Post, slug=post_slug)
	today = timezone.now().date()

	if not request.user.is_staff:
		if item.draft or item.publish > today:
			raise Http404

	if request.user.is_authenticated():
		if Like.objects.filter(post=item, user=request.user).exists():
			liked = True 
		else:
			liked = False

	like_count= item.like_set.count()

	text = {
		"item" :item,
		"share_string": quote(item.content),
		"liked": liked,
		"like_count": like_count,
	}
	return render(request, "detail.html", text)

def post_create(request):
	if not request.user.is_staff:
		raise Http404
	form = PostForm(request.POST or None, request.FILES or None)
	if form.is_valid():
		item = form.save(commit=False)
		item.author = request.user
		item.save()
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

def like_button(request, post_slug):
	postobj = Post.objects.get(slug=post_slug)

	like, created = Like.objects.get_or_create(user=request.user, post=postobj)

	if created : 
		action = "like"
	else:
		like.delete()
		action = "unlike"

	like_count= postobj.like_set.count()

	response = {
		"like_count": like_count,
		"action": action, 
	}

	return JsonResponse(response, safe=False)



def home(request):
	context = {
		"key1": "hello",
		"key2": "bye",
	}
	return render (request, 'home.html', context)