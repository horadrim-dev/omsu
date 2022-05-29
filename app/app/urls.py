"""app URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from . import views

# УДАЛИТЬ +static() и эти библиотеки на боевом сервере
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('grappelli/', include('grappelli.urls')), # grappelli URLS
    path('admin/', admin.site.urls),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('download/', include('content.urls')),
    path('sitemap/', views.sitemap),
    path('', views.main),

    path('<slug:cat1>/', views.route), #, name='index'),
    path('<slug:cat1>/<slug:cat2>/', views.route),
    path('<slug:cat1>/<slug:cat2>/<slug:cat3>/', views.route),
    path('<slug:cat1>/<slug:cat2>/<slug:cat3>/<slug:cat4>/', views.route),
    path('<slug:cat1>/<slug:cat2>/<slug:cat3>/<slug:cat4>/<slug:cat5>/', views.route),
    # path('home/', views.main),
    # path('news/', include('newsfeed.urls', namespace='newsfeed')),
] #+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# for section in Menu.objects.filter(level=1):
#     urlpatterns += [
#         path(
#             section.alias + '/', 
#             include(('menus.urls', section.alias), 
#             namespace=section.alias), 
#             {'section':section}
#         )
#     ]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
