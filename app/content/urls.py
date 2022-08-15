from django.urls import path
from . import views
# Create your views here.

# download/
urlpatterns = [
    path('attachment/<uuid:uuid>/', views.download_attachment, name='attachment_download' ),
    path('ajax/feed/<slug:feed_slug>/', views.FeedView.as_view(), name='ajax_feed_page' ),
    # path('ajax/feed/page/<slug:slug>/', views.ajax_feed_page, name='ajax_feed_page' ),
    # path('ajax/post/', views.ajax_post, name='ajax_post' ),
    # path('ajax/post/<slug:slug>/', views.ajax_post, name='ajax_feed' ),
    # path('ajax/feed/<slug:slug>/', views.load_feed, name='feed' ),
]
