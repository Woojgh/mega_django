from django import forms
from ENV/lib/python3.6/site-packages/photologue/models.py import Gallery

class ProjectUploadForm(forms.ModelForm):
    """Image upload form."""
    class Meta:
        model = Gallery
        include = ['date_added', 'title', 'slug', 'description', 'is_public', 'photos', ]