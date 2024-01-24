from django.urls import path # This line imports the 'path' function from 'django.urls'. This function is used to
# define URL patterns.
# from .views import FormResponseView # This line imports the 'FormResponseView' class from the 'views.py' file.

from . import views # This line imports the 'views.py' file.

# Define your routes here
# TODO: Define your routes here

urlpatterns = [
    path('getData/', views.getData),
    path('addData/', views.addItem),
    path('form/', views.form, name='form'),
]

# urlpatterns = [
#     path('', views.getData),
#     path('submit-form/', FormResponseView.as_view(), name='submit-form'),
# ]

