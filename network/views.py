from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse, Http404
from django.core.paginator import Paginator
from rest_framework.parsers import JSONParser
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from django.urls import reverse

from .models import User, Post, Follow, Like
from .serializers import PostSerializer, LikeSerializer


def index(request):
    """ 
    Load the home page
    """

    posts = Post.objects.order_by("-timestamp").all()
    paginator = Paginator(object_list=posts, per_page=10, allow_empty_first_page=True)
    page_number = request.GET.get('page')
    page_object = paginator.get_page(number=page_number)
    likes = list()

    if str(request.user) != "AnonymousUser":
        for post in page_object:
            # Return whether user have liked post or not
            try:
                like = Like.objects.get(post=post, user=request.user)
                likes.append(like.is_liked)

            # If user have never liked or unliked a post set it to not liked
            except Like.DoesNotExist:
                likes.append(False)

    return render(request, "network/index.html", {
        "page_object": page_object,
        "likes": likes
    })


def new_post(request):
    """
    Create a new post and redirect the user to the home page
    """

    content = request.POST["content"]
    post = Post(content=content, poster=request.user)
    post.save()

    return HttpResponseRedirect(reverse('index'))


def profile(request, poster_id):
    """
    Load the profile of the user whom the user tried to access if available
    """

    try:
        poster = User.objects.get(pk=poster_id)
    except User.DoesNotExist:
        raise Http404("This user does not exist")
    
    try:
        Follow.objects.get(is_following=True, followee=poster, follower=request.user)
        is_following = True
    except Follow.DoesNotExist:
        is_following = False

    posts = Post.objects.filter(poster=poster).order_by("-timestamp")
    paginator = Paginator(object_list=posts, per_page=10, allow_empty_first_page=True)
    page_number = request.GET.get('page')
    page_object = paginator.get_page(number=page_number)
    len(page_object)

    poster_following = poster.following.filter(follower_id=poster_id, is_following=True)
    poster_followers = poster.followers.filter(followee_id=poster_id, is_following=True)
    followers = list()
    followings = list()

    for follower in poster_followers:
        followers.append(User.objects.get(pk=follower.follower_id))

    for following in poster_following:
        followings.append(User.objects.get(pk=following.followee_id))

    return render(request, "network/profile.html", {
        "page_object": page_object,
        "poster": poster,
        "followings": followings,
        "followers": followers,
        "posts_count": Post.objects.filter(poster=poster).count(),
        "followers_count": poster.followers.filter(followee_id=poster_id, is_following=True).count(),
        "followee_count": poster.following.filter(follower_id=poster_id, is_following=True).count(),
        "is_following": is_following
    })


def user_profile(request):
    """
    Load the current user's profile page
    """

    if (str(request.user) == "AnonymousUser"):
        return HttpResponseRedirect(reverse("login"))

    else:
        return HttpResponseRedirect(reverse("profile", args=(request.user.id,)))


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
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]

        user = User.objects.create_user(username, email, password)

        # Ensure password is valid
        if not user.is_password_valid():
            return render(request, "network/register.html", {
                "message": "Password must be at least 8 characters long, contain one uppercase, one lower case, one digit"
            })

        # Ensure password matches confirmation
        elif not user.do_passwords_match:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })
            

        # Attempt to create new user
        try:
            # user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")


def following(request):
    user = User.objects.get(pk=request.user.id)
    followings = user.following.filter(is_following=True)
    user_followings = list()
    for following in followings:
        user_followings.append(following.followee_id)

    following = User.objects.filter(pk__in=user_followings)
    posts = Post.objects.filter(poster__in=following).order_by("-timestamp")
    paginator = Paginator(object_list=posts, per_page=10, allow_empty_first_page=True)
    page_number = request.GET.get('page')
    page_object = paginator.get_page(number=page_number)

    return render(request, "network/following.html", {
        "page_object": page_object
    })


# API Views
@csrf_exempt
def like(request):
    """
    Allow users to like and unlike posts
    """

    # User loading the page
    if request.method == 'POST':
        data = JSONParser().parse(request)
        post = Post.objects.get(pk=data["post_id"])
        
        # Set users who haven't logged in like status to not liked
        if str(request.user) == "AnonymousUser":
            return JsonResponse({"liked": False})

        # Users who have logged in
        else:

            # Return whether user have liked post or not
            try:
                likes = Like.objects.get(post=post, user=request.user)
                return JsonResponse({"liked": likes.is_liked})

            # If user have never liked or unliked a post set it to not liked
            except Like.DoesNotExist:
                return JsonResponse({"liked": False})

    # User trying to toggle between like and dislike
    elif request.method == 'PUT':
        
        # User haven't logged in
        if str(request.user) == "AnonymousUser":
            return JsonResponse({"status": "Anonymous User"}, status=201)

        # User have logged in
        else:
            data = JSONParser().parse(request)
            post = Post.objects.get(pk=data["post_id"])

            if data["is_liked"]:
                post.increase_likes()
            else:
                post.decrease_likes()

            # Attempt to toggle between like and unlike of a post
            try:
                like = Like.objects.get(post=post, user=request.user)
                like.is_liked = data["is_liked"]
                like.save()

            # User have never like or unliked post
            except Like.DoesNotExist:
                like = Like(is_liked=data["is_liked"], post=post)
                like.save()
                like.user.add(request.user)

            return JsonResponse({"status": "Successful"}, status=201)


@csrf_exempt
def like_count(request):
    """
    Gets the number of likes a post have
    """

    data = JSONParser().parse(request)
    post = Post.objects.get(pk=data["post_id"])
    serializer = PostSerializer(post, many=False)
    return JsonResponse(serializer.data, safe=False)


@csrf_exempt
def change_password(request):
    """
    Change the password of a user
    """

    try:
        user = User.objects.get(pk=request.user.id)
    except User.DoesNotExist:
        raise Http404("This user does not exist")

    data = JSONParser().parse(request)

    if data.get("prev_pwd") is not None:
        if data["prev_pwd"] is not user.password:
            return JsonResponse({"message": "Old password is wrong"}, status=201)

    elif data.get("confirm_pwd") is not None:
        if not user.do_passwords_match(data["confirm_pwd"]):
            return JsonResponse({"message": "New passwords don't match"}, status=201)

    elif data.get("new_pwd") is not None:
        if not user.is_password_valid(data["new_pwd"]):
            return JsonResponse({"message": "Password must be at least 8 characters long, contain one uppercase, one lower case, one digit"}, status=201)

    if data.get("new_pwd") is not None:
        user.password = data["new_pwd"]
        user.save()
        return JsonResponse({"message": "Successful"}, status=201)


@csrf_exempt
def edit_post(request):
    """
    Allows users to edit existing posts they have made
    """

    data = JSONParser().parse(request)

    try:
        post = Post.objects.get(pk=data["post_id"])
    except Post.DoesNotExist:
        raise Http404("This post does not exist")

    if data.get("post_content") is not None:
        if len(data["post_content"]) == 0:
            return JsonResponse({"message": "Post must contain at least one character"}, status=201)

        post.content = data["post_content"]
        post.save()
        return JsonResponse({"message": "Successful"}, status=201)


@csrf_exempt
def follow(request):
    """
    Allow users to follow other users
    """

    data = JSONParser().parse(request)
    followee = User.objects.get(pk=data["followee"])

    try:
        follow = Follow.objects.get(is_following=False, followee=followee, follower=request.user)
        follow.is_following = True
        follow.save()
        return JsonResponse({"message": "Successful"}, status=201)
    except Follow.DoesNotExist:
        Follow.objects.create(is_following=True, followee=followee, follower=request.user)
        return JsonResponse({"message": "Successful"}, status=201)


@csrf_exempt
def unfollow(request):
    """
    Allow users to unfollow users they are already following
    """

    data = JSONParser().parse(request)
    followee = User.objects.get(pk=data["followee"])
    follow = Follow.objects.get(is_following=True, followee=followee, follower=request.user)
    follow.is_following = False
    follow.save()

    return JsonResponse({"message": "Successful"}, status=201)
