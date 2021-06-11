from django.shortcuts import render,redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
    )
from.models import Post, Comment
from users.models import *
from .forms import NewCommentForm
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.contrib.gis.geos import fromstr
from django.contrib.gis.measure import D
from django.contrib.gis.geos import GEOSGeometry
from django.contrib.gis.db.models.functions import Distance
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required
@login_required
def home(request):
    #paginate_by = 5
    current_user = request.user
    context = {
        'posts': Post.objects.filter(location__distance_lte=(GEOSGeometry(current_user.geo_location),D(km=5000)))
    }
    return render(request, 'blog/home.html', context)

class PostListView(ListView):
    model = Post
    template_name = 'blog/home.html '
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 5

class UserPostListView(ListView):
    template_name = 'blog/user_posts.html '
    context_object_name = 'posts'
    queryset = get_user_model().objects.all()
    def get_context_data(self, **kwargs):
        context = super(UserPostListView, self).get_context_data(**kwargs)
        context['posts'] = Post.objects.filter(author__username=self.kwargs['username']).order_by('-date_posted')
        context['prods'] = Prod.objects.filter(userr__username=self.kwargs['username']).order_by('-date_posted')
        context['services'] = Service.objects.filter(userr__username=self.kwargs['username'])
        return context

    
def PostLike(request, pk):
    post = get_object_or_404(Post, id=request.POST.get('post_id'))
    if post.likes.filter(id=request.user.id).exists():
        post.likes.remove(request.user)
    else:
        post.likes.add(request.user)

    return HttpResponseRedirect(reverse('post-detail', args=[str(pk)]))

class PostDetailView(DetailView):
    model = Post
#likes
    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        likes_connected = get_object_or_404(Post, id=self.kwargs['pk'])
        liked = False
        if likes_connected.likes.filter(id=self.request.user.id).exists():
            liked = True
        data['number_of_likes'] = likes_connected.number_of_likes()
        data['post_is_liked'] = liked
        #comments
        comments_connected = Comment.objects.filter(
            post_connected=self.get_object()).order_by('-date_posted')
        data['comments'] = comments_connected
        if self.request.user.is_authenticated:
            data['comment_form'] = NewCommentForm(instance=self.request.user)
        return data

    def post(self, request, *args, **kwargs):
        new_comment = Comment(content=request.POST.get('content'),
                                  author=self.request.user,
                                  post_connected=self.get_object())
        new_comment.save()
        return self.get(self, request, *args, **kwargs)
def DeleteComment(request, comment_id):
            user = request.user
            Comment.objects.filter(id=comment_id, author=user).delete()
            return redirect('/')
           
class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'content']



    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)



class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'content']


    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


def about(request):
    return render(request, 'blog/about.html', {'title': 'About'})




@login_required
def PostSearch(request):
  query = request.GET.get("q")
  context = {}
  
  if query:
    posts = Post.objects.filter(Q(title__icontains=query))

    #Pagination
    paginator = Paginator(posts, 6)
    page_number = request.GET.get('page')
    posts_paginator = paginator.get_page(page_number)

    context = {
        'posts': posts_paginator,
      }
  
  template = loader.get_template('users/search_post.html')
  
  return HttpResponse(template.render(context, request))

