from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.shortcuts import render
from src.NLG import NaturalLanguageGenerator
from django.views.decorators.csrf import csrf_exempt
import json

nlg = NaturalLanguageGenerator()

@csrf_exempt
@login_required(login_url='/login')
def chatbot(request):
    get_data = json.loads(request.body.decode('utf-8'))
    text = get_data['message']
    data = {
        'message': nlg.run_nlg(request, text)
    }
    return JsonResponse(data)

@login_required(login_url='/login')
def f_chat(request):
    return render(request, "chat/chat.html")

@login_required(login_url='/login')
def f_chats(request):
    return render(request, 'chat/chats.html')


@login_required(login_url='/login')
def f_cafe(request):
    return render(request, 'chat/cafe.html')


@login_required(login_url='/login')
def f_more(request):
    return render(request, 'chat/more.html')

@login_required(login_url='/login')
def f_profile(request):
    return render(request, 'chat/profile.html')


@login_required(login_url='/login')
def f_index(request):
    return render(request, 'chat/index.html')


@login_required(login_url='/login')
def espresso(request):
    return render(request, 'cafe/espresso.html')

@login_required(login_url='/login')
def decaffeine(request):
    return render(request, 'cafe/decaffeine.html')

@login_required(login_url='/login')
def smoothie(request):
    return render(request, 'cafe/smoothie.html')

@login_required(login_url='/login')
def tea(request):
    return render(request, 'cafe/tea.html')