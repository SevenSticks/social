from django.forms import ModelForm

from .models import Post


class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = ['group', 'text']
        labels = {
            'group': 'Групппа.',
            'text': 'Текст.'
        }
        help_texts = {
            'group': 'Выбирите группу в которой хотите опубликовать статью.',
            'text': 'Введите текст статьи.'
        }
