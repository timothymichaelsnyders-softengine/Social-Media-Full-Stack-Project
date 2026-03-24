from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static #me
from django.conf import settings #me
from userauth import views #me

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home),
    path('signup/', views.signup),
    path('loginn/', views.loginn),
    path('logoutt', views.logoutt),
    path('upload/', views.upload),
    path('like-post/<str:id>', views.likes, name='like-post'),

    # to redirect to each individual post we need
    path('#<str:id>', views.home_posts),

    # to show all the users posts:
    path('explore', views.explore), #leave out the trailing forward slash
    
    path('profile/<str:id_user>', views.profile),

    path('follow', views.follow, name='follow'),

    path('delete/<str:id>', views.delete),

    path('search_results/', views.search_results, name='search_results')
]