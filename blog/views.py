from django.shortcuts import render
# from django.http import HttpResponse


posts = [
    {
        'author': 'Charles Njenga',
        'title': 'Blog 1',
        'content': 'Blog 1 Content',
        'date_posted': 'August 30, 2019'
    },
    {
        'author': 'Jane Doe',
        'title': 'Blog 2',
        'content': 'Blog 2 Content',
        'date_posted': 'August 27, 20189'
    }
]


def home(request):
    context = {
        'posts': posts
    }
    return render(request, 'blog/home.html', context)


def about(request):
    return render(request, 'blog/about.html', {'title': 'Wamlambez'})
