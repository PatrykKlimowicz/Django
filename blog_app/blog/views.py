from django.shortcuts import render, get_object_or_404
from .models import Post
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
# Create your views here.


def post_list(request):
    object_list = Post.published.all()
    paginator = Paginator(object_list, 1)  # one post on each site
    page = request.GET.get('page')  # obtain current page number

    try:
        posts = paginator.page(page)  # obtain posts for desired page
    except PageNotAnInteger:
        # if page not an integer return first page
        posts = paginator.page(1)
    except EmptyPage:
        # if page index out of range return last page
        posts = paginator.page(paginator.num_pages)

    context = {'page': page, 'posts': posts}
    return render(request, 'blog/post/list.html', context=context)


def post_detail(request, year, month, day, post):
    post = get_object_or_404(Post, slug=post,
                             status='published',
                             publish__year=year,
                             publish__month=month,
                             publish__day=day)
    context = {'post': post}
    return render(request, 'blog/post/detail.html', context=context)
