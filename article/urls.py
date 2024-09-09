from django.urls import path
from .views import (
    ArticleDetailView,
    ArticleDeleteView,
    list_article,
    formulaire,
    get_and_update,
    add_comment,
)

urlpatterns = [
    path('list_article/', list_article, name='list_article'),
    path('formulaire/', formulaire, name='form-article'),
    path('edit/<int:id>/', get_and_update, name='edit'),
    path('delete/<int:pk>/', ArticleDeleteView.as_view(), name='delete'),
    path('add-comment/<int:id>/', add_comment, name='add-comment'),
    path('detail/<int:pk>/', ArticleDetailView.as_view(), name='detail'),
]
