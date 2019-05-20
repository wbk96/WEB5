from django.shortcuts import render,redirect,reverse
from django.http import HttpResponse,HttpResponseRedirect
from django.template import loader
from .models import User,biaoti
# Create your views here.

def checklogin(fun):
    def check(request,*args):
        name=request.session.get('username')
        print(name)
        pwd=request.session.get('userpwd')
        print(pwd)
        if name and pwd:
            return fun(request,*args)
        else:
            return redirect(reverse('tou1:login'))
    print(check,'我是check')
    return check
@checklogin
def index(request):
    username=request.session.get('username')
    ti=User.objects.all()
    print(locals())
    return render(request,'booktest/index.html', locals())
    # ti= biaoti.objects.all()
    # temp=loader.get_template('booktest/index.html')
    # result=temp.render({'ti':ti})
    # return HttpResponse(result)
@checklogin
def list(request,id):
    string = biaoti.objects.get(pk=id)
    # print(string)
    name = string.user_set.all()
    if request.method=="GET":
        return render(request,'booktest/list.html',{'name':name,'id':id,'string':string})
    elif request.method=='POST':
        userid=request.POST['sex']
        username=User.objects.get(pk=userid)
        username.pool+= 1
        username.save()
        # print(userid,username,username.pool)
        return HttpResponseRedirect('/tou1/detail/%s/'%id)
@checklogin
def detail(request,id):
    string = biaoti.objects.get(pk=id)
    name = string.user_set.all()
    temp=loader.get_template('booktest/detail.html')
    result=temp.render({'name':name,'string':string})
    print(result)
    return HttpResponse(result)

def add(request):
    if request.method=="GET":
        return render(request,'booktest/add.html')
    elif request.method=='POST':
        string=biaoti()
        string.string= request.POST['name']
        string.save()
        return HttpResponseRedirect('/tou1/index/')

def addtemp(request,id):
    our=biaoti.objects.get(pk=id)
    if request.method=='GET':
        return render(request,'booktest/addtemp.html',{'id':id,'our':our})
    elif request.method=='POST':
        name=request.POST['biaoti']
        id=biaoti.objects.get(string=name).id
        ou=User()
        ou.name=request.POST['name']
        ou.pool=0
        ou.string_id=id
        ou.save()
        return HttpResponseRedirect('/tou1/detail/%s/'%id)

def login(request):
    if request.method=='GET':
        return render(request,'booktest/login.html')
    else:
        request.session['username']=request.POST['username']
        request.session['userpwd'] = request.POST['userpwd']
        return redirect(reverse('tou1:index'))


def logout(request):
    ret=redirect(reverse('tou1:login'))
    request.session.flush()
    return ret





