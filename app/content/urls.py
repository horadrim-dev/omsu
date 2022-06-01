from django.urls import path
from . import views
# Create your views here.

# download/
urlpatterns = [
    path('attachment/<uuid:uuid>/', views.download_attachment, name='attachment_download' ),
    path('feed/<slug:slug>/', views.load_feed_page, name='feed_page' ),
]
