The setup for this specific Django applicaltion/project:

#1 - SETUP VIRUAL ENVIRONMENT
>pip install virtualenv
>virtualenv venv (creates the virtualenv)
(navigate to venv/Scripts to activate virtual environment)
>cd venv
>cd Scripts
>C:\Tim\Programming\Django\Social_Media_Images\venv\Scripts>activate (activate virtual env)


#2 - On ViRTUAL ENV
>pip install django
>django-admin startproject socialmedia (start the project)
>cd socialmedia
>py manage.py startapp userauth (start the application)

#3 - Setup the configurations in the SocialMedia project folder
> Check in the urls.py and settings.py files for marking "#me", this will indicate the setting up for the project
YOU MIGHT HAVE TO REFERNCE THE PROJECT FOLDER FOR TEMPLATES INSTEAD OF JUST `Templates` FOLDER IN THE Settings.py
E.G:
    `'DIRS': [os.path.join(BASE_DIR, 'socialmedia/templates')]`
INSTEAD OF:
    `'DIRS': [os.path.join(BASE_DIR, 'templates')]`

#4 - In the application
>Create a urls.py file
>Copy and paste everything from the urls.py file in socialmedia into the new file
>Remove `path('', include('userauth.urls'))` and replace it with `path('', views.home)`
>import `from userauth import views` on the top
>In views.py in the application, create:
def home(request):
    return HttpResponse("Hello World!")
>On the top of views.py, import `from django.http import HttpResponse`

#5 - In  virtual environment terminal/cmd, type "py manage.py runserver"

#################### Start of actual project ####################

#6 - Create Profile model
>Inside of userauth App, under models.py type create the Profile Model
>After creating the model and importing all important imports, run the following command in the
cmd to create the MIGRATION:
`py manage.py makemigrations`

#7 - Create the signup view
>Inside of the authuser application in the views.py file, create a signup function:
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
            return redirect('/')
    except:
        invalid = "User Already Exists"
        return render(request, 'signup.html', {'invalid': invalid})

>After this create the signup.html file with the fields 'fnm', 'emailid' and 'pwd' in the form name fields. Make sure the method is 'POST' to satisfy the incoming method on the backend

>run the command to actually migrate:
    `py manage.py migrate`

#8 - Creating the SUPERUSER
>In the terminal, type:
    py manage.py createsuperuser

E.G.
username: tim
email: tim@gmail.com
password: tim@12345

> Run the server

% NOTE TO SELF %
----------------
The application has the routes to the Project Templates folder.
So the application is the backend.
- Create MODELS in the Application. (models.py)
- Set the URLS in the Application. (urls.py)
- Create the VIEWS in the Application. (views.py)

The Project (initial command `django-admin startproject socialmedia`) contains the:
- Front end TEMPLATES for the PROJECT (templates/signup.html, etc...)
- The MEDIA for the PROJECT (such as `default_img_2.jpg`)
- The STATIC files for the PROJECT

DONT FORGET
In the urls.py of the PROJECT, add the following to include the URLS from the BACKEND:
`path('', include('userauth.urls'))` in the urlpatters array

And concat the urlpatters with the line at the bottom of the file:
`urlpatterns = urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)`

----------------
% END OF NOTE %

#9 - Register the models in admin.py in the APPLICATION (backend)
> in admin.py in the backend, type:
    from .models import *

    admin.site.register(Profile)

>Run Server and register

#10 - Login Page and View Login
>Add the login to the URLS array in the backend (Application)
    path('loginn/', views.loginn),
>Create the .html document in Templates directory in the Frontend (Project)
>Create the view in the views.py in the Backend with logic.

#11 - Logout
>Create .html for logout
>Create URL for logoutt
>Create VIEW for logoutt

#12 - Post Model
>Create a new model called Post in the models.py file in the Backend

#13 - Uploads
>Create the Posts model
>Create the modal.html file
>Register the Posts model in admin.py
>Migrate the Post model
    py manage.py makemigrations
    py manage.py migrate
>Run server

% NOTE TO SELF %
When trying to Create a Post,
You get an error saying that there is no backslash or something like that at the end of the URL
And django cannot redirect to a backslash with request information or something.

FIX : 
In the form of the modal.html, instead of:
<form action="upload" method="POST" enctype="multipart/form-data">
Type:
<form action="/upload/" method="POST" enctype="multipart/form-data">

And in the settings.py of the Project (frontend), add:
`APPEND_SLASH = False`
% END OF NOTE %

>Post is created in sqlite database, now just render it on the frontend (.html template)
    - Do this by adding functionality in the views.py (backend) home function before `return render(request, 'main.html')`

From:
    def home(request):
    return render(request, 'main.html')

To:
    def home(request):
    # return HttpResponse("Hello World!")

    post = Post.objects.all().order_by('-created_at')
    # profile = Profile.objects.get(user=request.user) #get the profile of the user that is logged in
    context = {
        'post' : post,
        # 'profile' : profile
    }

    return render(request, 'main.html', context)

>The image is now rendered on localhost:8000 (home page dashboard)
[Maybe resize the images, damn bro!]

#14 - Liking posts
>In the models.py of the backend (Application - userauth), create a new model called LikePost(models.Model)
> Run `py manage.py makemigrations`
> Run `py manage.py migrate`
>In admin, register the LikePost model:
    `admin.site.register(LikePost)`
>In urls, add the like-post URL:
    `path('like-post/<str:id>', views.likes, name='like-post')`
>In the urls.py add a new function called 'likes'. Pass the `id` as a second parameter, to target the specific post.
>Add a new URL to urls.py:
`path('#<str:id>', views.home_posts)` to redirect to each individual post
>Add this to the views.py file as well as a function:
`def home_posts(request):`

#15 - Profile
>Create a new path in urls.py file:
`path('profile/<str:id_user>', views.profile)`
>Create the new function in views.py (don't forget 2nd parameter)
>Create the template `profile.html` and `edit_profile.html`
>Include `edit_profile.html` in the `profile.html` template via:
    `{% include "edit_profile.html" %}`
[This will include the form needed for the functionality in the views.py file for POST requests and GET requests]

>>Because Create Post won't work from Profile.html, create a new template called `profile_upload.html`.
>>Copy the code from `modal.html` to `profile_upload.html`
>> Add `{% include "profile_upload.html" %}` in the profile.html template
>> In the `profile_upload.html` template, target `exampleModal2` in the div:
    <div class="modal fade" id="exampleModal2" tabindex="-1" aria-labelledby="exampleModalLabel" aria-hidden="true">

#16 - Followers
>Create a new model called 'Followers'
>Add in admin.py file the new Model
>Create migrations
>Add a new function `follow` in views.py
>Add functionality to follow
>Add functionality to the `profile` function in viewss as well...
    This is to:
    i) count number of users the current profile is following
    ii) count the number of followers the current profile has
    iii) Determine whether current logged in user is following the currently viewed user account

#17 - Delete posts
>Create a new url `delete/<str:id>` and link it to `views.delete`
>Create a new function in views.py called `delete` and pass a parameter for the post `id`

#18 - Searching users
(Do I have to do this one, uuhhgg!!)
>Create a url called `search_results/` and link it to views.search_result
>Create a template called 'search.html' which will have a form to type the user you want to search for.
>Add functionality to `search` function in views.py, using BUILT IN DJANGO FUNCTIONS.
>Return a redirect to a new .html template with the list of matched users, soo....
>Create a new .html template called `search_user.html`

% NOTE TO SELF %
We use modals alot in this project hence why you need to add `data-bs-target="#exampleModal3"` for example to your menu items.
You also need to include the same name in the `id` of the modal in the modal template so that the correct modal opens when the menu item is clicked.
In the `main` tag of the template where you want the modal to appear, you also need to add an `includes` section, eg.
`{% include "search.html" %}`
Which will include the search.html file (which is the modal code) in the current .html file.
% END NOTE %




LAST, AND HOPEFULLY THE LEAST


#19 - Add decorators to specific functions to limit accesing these endpoints if you are not logged in/authorized to access them.
> In the views.py file in the Backend (Application), import the decorators:
`from django.contrib.auth.decorators import login_required`

% NOTE TO SELF %
Logoutt url should be `path('logoutt', views.logoutt)`
NOT `path('logoutt/', views.logoutt)` 
% END NOTE %