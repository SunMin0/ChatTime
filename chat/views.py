from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from src.NLG import NaturalLanguageGenerator
from src.NLU import NaturalLanguageUnderstanding
import re

# Create your views here.

def f_chat(request):
    if request.method == "GET":
        try:
            text = request.GET.get('query')
            text = re.sub('[-=+,#/\?:^$.@*\"※~&%ㆍ!』\\‘|\(\)\[\]\<\>`\'…》]', '', text) # 특수문자 제거
            text = re.sub('쥬스','주스',text)
            print(text)
            if request.GET.get('query') != None:
                try:
                    # intent 확인을 위한 임시 테스트 코드 -----------------
                    nlu = NaturalLanguageUnderstanding()
                    nlu.model_load()
                    intent, predict = nlu.predict(text)
                    print(text, intent, predict)
                    answer = intent
                    # ---------------------------------------------------

                    # 원본 코드 아래 두줄----------------------------------
                    # nlg = NaturalLanguageGenerator()
                    # answer = nlg.run_nlg(text)[0]
                    # ---------------------------------------------------
                except:
                    answer = "죄송해요. 알아듣지 못했어요."
                return render(request, 'chat.html', {'text': text, 'answer': answer})
        except:
            print("except")
        return render(request, 'chat.html')
    elif request.method == "POST":
        if 'blobURL' in request.POST:
            blobURL = request.POST['blobURL']
            context = {
             'blobURL': blobURL
            }
            return JsonResponse(context)

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