from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import DetailView
from django.views.generic import DeleteView
from .forms import ArticleForm, CommentForm
from .models import Article


def list_article(request):
    arts = Article.objects.all()
    context = {
        'articles': arts
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