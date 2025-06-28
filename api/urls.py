from django.urls import path
from .views import TokenMetadataView

urlpatterns = [
    path('token/<str:address>/', TokenMetadataView.as_view()),
]