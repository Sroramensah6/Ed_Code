from django import forms
from tinymce import TinyMCE
from .models import QuestionModel, Answers


class TinyMCEWidget(TinyMCE):
    def use_required_attribute(self, *args):
        return False


class QuestionForm(forms.ModelForm):
    content = forms.CharField(
        widget=TinyMCEWidget(
            attrs={'required': False, 'cols': 30, 'rows': 10}
        )
    )

    class Meta:
        model = QuestionModel
        fields = ('title', 'content', 'tags')


class AnswerForm(forms.ModelForm):
    content = forms.CharField(
        widget=TinyMCEWidget(
            attrs={'required': False, 'cols': 30, 'rows': 10}
        )
    )

    class Meta:
        model = Answers
        fields = ('content',)
