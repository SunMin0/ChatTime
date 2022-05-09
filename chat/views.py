from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.shortcuts import render
from src.NLG import NaturalLanguageGenerator

# Create your views here.



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

def f_chats(request):
    return render(request, 'chat/chats.html')

def f_find(request):
    return render(request, 'chat/find.html')

def f_more(request):
    return render(request, 'chat/more.html')

def f_profile(request):
    return render(request, 'chat/profile.html')

def f_index(request):
    return render(request, 'chat/index.html')