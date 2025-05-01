from django.urls import path

app_name = 'articles'

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
    path('edit/<uuid:id>/', get_and_update, name='edit'),
    path('delete/<uuid:pk>/', ArticleDeleteView.as_view(), name='delete'),
    path('add-comment/<uuid:pk>/', add_comment, name='add-comment'),
    path('detail/<uuid:pk>/', ArticleDetailView.as_view(), name='detail'),
]
