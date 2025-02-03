import django_filters
from .models import Article, Category

class ArticleFilter(django_filters.FilterSet):
    category = django_filters.ModelChoiceFilter(
        queryset=Category.objects.all(),
        field_name='category',
        label='Catégorie',
    )

    class Meta:
        model = Article
        fields = ['category']