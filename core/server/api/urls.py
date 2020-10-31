from django.urls import path

from .views import *

urlpatterns = [
    path('site-event', SiteEventCreateView.as_view()),
 #   path('site-worker', SiteCreateView.as_view()),
     path('site', SiteCreateView.as_view())
]
