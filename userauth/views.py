from django.shortcuts import render, redirect, get_object_or_404 #redirect, 404
from django.http import HttpResponse
from django.contrib.auth.models import User #me
from django.contrib.auth import authenticate, login, logout #me
from .models import Profile, Post, LikePost, Followers #me
from django.db.models import Q
from django.contrib.auth.decorators import login_required

# Create your views here.

def signup(request):
    try:
        if request.method == 'POST':
            fnm = request.POST.get('fnm') #this is a field in the HTML
            emailid = request.POST.get('emailid')
            pwd = request.POST.get('pwd')

            #create the new user
            my_user = User.objects.create_user(fnm, emailid, pwd)
            my_user.save()
            user_model = User.objects.get(username=fnm)
            new_profile = Profile.objects.create(user=user_model, id_user=user_model.id)
            new_profile.save()

            #REDIRECT TO HomePage
            if my_user is not None:
                login(request, my_user) #login is a built in Django method
                return redirect('/')
            return redirect('/loginn')

    except:
        invalid = "User Already Exists"
        return render(request, 'signup.html', {'invalid': invalid})
    
    
    # return render(request, '../socialmedia/templates/signup.html')
    return render(request, 'signup.html')
    # return redirect('/signup.html')
    # return HttpResponse('Sign Up Page')



def loginn(request):
    if request.method == "POST":
        fnm = request.POST.get('fnm') #first name
        pwd = request.POST.get('pwd') #password

        #authenticate
        userr = authenticate(request, username=fnm, password=pwd)
        #check if user is not None
        if userr is not None:
            login(request, userr) #login is a built in Django method
            return redirect('/')

        invalid = "Invalid credentials"
        return redirect(request, 'loginn.html', {'invalid': invalid})
    
    return render(request, 'loginn.html')


@login_required(login_url='/loginn')
def logoutt(request):
    logout(request) #This is a Django function
    return redirect('/loginn')


@login_required(login_url='/loginn')
def upload(request):

    if request.method == 'POST':
        user = request.user.username
        image = request.FILES.get('image_upload')
        caption = request.POST['caption']

        new_post = Post.objects.create(user=user, image=image, caption=caption)
        new_post.save()

        return redirect('/')
    else:
        return redirect('/')


@login_required(login_url='/loginn')
def home(request):
    # return HttpResponse("Hello World!")

    # ---------- This is to show the posts of only the user's I am following ------------
    following_users= Followers.objects.filter(follower=request.user.username).values_list('user', flat=True)
    
    #The below line makes sure that:
    # > I can see my own posts, or...
    # > I can see the posts of the people I am following
    post = Post.objects.filter(Q(user=request.user.username) | Q(user__in=following_users)).order_by('-created_at')
    profile = Profile.objects.get(user=request.user) #get the profile of the user that is logged in
    context = {
        'post' : post,
        'profile' : profile
    }

    return render(request, 'main.html', context)
    #------------------------------------------------------------------------------------

    # post = Post.objects.all().order_by('-created_at')
    # context = {
    #     'post' : post,
    # }

    # return render(request, 'main.html', context)


@login_required(login_url='/loginn')
def likes(request, id):
    if request.method == 'GET':
        username = request.user.username
        post = get_object_or_404(Post, id=id) #get the Post

        like_filter = LikePost.objects.filter(post_id=id, username=username).first() #get the first
        if like_filter is None:
            #recreate a new like
            new_like = LikePost.objects.create(post_id=id, username=username) #create a new LikePost
            post.no_of_likes = post.no_of_likes + 1
        else:
            like_filter.delete()
            post.no_of_likes = post.no_of_likes - 1

        post.save()

        return redirect('/#' + id) #redirect to each individual post
    


# for individual 
@login_required(login_url='/loginn')
def home_posts(request, id):
    post = Post.objects.get(id=id)
    profile = Profile.objects.get(user=request.user)
    context = {
        'post': post,
        'profile': profile
    }

    return render(request, 'main.html', context) #pass the context



def explore(request):
    #just get all posts:
    post = Post.objects.all().order_by('-created_at')
    # profile = Profile.objects.get(user=request.user) #which user is logged in

    context = {
        'post': post,
        # 'profile': profile
    }

    return render(request, 'explore.html', context) #pass the context to the template


@login_required(login_url='/loginn')
def profile(request, id_user):
    user_object = User.objects.get(username=id_user)
    profile = Profile.objects.get(user=request.user)
    
    user_profile = Profile.objects.get(user=user_object) #this is the user that is logged in
    
    #get posts of logged in user
    user_posts = Post.objects.filter(user=id_user).order_by('-created_at')
    user_post_length = len(user_posts) #get the number of user posts

    #Add a new follower variable
    follower = request.user.username
    user = id_user

    if Followers.objects.filter(follower=follower, user=user).first():
        #if user is already followed, unfollow if the follow button is clicked again
        follow_unfollow='Unfollow'
    else:
        follow_unfollow='Follow'

    user_followers = len(Followers.objects.filter(user=id_user)) #count the number of followers for the user account
    user_following = len(Followers.objects.filter(follower=id_user)) #count the number of users the current account is following


    context = {
        'user_object': user_object,
        'user_profile': user_profile,
        'user_posts': user_posts,
        'user_post_length': user_post_length,
        'profile': profile,
        'follow_unfollow': follow_unfollow,
        'user_followers': user_followers,
        'user_following': user_following
    }

    if request.user.username == id_user:
        if request.method == "POST":
            if request.FILES.get('image') == None:
                image = user_profile.profileimg
                bio = request.POST['bio']
                location = request.POST['location']

                user_profile.profileimg = image
                user_profile.bio = bio
                user_profile.location = location
                user_profile.save()
            
            if request.FILES.get('image') != None:
                image = request.FILES.get('image')
                bio = request.POST['bio']
                location = request.POST['location']

                user_profile.profileimg = image
                user_profile.bio = bio
                user_profile.location = location
                user_profile.save()

            return redirect('/profile/' + id_user)
        else:
            return render(request, 'profile.html', context) 


    return render(request, 'profile.html', context) #pass the context



@login_required(login_url='/loginn')
def follow(request):
    if request.method == 'POST':
        follower = request.POST['follower'] #get the follower name
        user = request.POST['user']

        if Followers.objects.filter(follower=follower, user=user).first():
            delete_follower = Followers.objects.get(follower=follower, user=user)
            delete_follower.delete()
            return redirect('/profile/' + user) #return back to the user's profile
    
        else:
            #if the user is not being followed
            new_follower = Followers.objects.create(follower=follower, user=user)
            new_follower.save()
            return redirect('/profile/' + user)
        
    else:
        return redirect('/')



@login_required(login_url='/loginn')
def delete(request, id):
    post = Post.objects.get(id = id)
    post.delete()
    return redirect('/profile/' + request.user.username)


def search_results(request):
    query = request.GET.get('q')
    users = Profile.objects.filter(user__username__icontains=query) #this is a djano function
    posts = Post.objects.filter(caption__icontains=query) #this is a django function
    context = {
        'query': query,
        'users': users,
        'posts': posts
    }

    return render(request, 'search_user.html', context)