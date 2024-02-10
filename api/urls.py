from django.urls import path
from . import views
from .views import web_scraper_view, screenshot_view

urlpatterns = [
    path('getData/', views.getData),
    path('addData/', views.addItem),
    path('screenshot/', views.screenshot_view, name='take_screenshot'),
    path('fetch-content/', web_scraper_view, name='fetch_content'),
]