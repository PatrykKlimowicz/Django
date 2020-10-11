from django.urls import path
from . import views

app_name = 'images'

urlpatterns = [
    path('create/', views.image_create, name='create'),
    path('detail/<int:image_id>/<slug:image_slug>/', views.image_detail, name='detail'),
]
