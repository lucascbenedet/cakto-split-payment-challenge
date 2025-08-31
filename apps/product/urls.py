from django.urls import path
from .views import RetrieveProductView, ListCreateProductView

urlpatterns = [
    path('', ListCreateProductView.as_view()),
    path('<uuid:pk>', RetrieveProductView.as_view()),
    
]