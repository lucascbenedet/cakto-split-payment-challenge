
from django.urls import path
from .views import CreateSplits


urlpatterns = [
    path('', CreateSplits.as_view())
]