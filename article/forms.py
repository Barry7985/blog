from django import forms
from .models import Article, Comment, Tag
from django.utils.text import slugify

class ArticleForm(forms.ModelForm):
    tags = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Tags séparés par des virgules'}),
        help_text='Entrez les tags séparés par des virgules'
    )

    class Meta:
        model = Article
        fields = ['title', 'sumary', 'content', 'cover', 'category', 'status', 'featured']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'sumary': forms.TextInput(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={'class': 'form-control ckeditor'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'featured': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.slug = slugify(instance.title)
        
        if commit:
            instance.save()
            
            # Handle tags
            if self.cleaned_data['tags']:
                tag_names = [tag.strip() for tag in self.cleaned_data['tags'].split(',')]
                for tag_name in tag_names:
                    tag, created = Tag.objects.get_or_create(
                        name=tag_name,
                        defaults={'slug': slugify(tag_name)}
                    )
                    instance.tags.add(tag)
        
        return instance

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

class CommentModerationForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['status']
        widgets = {
            'status': forms.Select(attrs={'class': 'form-control'}),
        }
