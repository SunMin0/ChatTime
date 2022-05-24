from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.shortcuts import render
from src.NLG import NaturalLanguageGenerator

# Create your views here.


@login_required(login_url='/login')
def f_chat(request):
    if request.method == "GET":
        try:
            text = request.GET.get('query') # 물음표 제거
            text = text.replace('?', '')
            if request.GET.get('query') != None:
                try:
                    nlg = NaturalLanguageGenerator()
                    answer = nlg.run_nlg(text)[0]
                except:
                    answer = "죄송해요. 알아듣지 못했어요."
                return render(request, 'chat/chat.html', {'text': text, 'answer': answer})
        except:
            print("except")
        return render(request, 'chat/chat.html')
    elif request.method == "POST":
        if 'blobURL' in request.POST:
            blobURL = request.POST['blobURL']
            context = {
             'blobURL': blobURL
            }
            return JsonResponse(context)


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