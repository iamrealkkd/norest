from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import NoteFileForm, ProcessOptionsForm
from .models import NoteFile
from PyPDF2 import PdfReader
from gtts import gTTS
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer
import os
from django.conf import settings
import docx

@login_required
def upload_file(request):
    if request.method == 'POST':
        form = NoteFileForm(request.POST, request.FILES)
        if form.is_valid():
            note = form.save(commit=False)
            note.user = request.user
            note.save()
            
            # Process the file based on user's options
            return redirect('process_options', note_id=note.id)
    else:
        form = NoteFileForm()
    return render(request, 'notes/upload.html', {'form': form})

@login_required
def process_options(request, note_id):
    note = NoteFile.objects.get(id=note_id, user=request.user)
    
    if request.method == 'POST':
        form = ProcessOptionsForm(request.POST)
        if form.is_valid():
            # Extract text from file
            text = extract_text_from_file(note.file.path)
            note.processed_text = text
            note.save()
            
            # Process based on options
            if form.cleaned_data['generate_summary']:
                summary = generate_summary(text, form.cleaned_data['summary_length'])
                note.summary = summary
                note.save()
                
            if form.cleaned_data['generate_audio']:
                audio_path = generate_audio(text, note.title)
                note.audio_file = audio_path
                note.save()
                
            return redirect('note_detail', note_id=note.id)
    else:
        form = ProcessOptionsForm()
    return render(request, 'notes/process_options.html', {'form': form, 'note': note})

def extract_text_from_file(file_path):
    if file_path.endswith('.pdf'):
        reader = PdfReader(file_path)
        text = " ".join([page.extract_text() for page in reader.pages])
    elif file_path.endswith('.docx'):
        doc = docx.Document(file_path)
        text = " ".join([para.text for para in doc.paragraphs])
    else:  # txt file
        with open(file_path, 'r') as f:
            text = f.read()
    return text

def generate_summary(text, length='medium'):
    sentences = {
        'short': 3,
        'medium': 5,
        'long': 7
    }.get(length, 5)
    
    parser = PlaintextParser.from_string(text, Tokenizer("english"))
    summarizer = LsaSummarizer()
    summary = summarizer(parser.document, sentences)
    return " ".join([str(sentence) for sentence in summary])

def generate_audio(text, title):
    tts = gTTS(text=text, lang='en')
    audio_path = os.path.join(settings.MEDIA_ROOT, 'audio', f"{title.replace(' ', '_')}.mp3")
    tts.save(audio_path)
    return os.path.join('audio', f"{title.replace(' ', '_')}.mp3")

@login_required
def note_detail(request, note_id):
    note = NoteFile.objects.get(id=note_id, user=request.user)
    return render(request, 'notes/note_detail.html', {'note': note})

@login_required
def note_list(request):
    notes = NoteFile.objects.filter(user=request.user).order_by('-uploaded_at')
    return render(request, 'notes/note_list.html', {'notes': notes})
