from django.urls import path

from .views import *

urlpatterns = [
    path('site-event', SiteEventCreateView.as_view()),
    path('position', PositionView.as_view()),
    path('worker', WorkerCreateView.as_view()),
    path('worker/<str:pk>', WorkerView.as_view()),
    path('site', SiteCreateView.as_view()),
    path('site/short', ShortSiteListView.as_view()),
    path('site/<str:pk>', SiteView.as_view()),
    path('site/short/<str:pk>', ShortSiteView.as_view()),
    path('metrics', SensorReportView.as_view()),
]
