import uuid
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from ckeditor_uploader.fields import RichTextUploadingField
from django.utils.text import slugify

# Create your models here.
class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True, verbose_name='nom du tag')
    slug = models.SlugField(unique=True, null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Tag'
        verbose_name_plural = 'Tags'

class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name='nom de la catégorie')
    description = models.TextField(blank=True, null=True, verbose_name='description')
    slug = models.SlugField(unique=True, null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Catégorie'
        verbose_name_plural = 'Catégories'

class Article(models.Model):
    STATUS_CHOICES = [
        ('draft', 'Brouillon'),
        ('published', 'Publié'),
        ('archived', 'Archivé'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255, verbose_name='titre')
    slug = models.SlugField(unique=True, null=True, blank=True)
    sumary = models.CharField(max_length=255, blank=True, null=True, verbose_name='resume')
    content = RichTextUploadingField(blank=True, null=True, verbose_name='contenu')
    date_pub = models.DateField(null=True, default=timezone.now, blank=True)
    cover = models.ImageField(upload_to='articles', max_length=255, null=True, verbose_name="photo de couverture")
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='catégorie')
    tags = models.ManyToManyField(Tag, blank=True, verbose_name='tags')
    user = models.ForeignKey(User, on_delete=models.PROTECT, null=True, blank=False)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft', verbose_name='statut')
    featured = models.BooleanField(default=False, verbose_name='article en vedette')
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
            # If slug already exists, append a number
            counter = 1
            while Article.objects.filter(slug=self.slug).exists():
                self.slug = f"{slugify(self.title)}-{counter}"
                counter += 1
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Article'
        verbose_name_plural = 'Articles'
        ordering = ['-date_pub']

class Comment(models.Model):
    STATUS_CHOICES = [
        ('pending', 'En attente'),
        ('approved', 'Approuvé'),
        ('rejected', 'Rejeté'),
    ]

    name = models.TextField(verbose_name='Nom', null=True)
    content = models.TextField(verbose_name='Commentaire')
    created_at = models.DateTimeField(auto_now_add=True)
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    owner = models.ForeignKey(User, on_delete=models.PROTECT, null=True, blank=False)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending', verbose_name='statut')
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='replies')

    def __str__(self):
        return f"{self.created_at}"

    class Meta:
        verbose_name = 'Commentaire'
        verbose_name_plural = 'Commentaires'
        ordering = ['-created_at']

class Contact(models.Model):
    name = models.CharField(max_length=100, verbose_name='Nom')
    email = models.EmailField(verbose_name='Email')
    subject = models.CharField(max_length=200, verbose_name='Sujet')
    message = models.TextField(verbose_name='Message')
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.name} - {self.subject}"

    class Meta:
        verbose_name = 'Message de contact'
        verbose_name_plural = 'Messages de contact'

