from django.shortcuts import render, get_object_or_404 ,redirect
from django.http import HttpResponseRedirect
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from .models import Post , Comment
from django.views.generic import ( ListView,
                                   DetailView, 
                                   CreateView,
                                   UpdateView,
                                   DeleteView
)
from django.db.models import Exists, OuterRef
from users.forms import CommentForm
from django.contrib import messages

def home(request):
  context = {
     'posts': Post.objects.all()
  }
  return render (request,'blog/home.html',context)

class PostListView(ListView):
    model = Post
    template_name = 'blog/home.html'
    context_object_name = 'posts'
    ordering = ['-date_created']
    paginate_by = 5

class UserPostListView(ListView):
    model = Post
    template_name = 'blog/user_posts.html'
    context_object_name = 'posts'
    paginate_by = 5

    def get_queryset(self):
        user =  get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date_created')

class PostDetailView(DetailView):
    model = Post 
    is_liked = False

    def get_queryset(self, *args, **kwargs):
      return super().get_queryset(*args, **kwargs).annotate(
          is_liked=Exists(Post.likes.through.objects.filter(
              user_id=self.request.user.id,
              post_id=OuterRef('pk')
           ))
      )
        
class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title','content']

    def form_valid(self, form):
      form.instance.author=self.request.user
      return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title','content']

    def form_valid(self, form):
      form.instance.author=self.request.user
      return super().form_valid(form)

    def test_func(self):
      post = self.get_object()
      if self.request.user==post.author:
          return True
      return False

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post

    success_url = '/'

    def test_func(self):
      post = self.get_object()
      if self.request.user==post.author:
          return True
      return False


def about(request):
  return render (request,'blog/about.html')

def like_post(request):
  post = get_object_or_404(Post, id=request.POST.get('post_id'))
  is_liked=False
  if post.likes.filter(id=request.user.id).exists():
    post.likes.remove(request.user)
    is_liked = False
  else:
    post.likes.add(request.user)
    is_liked = True
  return HttpResponseRedirect(post.get_absolute_url())

def commentpage(request,pk):
  post = Post.objects.get(id=pk)
  comments = Comment.objects.filter(post=post).order_by('-id')
  total_comment =  Comment.objects.filter(post=post).count()
  form = CommentForm()
  if request.method == 'POST':
    form = CommentForm(request.POST)
    if form.is_valid():
      content = request.POST.get('content')
      comment = Comment.objects.create(post=post, user=request.user, content=content)
      comment.save()
      messages.success(request,f'Successfully added your comment')
      return redirect('/')
    else:
      form.errors()
  return render(request,'blog/commentpage.html',{'form':form, 'comments':comments, 
  'total_comment':total_comment})


def delete_comment(request,pk):
  comment = Comment.objects.get(id=pk)
  comment.delete()
  messages.success(request,f'Successfully deleted your comment')
  return redirect('/')
