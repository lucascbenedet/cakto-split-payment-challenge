from django.urls import path
from .views import RetrieveProductView, ListCreateProductView, GetActiveRules

urlpatterns = [
    path('', ListCreateProductView.as_view()),
    path('<uuid:pk>', RetrieveProductView.as_view()),
    path('<uuid:pk>/rules', GetActiveRules.as_view()),
    
]