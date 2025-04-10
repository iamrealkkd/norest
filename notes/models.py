from django.db import models
from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator

class NoteFile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    file = models.FileField(
        upload_to='notes/',
        validators=[FileExtensionValidator(allowed_extensions=['pdf', 'docx', 'txt'])]
    )
    uploaded_at = models.DateTimeField(auto_now_add=True)
    processed_text = models.TextField(blank=True, null=True)
    summary = models.TextField(blank=True, null=True)
    audio_file = models.FileField(upload_to='audio/', blank=True, null=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-uploaded_at']
