from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout as auth_logout
from .models import StudyMaterial
import json

def home(request):
    return render(request, 'repository/home.html')

@login_required
def upload_material(request):
    if request.method == 'POST':
        title = request.POST['title']
        description = request.POST.get('description', '')
        tags = request.POST.get('tags', '')
        link = request.POST['link']
        StudyMaterial.objects.create(
            title=title,
            description=description,
            tags=tags,
            link=link
        )
        return redirect('home')
    return render(request, 'repository/upload_material.html')

@login_required
def search_materials(request):
    tag = request.GET.get('tag')
    title = request.GET.get('title')
    query = StudyMaterial.objects.all()
    if tag:
        query = query.filter(tags__icontains=tag)
    if title:
        query = query.filter(title__icontains=title)
    materials = query
    return JsonResponse([{
        "title": m.title,
        "description": m.description,
        "tags": m.tags,
        "link": m.link
    } for m in materials], safe=False)

@login_required
def chatbot(request):
    if request.method == 'POST':
        user_message = json.loads(request.body).get('message', '').lower()
        response_message = "I didn't understand that. Can you try again?"

        if any(greeting in user_message for greeting in ['hello', 'hi', 'hey']):
            response_message = 'Hello! How can I assist you today?'
        elif 'good morning' in user_message:
            response_message = 'Very good morning! How can I help you?'
        elif 'good afternoon' in user_message:
            response_message = 'Good afternoon! How can I help you?'
        elif 'good evening' in user_message:
            response_message = 'Good evening! How can I help you?'
        elif 'good night' in user_message:
            response_message = 'Good night! Have a great sleep'
        elif 'upload' in user_message:
            response_message = 'Sure! Please provide the title of the study material.'
            request.session['upload_state'] = 'title'
        elif any(term in user_message for term in ['search', 'download', 'access']):
            response_message = 'What tag or title are you looking for?'
            request.session['search_state'] = True
        elif request.session.get('upload_state'):
            upload_state = request.session['upload_state']
            if upload_state == 'title':
                request.session['upload_title'] = user_message
                response_message = 'Got it. Please provide a description.'
                request.session['upload_state'] = 'description'
            elif upload_state == 'description':
                request.session['upload_description'] = user_message
                response_message = 'Great. Now provide some tags (comma separated).'
                request.session['upload_state'] = 'tags'
            elif upload_state == 'tags':
                request.session['upload_tags'] = user_message
                response_message = 'Almost done! Please provide the link to the study material.'
                request.session['upload_state'] = 'link'
            elif upload_state == 'link':
                StudyMaterial.objects.create(
                    title=request.session['upload_title'],
                    description=request.session['upload_description'],
                    tags=request.session['upload_tags'],
                    link=user_message
                )
                response_message = 'Thank you! Your study material has been uploaded. Have a great day!'
                del request.session['upload_state']
                request.session.pop('upload_title', None)
                request.session.pop('upload_description', None)
                request.session.pop('upload_tags', None)
        elif request.session.get('search_state'):
            query = StudyMaterial.objects.filter(tags__icontains=user_message) | StudyMaterial.objects.filter(title__icontains=user_message)
            if query.exists():
                response_message = 'Here are the materials I found:<br>' + '<br>'.join([f'{m.title} : <a href="{m.link}" target="_blank">{m.link}</a>' for m in query])
                #response_message = 'Here are the materials I found:\n' + '\n'.join([f"{m.title}: {m.link}" for m in query])
            else:
                response_message = 'No study materials found for that tag or title.'
            del request.session['search_state']

        return JsonResponse({'response': response_message})
    return render(request, 'repository/chatbot.html')

@login_required
def logout(request):
    auth_logout(request)
    return render(request, 'repository/logout.html')
