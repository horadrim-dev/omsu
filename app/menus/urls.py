from django.urls import path
from . import views
# Create your views here.

urlpatterns = [
    path('', views.categories, name='activity'),
    # path('<slug:category>/', views.subcategories),
    # path('<slug:category>/<slug:slug>/', views.content),
    # path('', views.menus, name='activity'),
    path('<slug:cat1>/', views.menus),
    path('<slug:cat1>/<slug:cat2>/', views.menus),
    path('<slug:cat1>/<slug:cat2>/<slug:cat3>/', views.menus),
]
