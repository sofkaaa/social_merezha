from django.urls import path
from . import views

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('post/new/', views.PostCreateView.as_view(), name='post-create'),
    path('post/<int:pk>/', views.PostDetailView.as_view(), name='post_detail'),
    path("comment/edit/<int:pk>", views.ComentEditView.as_view(), name="comment-edit"),
    path("comment/delete/<int:pk>", views.ComentDeleteView.as_view(), name="comment-delete"),
    path('profile/<str:username>/', views.ProfileView.as_view(), name='profile'),
    path('events/', views.EventListView.as_view(), name='event-list'),
    path('events/new/', views.EventCreateView.as_view(), name='event-create'),
    path('groups/', views.GroupListView.as_view(), name='group-list'),
    path("user_list/", views.UserListView.as_view(), name = "user-list"),
    path("friend/<int:pk>/", views.FriendView.as_view(), name = "friend"),
    path('post/<int:pk>/edit/', views.PostEditView.as_view(), name='post-edit'),
]