from django.urls import path
from . import views
from .views import web_scraper_view, screenshot_view

urlpatterns = [
    path('reports/', views.get_reports),
    path('report/add/', views.add_report),
    path('screenshot/', views.screenshot_view, name='take_screenshot'),
    path('fetch-content/', web_scraper_view, name='fetch_content'),
]
