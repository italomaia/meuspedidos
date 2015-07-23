from django import forms
from .models import CandidateApplication, SkillScore, ExpectedSkill


class CandidateApplicationForm(forms.ModelForm):
    class Meta:
        model = CandidateApplication
        fields = ('name', 'email')

    def __init__(self, *args, **kwargs):
        super(CandidateApplicationForm, self).__init__(*args, **kwargs)

        for field_name in self.fields:
            field = self.fields[field_name]

            if field.required:
                field.widget.attrs['required'] = 'required'


class SkillForm(forms.ModelForm):
    class Meta:
        model = SkillScore
        exclude = ("candidate_application",)

    def __init__(self, *args, **kwargs):
        super(SkillForm, self).__init__(*args, **kwargs)
        current_widget = self.fields['expected_skill'].widget
        new_widget = forms.HiddenInput()
        new_widget.is_required = current_widget.is_required
        new_widget.attrs = current_widget.attrs
        self.fields['expected_skill'].widget = new_widget
