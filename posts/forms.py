from django import forms
from .models import Post, Comment, Community

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'featured_image', 'content', 'crypto_ticker']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 5}),
            'crypto_ticker': forms.TextInput(attrs={'placeholder': 'e.g., BTC'}),
        }

    community = forms.ModelChoiceField(queryset=Community.objects.all(), required=False, empty_label="Select a community (Optional)")


class CommentForm(forms.ModelForm):
    """
    Form class for users to comment on a post
    """
    class Meta:
        """
        Specify the django model and order of the fields
        """
        model = Comment
        fields = ('body',)