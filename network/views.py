import datetime
import json

from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .models import User, Posts
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator

def index(request):
    return render(request, "network/index.html")

def following(request):
    return render(request, "network/following.html")

@login_required
def new(request):
    if request.method == "POST":
        content = request.POST["content"]
        postTime = datetime.datetime.now()
        user = User.objects.get(username=request.user.username)
        post = Posts(content=content, poster=user, likes=0, postTime=postTime)
        post.save()
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/new.html")


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
            user.liked.clear()
            user.following.clear()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")

@csrf_exempt
@login_required
def posts(request, mode=None):
    # API interaction get list of posts depending on mode
    page = int(request.GET.get("page") or 1)

    if mode == None:
        # return all posts
        posts = Posts.objects.all()

    elif mode == "following":
        # return posts by those user is following
        user = User.objects.get(username=request.user.username)
        posts = Posts.objects.filter(poster__in=user.following.all())

    else:
        # return posts for specific username
        user = User.objects.get(username=mode)
        posts = Posts.objects.filter(poster=user)

    # Return posts in reverse chronologial order
    posts = posts.order_by("-postTime").all()
    posts = Paginator(posts, 10)
    posts = posts.page(page)
    return JsonResponse([post.serialize() for post in posts], safe=False)


@csrf_exempt
@login_required
def follow(request):
    # API interaction to update who the user is following

    if request.method == "PUT":
        data = json.loads(request.body)
        user = User.objects.get(username=request.user.username)
        following = User.objects.get(username=data["following"])
        print(data["follow"])
        if data["follow"] == "true":
            user.following.add(following)
        else:
            user.following.remove(following)
        return HttpResponse(status=204)


def profile(request, profile):
    # Render user profile page from url
    user = User.objects.get(username=profile)
    return render(request, "network/profile.html", {
        "profile": user,
        "following": user.following.count(),
        "followers": user.followers.count(),
        "allow": user not in User.objects.get(username=request.user.username).following.all()
    })
