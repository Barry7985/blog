from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import DetailView
from django.views.generic import DeleteView
from .forms import ArticleForm, CommentForm
from .models import Article, Category
from django.core.paginator import Paginator
from .filters import ArticleFilter

def list_article(request):
    # Récupérer tous les articles
    articles = Article.objects.all()

    # Appliquer le filtre
    article_filter = ArticleFilter(request.GET, queryset=articles)
    filtered_articles = article_filter.qs

    # Pagination
    paginator = Paginator(filtered_articles, 9)  # 9 articles par page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Récupérer toutes les catégories
    categories = Category.objects.all()

    context = {
        'filter': article_filter,
        'page_obj': page_obj,
        'categories': categories,  # Passer les catégories au template
    }
    return render(request, 'articles/list_articles.html', context)

@login_required  # decorateur
def formulaire(request):
    if request.method == 'POST':
        form = ArticleForm(request.POST, files=request.FILES)
        if form.is_valid():
            article = form.save(commit=False)
            article.user = request.user
            article.save()  # enregistrement dans la base
            return redirect(reverse('list_article'))
    else:
        form = ArticleForm()
    context = {
        'form': form
    }
    return render(request, 'articles/formulaire.html', context)

@login_required
def get_and_update(request, id):
    article = Article.objects.get(id=id)  # recuperation d'un article
    if request.method == 'GET':
        form = ArticleForm(instance=article)  # creation d'un formulaire
    elif request.method == 'POST':
        form = ArticleForm(instance=article, data=request.POST, files=request.FILES)  # creation d'un formulaire
        if form.is_valid():
            form.save()
            return redirect(reverse('list_article'))
    context = {
        'article': article,
        'form': form
    }
    return render(request, 'articles/edit.html', context)


def add_comment(request, id):

    if request.method == 'POST':
        article = Article.objects.get(id=id)
        # initial = {'article': article}
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.article = article
            comment.owner = request.user
            comment.save()
        else:
            context = {
                'article': article,
                'form': form
            }
            return render(request, 'articles/article_detail.html', context)
    return redirect('detail', article.id)

class ArticleDetailView(DetailView):
    model = Article
    template_name = 'articles/article_detail.html'
    context_object_name = 'article'

    def get_context_data(self, **kwargs: any) -> dict[str, any]:
        context = super().get_context_data(**kwargs)
        context['form'] = CommentForm()
        return context
        
        
class ArticleDeleteView(LoginRequiredMixin, DeleteView):
    model = Article
    template_name = 'articles/article_delete.html'
    success_url = reverse_lazy('list_article')