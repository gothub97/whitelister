from django.urls import path
from .views import TokenProfileView, ContractAnalysisView, ContractAnalysisListView, TokenListView, HolderAnalysisView

urlpatterns = [
    path('token/<str:address>/', TokenProfileView.as_view(), name='token-profile'),
    path('token/', TokenListView.as_view(), name='token-list'),
    path('token/<uuid:token_id>/analyse/contract/', ContractAnalysisView.as_view(), name='contract-analysis'),
    path('token/<uuid:token_id>/analyses/contract/', ContractAnalysisListView.as_view(), name='contract-analysis-list'),
    path('api/token/<uuid:token_id>/analyses/holders/', HolderAnalysisView.as_view()),
]