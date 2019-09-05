from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    DeleteView
)
from django.shortcuts import render
from .models import Post
# from django.http import HttpResponse


# posts = [
#     {
#         'author': 'Charles Njenga',
#         'title': 'Blog 1',
#         'content': 'Blog 1 Content',
#         'date_posted': 'August 30, 2019'
#     },
#     {
#         'author': 'Jane Doe',
#         'title': 'Blog 2',
#         'content': 'Blog 2 Content',
#         'date_posted': 'August 27, 20189'
#     }
# ]


def home(request):
    context = {
        'posts': Post.objects.all()
    }
    return render(request, 'blog/home.html', context)


class PostListView(ListView):
    model = Post
    template_name = 'blog/home.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    ordering = ['-date_posted']


class PostDetailView(DetailView):
    model = Post


class PostDeleteView(DeleteView):
    model = Post

class PostCreateView(CreateView):
    model = Post
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


def about(request):
    return render(request, 'blog/about.html', {'title': 'Wamlambez'})
