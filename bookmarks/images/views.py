from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse, HttpResponse
from django.views.decorators.http import require_POST
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
import redis
from django.conf import settings

from .forms import ImageCreateForm
from .models import Image
from common.decorators import ajax_required
from actions.utils import create_action

# connect to redis
r = redis.Redis(host=settings.REDIS_HOST,
                port=settings.REDIS_PORT,
                db=settings.REDIS_DB)


# Create your views here.
@login_required
def image_create(request):
    if request.method == "POST":
        form = ImageCreateForm(data=request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            new_item = form.save(commit=False)

            new_item.user = request.user
            new_item.save()
            create_action(request.user, 'bookmarked image', new_item)
            messages.success(request, "Image added successfully!")
            return redirect(new_item.get_absolute_url())
    else:
        form = ImageCreateForm(data=request.GET)

    context = {'form': form, 'section': 'images'}
    return render(request, 'images/image/create.html', context=context)


def image_detail(request, image_id, image_slug):
    image = get_object_or_404(Image, id=image_id, slug=image_slug)

    # increment total_views by 1, if key:value pair is not exist incr will create it
    total_views = r.incr(f'image:{image.id}:views')

    context = {'image': image, 'section': 'images', 'total_views': total_views}
    return render(request, 'images/image/detail.html', context=context)


@ajax_required
@login_required
@require_POST
def image_like(request):
    image_id = request.POST.get('id')
    action = request.POST.get('action')

    if image_id and action:
        try:
            image = Image.objects.get(id=image_id)
            if action == 'like':
                image.users_like.add(request.user)
                create_action(request.user, 'likes', image)
            else:
                image.users_like.remove(request.user)
            return JsonResponse({'status': 'ok'})
        except:
            pass
    return JsonResponse({'status': 'error'})


@login_required
def image_list(request):
    images = Image.objects.all()
    paginator = Paginator(images, 20)
    page = request.GET.get('page')

    try:
        images = paginator.page(page)
    except PageNotAnInteger:
        images = paginator.page(1)
    except EmptyPage:
        if request.is_ajax():
            return HttpResponse('')
        images = paginator.page(paginator.num_pages)

    context = {'section': 'images', 'images': images}
    if request.is_ajax():
        return render(request, 'images/image/list_ajax.html', context=context)

    return render(request, 'images/image/list.html', context=context)
