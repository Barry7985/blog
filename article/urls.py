from django.urls import path, reverse_lazy

app_name = 'articles'

from .views import (
    ArticleDetailView,
    ArticleDeleteView,
    list_article,
    formulaire,
    get_and_update,
    add_comment,
    contact_view,
    moderate_comment,
)

urlpatterns = [
    path('list_article/', list_article, name='list_article'),
    path('formulaire/', formulaire, name='form_article'),
    path('edit/<uuid:uuid>/', get_and_update, name='edit'),
    path('delete/<uuid:uuid>/', ArticleDeleteView.as_view(success_url=reverse_lazy('articles:list_article')), name='delete'),
    path('add-comment/<uuid:uuid>/', add_comment, name='add-comment'),
    path('moderate-comment/<int:comment_id>/', moderate_comment, name='moderate-comment'),
    path('detail/<uuid:uuid>/', ArticleDetailView.as_view(), name='detail'),
    path('contact/', contact_view, name='contact'),
]
