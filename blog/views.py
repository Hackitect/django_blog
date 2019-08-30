from django.shortcuts import render
# from django.http import HttpResponse


posts = [
    {
        'Author': 'Charles Njenga',
        'Title': 'Blog 1',
        'Content': 'Blog 1 Content',
        'Date_Posted': 'August 30, 2019'
    },
    {
        'Author': 'Jane Doe',
        'Title': 'Blog 2',
        'Content': 'Blog 2 Content',
        'Date_Posted': 'August 27, 20189'
    }
]


def home(request):
    context = {
        'posts': posts
    }
    return render(request, 'blog/home.html', context)


def about(request):
    return render(request, 'blog/about.html', {'title': 'Wamlambez'})
