from django import forms
from django.shortcuts import redirect, render
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views import View
from django.views.generic import ListView, CreateView, DetailView, DeleteView, UpdateView
from .models import Post, UserProfile, Comment, Event, Group 
from django.http import HttpResponseForbidden
from django.urls import reverse, reverse_lazy
from .forms import CommentForm, EventForm, GroupForm, OwnerForm, UserProfileForm
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
    template_name = "post_delete.html"
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
    
class EventDetailView(LoginRequiredMixin, DetailView):
    model = Event
    template_name = 'event_detail.html'
    context_object_name = 'event'

class EventRegisterView(LoginRequiredMixin, View):
    def post(self, request, pk):
        event = get_object_or_404(Event, pk=pk)
        event.member.add(request.user)
        return redirect('event-detail', pk=pk)

class GroupListView(LoginRequiredMixin, ListView):
    model = Group
    template_name = 'groups.html'
    context_object_name = 'groups'

class GroupCreateView(LoginRequiredMixin, CreateView):
    model = Group
    form_class = GroupForm
    template_name = 'group_create.html'
    success_url = reverse_lazy('group-list')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        response = super().form_valid(form)
        self.object.member.add(self.request.user)
        return response
    
class GroupDetailView(LoginRequiredMixin, DetailView):
    model = Group
    template_name = 'group_detail.html'
    context_object_name = 'group'

class GroupRegisterView(LoginRequiredMixin, View):
    def post(self, request, pk):
        group = get_object_or_404(Group, pk=pk)
        
        if request.user == group.owner:
            if 'new_owner' in request.POST:
                form = OwnerForm(group, request.POST)
                if form.is_valid():
                    group.owner = form.cleaned_data['new_owner']
                    group.member.remove(request.user)
                    group.save()
                    return redirect('group-detail', pk=pk)
            else:

                form = OwnerForm(group)
                return render(request, 'owner.html', {'form': form, 'group': group})
        else:
            if request.user in group.member.all():
                group.member.remove(request.user)
            else:
                group.member.add(request.user)
        
        return redirect('group-detail', pk=pk)
    
class GroupDeleteView(LoginRequiredMixin, DeleteView):
    model = Group
    template_name = 'group_delete.html'
    context_object_name = 'group'
    success_url = reverse_lazy('group-list')

    def dispatch(self, request, *args, **kwargs):
        group = self.get_object()
        if request.user != group.owner:
            return redirect('group-detail', pk=group.pk)
        return super().dispatch(request, *args, **kwargs)

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