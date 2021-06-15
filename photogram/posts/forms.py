from django import forms
from .models import Post


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['image', 'tag']

    image = forms.ImageField(label=u'Фотографии', widget=forms.FileInput(attrs={'multiple': 'multiple'}))


class FilterForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['tag']