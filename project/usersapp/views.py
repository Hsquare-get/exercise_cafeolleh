from django.contrib.auth.hashers import make_password, check_password
from django.shortcuts import render, redirect

# Create your views here.
from usersapp.models import Users


def login(request):
    context = None
    #POST방식으로 요청받으면, usermail에는 POST 방식으로 받아온 input name이 email인 value 값을 가져오고,
    # 그 값이 없으면 오류가 아니라 default값으로 None으로 처리한다.(하지만 input 방식이 required이기 때문에 입력받은 값이 없을 수는 없다.)
    if request.method == 'POST':
        useremail = request.POST.get('email', None)
        password = request.POST.get('password', None)
        try:
            user = Users.objects.get(useremail=useremail) #Users 클래스의 모든 객체를 가져오려면 Users.objects.all() 해주고
                                                        #Users 클래스의 useremail 객체 하나만을 가져오려면 Users.objects.get(useremail=useremail)으로 가져온다
        except Users.DoesNotExist: #예외처리문 : useremail을 get 해오지 못하면 (db에 등록된 email이 없을 경우 email을 get해오지 못함)
            context = {'error': '아이디 또는 비밀번호가 일치하지 않습니다.'}
            return render(request,'login.html',context) #error 메시지를 login.html로 딕셔너리 형태로 전달한다
        else: #try에서 오류없이 통과했으면
            user_name=user.username
            print(user_name)
            if check_password(password, user.password): #만약 입력한 비밀번호와 db에 등록된 user.password가 같으면
                request.session['user'] = user_name #'user' key의 value를 위에서 받아온 user_name으로 세션에 저장한다.
                return redirect('/mainapp/home/') #로그인에 성공했으면 /mainapp/home/ 으로 redirect한다.
            else:
                context = {'error': '아이디 또는 비밀번호가 일치하지 않습니다.'} #만약 입력한 비밀번호와 db에 등록된 user.password가 다르면
                return render(request, 'login.html', context) #다시 login 페이지로 rendering하고 에러 메시지를 전달한다. (alert해주기 위해서)
    else:
        return render(request, 'login.html', context) #맨 처음 GET방식으로 접근하면 login.html로 렌더링



def register(request):
    if request.method =='GET':
        return render(request, 'register.html')
    elif request.method == 'POST':
        useremail = request.POST.get('email', None) #POST방식으로 받아온 name이 email input의 value값을 useremail 변수에 저장한다.
        username = request.POST.get('name', None)
        password = request.POST.get('password', None)
        re_password = request.POST.get('re-password', None)
        res_data={}
        if password != re_password:
            res_data['error']='비밀번호가 다릅니다.'
            return render(request, 'register.html', res_data) #비밀번호가 다르면 다시 register.html로 res_data 딕셔너리를 전달한다.
                                                            #register.html로 가서 res_data의 'error'가 있으면 alert 할 예정
        else: #1차 비밀번호와 2차 비밀번호가 같으면
            users = Users(
                useremail=useremail,
                username=username,
                password=make_password(password)
            )
            users.save() #확정 저장
            return render(request,'login.html') #이메일과 이름과 비밀번호가 모두 등록이 됐으면 로그인 페이지로 렌더링


def forgot(request):
    if request.method == "POST":
        useremail=request.POST.get("email")
        try:
            user = Users.objects.get(useremail=useremail)
        except Users.DoesNotExist:
            context = {'error': '없는 이메일 주소입니다.'}
            return render(request,'forgot.html',context)
        else:
            request.session['email']=useremail
            return redirect('/usersapp/pwreset/?email='+useremail)
    else:
        return render(request, 'forgot.html')

def pwreset(request):
    if request.method == "POST":
        password=request.POST.get("password")
        re_password=request.POST.get("re-password")
        e = request.GET.get('email', "NotFound")
        if password != re_password:
            return render(request,'pwreset.html',context={"error":"비밀번호가 일치하지 않습니다.",'email':e})
        else:
            if e == "NotFound": return render(request,'/usersapp/forgot/',{'error':"변경할 이메일을 입력해 주세요."})
            user=Users.objects.get(useremail=e)
            user.password=make_password(password)
            user.save()
            return redirect("usersapp:login")
    else:
        e=request.GET.get('email',"NotFound")
        if e == "NotFound": return render(request, 'forgot.html', {'error': "변경할 이메일을 입력해 주세요."})
        return render(request, 'pwreset.html',{'email':request.GET['email']})
