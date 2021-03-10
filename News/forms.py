from django import forms
from tinymce import TinyMCE
from .models import NewsPost

from pagedown.widgets import PagedownWidget


class TinyMCEWidget(TinyMCE):
    def use_required_attribute(self, *args):
        return False


class PostForm(forms.ModelForm):
    # content = forms.CharField(
    #     widget=TinyMCEWidget(
    #         attrs={'required': False, 'cols': 30, 'rows': 10}
    #     )
    # )
    # over_view = forms.CharField(widget=PagedownWidget)
    content = forms.CharField(widget=PagedownWidget)

    publish = forms.DateField(widget=forms.SelectDateWidget)

    class Meta:
        model = NewsPost
        fields = ('title', 'over_view', 'thumbnail', 'content', 'publish',
                  'tags',  'featured', 'categories', )

        # , 'previous_post', 'next_post
