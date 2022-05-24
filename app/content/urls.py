from django.urls import path
from . import views
# Create your views here.

urlpatterns = [
    path('attachment/<uuid:uuid>/', views.download_attachment, name='attachment_download' ),
]
