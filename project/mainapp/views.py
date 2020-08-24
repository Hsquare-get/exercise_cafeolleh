from django.core.paginator import Paginator
from django.http import JsonResponse
from django.shortcuts import render, redirect

# Create your views here.

def home(request):
    #session에 user 정보가 저장되어있으면 로그인 상태 표시(이름으로)
    if 'user' in request.session:
        context={'user_name':request.session.get('user')}
        return render(request,'home.html',context)
    else:
        return render(request,'home.html')

def logout(request):
    #session에 user 정보가 저장되어있으면 지우고, 지워졌으면 로그인 상태가 아닌 home.html을 render
    if 'user' in request.session:
        del request.session['user']
        return render(request,'home.html')

def best9(request):
    return render(request,'bestmenu.html')