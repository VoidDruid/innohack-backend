from django.urls import path

from .views import *

urlpatterns = [
    path('site-event', SiteEventCreateView.as_view()),
    path('worker', WorkerCreateView.as_view()),
    path('site', SiteCreateView.as_view()),
    path('position', PositionView.as_view())
]
