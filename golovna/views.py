from django.shortcuts import redirect, render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView, DetailView
from .models import Post, UserProfile, Comment, Event, Group
from django.http import HttpResponseForbidden
from django.urls import reverse_lazy
from .forms import CommentForm
# Create your views here.

class HomeView(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'home.html'
    context_object_name = "posts"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['events'] = Event.objects.all().order_by('data')[:5]
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

    def post(self, request, *args, **kwargs):
        post = self.get_object()

        form = CommentForm(request.POST)
        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.post = post
            new_comment.us = request.user
            new_comment.save()

            return redirect(request.path_info)
        else:
            return self.get(request, *args, **kwargs)

