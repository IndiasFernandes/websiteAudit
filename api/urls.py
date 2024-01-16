from django.urls import path
from .views import FormResponseView

# Define your routes here
# TODO: Define your routes here

urlpatterns = [
    path('submit-form/', FormResponseView.as_view(), name='submit-form'),
]
