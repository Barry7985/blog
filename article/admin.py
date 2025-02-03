from django.contrib import admin
from article.models import Article,Comment,Category
# Register your models here.
admin.site.register(Article)
admin.site.register(Comment)
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')