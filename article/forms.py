from django import forms
from .models import Article, Comment

class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ('title', 'sumary', 'cover', 'date_pub', 'content')
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'sumary': forms.TextInput(attrs={'class': 'form-control'}),
            'date_pub': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'cols': 80, 'rows': 10}),
            'cover': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('name','content')
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control',}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }
