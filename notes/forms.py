from django import forms
from .models import NoteFile

class NoteFileForm(forms.ModelForm):
    class Meta:
        model = NoteFile
        fields = ['title', 'file']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'file': forms.FileInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'title': 'Note Title',
            'file': 'Upload File (PDF, DOCX, TXT)'
        }

class ProcessOptionsForm(forms.Form):
    generate_summary = forms.BooleanField(
        required=False,
        initial=True,
        label='Generate Summary'
    )
    generate_audio = forms.BooleanField(
        required=False,
        initial=True,
        label='Generate Audio Version'
    )
    summary_length = forms.ChoiceField(
        choices=[('short', 'Short'), ('medium', 'Medium'), ('long', 'Long')],
        initial='medium',
        widget=forms.RadioSelect,
        label='Summary Length'
    )
