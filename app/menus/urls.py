from django.urls import path
from . import views
# Create your views here.

urlpatterns = [
    path('', views.categories, name='activity'),
    path('<slug:category>/', views.subcategories),
    path('<slug:category>/<slug:slug>/', views.content),
]
