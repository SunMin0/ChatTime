from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from src.NLG import NaturalLanguageGenerator
from django.views.decorators.csrf import csrf_exempt
import json

nlg = NaturalLanguageGenerator()

@csrf_exempt
def chatbot(request):
    get_data = json.loads(request.body.decode('utf-8'))
    text = get_data['message']
    data = {
        'message': nlg.run_nlg(text)
    }
    return JsonResponse(data)

def f_chat(request):
    return render(request, "chat.html")

def f_chats(request):
    return render(request, 'chats.html')

def f_find(request):
    return render(request, 'find.html')

def f_more(request):
    return render(request, 'more.html')

def f_profile(request):
    return render(request, 'profile.html')

def f_index(request):
    return render(request, 'index.html')