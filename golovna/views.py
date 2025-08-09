from django import forms
from django.shortcuts import redirect, render
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views import View
from django.views.generic import ListView, CreateView, DetailView, DeleteView, UpdateView
from .models import Post, UserProfile, Comment, Event, Group 
from django.http import HttpResponseForbidden
from django.urls import reverse, reverse_lazy
from .forms import CommentForm, EventForm, UserProfileForm
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
# Create your views here.

class HomeView(ListView):
    model = Post
    template_name = 'home.html'
    context_object_name = 'posts'

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            user_profile, created = UserProfile.objects.get_or_create(us=user)

            friend_users = user_profile.friends.values_list('us', flat=True)
            return Post.objects.filter(us__in=friend_users).order_by('-time')
        return Post.objects.all().order_by("-time")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['events'] = Event.objects.all().order_by('data')[:5]
        context['groups'] = Group.objects.all().order_by('time')[:5]
        return context

class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['content', 'image', 'video', 'link']
    template_name = 'post_create.html'
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        form.instance.us = self.request.user
        return super().form_valid(form)
    
class PostDetailView(LoginRequiredMixin, DetailView):
    model = Post
    template_name = "post_detail.html"
    context_object_name = "post"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = CommentForm()
        context['comments'] = Comment.objects.filter(post=self.object, vid__isnull=True).order_by('-time')
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = CommentForm(request.POST)

        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = self.object
            comment.us = request.user
            comment.save()
            return redirect('post_detail', pk=self.object.pk)

        context = self.get_context_data()
        context['form'] = form
        return self.render_to_response(context)

class ProfileView(LoginRequiredMixin, DetailView):
    model = UserProfile
    template_name = 'profile.html'
    context_object_name = 'profile_user'

    def get_object(self):
        return get_object_or_404(UserProfile, us__username=self.kwargs['username'])

    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profile'] = self.object
        context['posts'] = Post.objects.filter(us=self.object.us)
        return context
        
class PostDeleteView(LoginRequiredMixin, DeleteView):
    model = Post
    template_name = "post_confirm_delete.html"
    success_url = reverse_lazy("home")

class PostEditView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['content', 'image', 'video', 'link']
    template_name = "post_edit.html"
    success_url = reverse_lazy("home")

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author      

class EventListView(LoginRequiredMixin, ListView):
    model = Event
    template_name = 'events.html'
    context_object_name = 'events'
    ordering = ['data']

class EventCreateView(LoginRequiredMixin, CreateView):
    model = Event
    form_class = EventForm
    template_name = 'events_create.html'
    success_url = reverse_lazy('event-list')

    def form_valid(self, form):
        form.instance.us = self.request.user
        return super().form_valid(form)

class GroupListView(LoginRequiredMixin, ListView):
    model = Group
    template_name = 'groups.html'
    context_object_name = 'groups'

class ComentEditView(LoginRequiredMixin,  UpdateView):
    model = Comment
    form_class = CommentForm
    template_name = "coment_edit.html"

    def get_success_url(self):
        return reverse("post-detail", kwargs={"pk": self.get_object().pk})


class ComentDeleteView(LoginRequiredMixin,  DeleteView):
    model = Comment
    template_name = "coment_delete.html"

    def get_success_url(self):
        return reverse_lazy("post-detail", kwargs={"pk": self.get_object().pk})
    
class UserListView(LoginRequiredMixin, ListView):
    model = UserProfile
    template_name = "user_list.html"
    context_object_name = "user_list"

class FriendView(LoginRequiredMixin, View):
    def post(self, request, pk):
        friend_profile = get_object_or_404(UserProfile, pk=pk)

        request.user.userprofile.friends.add(friend_profile)
        friend_profile.friends.add(request.user.userprofile)
        return redirect ("user-list")