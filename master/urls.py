from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login.as_view()),
    path('logout/', views.Logout.as_view()),

    path('recipe/', views.RecipeApi.as_view()),
    path('rating/', views.RatingApi.as_view()),

]

from .import scheduler

scheduler.start()

# def