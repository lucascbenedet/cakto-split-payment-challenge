
from django.urls import path
from .views import CreateSplits, UpdateSplitStatus


urlpatterns = [
    path('', CreateSplits.as_view()),
    path('<uuid:split_id>/status/', UpdateSplitStatus.as_view()),
]