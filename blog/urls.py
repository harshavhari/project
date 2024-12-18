from django.urls import path
from . import views

urlpatterns = [
    path('', views.blog_list, name='blog_list'),
    path('post/<slug:slug>/', views.blog_detail, name='blog_detail'),
    path('post/new/', views.blog_create, name='blog_create'),
    path('post/<slug:slug>/edit/', views.blog_edit, name='blog_edit'),
    path('post/<slug:slug>/delete/', views.blog_delete, name='blog_delete'),
]
