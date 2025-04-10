from django.urls import path
from . import views

app_name = 'notes'

urlpatterns = [
    path('', views.note_list, name='note_list'),
    path('upload/', views.upload_file, name='upload_file'),
    path('note/<int:note_id>/', views.note_detail, name='note_detail'),
    path('note/<int:note_id>/process/', views.process_options, name='process_options'),
]
