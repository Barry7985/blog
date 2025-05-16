from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views.generic import DetailView, ListView
from django.views.generic import DeleteView
from django.db.models import Q
from .forms import ArticleForm, CommentForm, CommentModerationForm
from .models import Article, Category, Contact, Tag, Comment
from django.core.paginator import Paginator
from .filters import ArticleFilter
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings

def list_article(request):
    articles = Article.objects.filter(status='published')
    
    # Get filter parameters
    category = request.GET.get('category')
    tag = request.GET.get('tag')
    search = request.GET.get('search')
    
    if category:
        articles = articles.filter(category__slug=category)
    if tag:
        articles = articles.filter(tags__slug=tag)
    if search:
        articles = articles.filter(
            Q(title__icontains=search) |
            Q(content__icontains=search) |
            Q(sumary__icontains=search)
        )
    
    # Apply the filter
    article_filter = ArticleFilter(request.GET, queryset=articles)
    filtered_articles = article_filter.qs

    # Pagination
    paginator = Paginator(filtered_articles, 9)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Get all categories and tags for the sidebar
    categories = Category.objects.all()
    tags = Tag.objects.all()

    context = {
        'filter': article_filter,
        'page_obj': page_obj,
        'categories': categories,
        'tags': tags,
    }
    return render(request, 'articles/list_articles.html', context)

@login_required
def formulaire(request):
    if request.method == 'POST':
        form = ArticleForm(request.POST, files=request.FILES)
        if form.is_valid():
            article = form.save(commit=False)
            article.user = request.user
            article.save()
            messages.success(request, 'Article créé avec succès!')
            return redirect(reverse('articles:list_article'))
    else:
        form = ArticleForm()
    context = {
        'form': form
    }
    return render(request, 'articles/formulaire.html', context)

@login_required
def get_and_update(request, uuid):
    article = get_object_or_404(Article, id=uuid)
    if request.method == 'GET':
        form = ArticleForm(instance=article)
    elif request.method == 'POST':
        form = ArticleForm(instance=article, data=request.POST, files=request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Article mis à jour avec succès!')
            return redirect(reverse('articles:list_article'))
    context = {
        'article': article,
        'form': form
    }
    return render(request, 'articles/edit.html', context)

@login_required
def add_comment(request, uuid):
    article = get_object_or_404(Article, id=uuid)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.article = article
            comment.owner = request.user
            comment.save()
            messages.success(request, 'Commentaire ajouté avec succès!')
        else:
            messages.error(request, 'Erreur lors de l\'ajout du commentaire.')
    return redirect('articles:detail', uuid=article.uuid)

@login_required
def moderate_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    if request.method == 'POST':
        form = CommentModerationForm(request.POST, instance=comment)
        if form.is_valid():
            form.save()
            messages.success(request, 'Statut du commentaire mis à jour!')
    return redirect('articles:detail', pk=comment.article.id)

class ArticleDetailView(DetailView):
    model = Article
    template_name = 'articles/article_detail.html'
    context_object_name = 'article'
    pk_url_kwarg = 'uuid'

    def get_queryset(self):
        # Allow viewing if user is authenticated and is the author, or if article is published
        if self.request.user.is_authenticated:
            return Article.objects.filter(
                Q(status='published') | 
                Q(user=self.request.user)
            )
        return Article.objects.filter(status='published')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        article = self.get_object()
        
        # Add comment form and approved comments
        context['form'] = CommentForm()
        context['comments'] = article.comment_set.filter(
            status='approved', 
            parent=None
        ).order_by('-created_at')
        
        # Add related articles
        context['related_articles'] = Article.objects.filter(
            status='published',
            category=article.category
        ).exclude(id=article.id)[:3]
        
        return context

    def get_object(self, queryset=None):
        try:
            return super().get_object(queryset)
        except Article.DoesNotExist:
            messages.error(self.request, "L'article demandé n'existe pas ou n'est pas accessible.")
            return None

class ArticleDeleteView(LoginRequiredMixin, DeleteView):
    model = Article
    template_name = 'articles/article_delete.html'
    success_url = reverse_lazy('articles:list_article')
    pk_url_kwarg = 'uuid'

    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Article supprimé avec succès!')
        return super().delete(request, *args, **kwargs)

def contact_view(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        
        contact = Contact.objects.create(
            name=name,
            email=email,
            subject=subject,
            message=message
        )
        
        email_message = f"""
        Nouveau message de contact reçu:
        
        De: {name} ({email})
        Sujet: {subject}
        
        Message:
        {message}
        """
        
        send_mail(
            subject=f'Nouveau message de contact: {subject}',
            message=email_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[settings.ADMIN_EMAIL],
            fail_silently=False,
        )
        
        messages.success(request, 'Votre message a été envoyé avec succès!')
        return redirect('articles:contact')
        
    return render(request, 'article/contact.html')