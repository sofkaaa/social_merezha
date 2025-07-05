from django.urls import path
from . import views

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('post/new/', views.PostCreateView.as_view(), name='create_post'),
    path('post/<int:pk>/', views.PostDetailView.as_view(), name='post_detail'),
    path("comment/edit/<int:pk>", views.ComentEditView.as_view(), name="comment-edit"),
    path("comment/delete/<int:pk>", views.ComentDeleteView.as_view(), name="comment-delete"),
    path('profile/<slug:username>/', views.ProfileView.as_view(), name='profile'),
    path('events/', views.EventListView.as_view(), name='events'),
    path('groups/', views.GroupListView.as_view(), name='groups'),
]