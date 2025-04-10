from django.contrib import admin
from .models import NoteFile

@admin.register(NoteFile)
class NoteFileAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'uploaded_at')
    list_filter = ('user', 'uploaded_at')
    search_fields = ('title', 'processed_text')
