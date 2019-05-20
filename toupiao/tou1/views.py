from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from django.template import loader
from .models import User,biaoti
# Create your views here.

def index(request):
    ti= biaoti.objects.all()
    temp=loader.get_template('booktest/index.html')
    result=temp.render({'ti':ti})
    return HttpResponse(result)

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

def detail(request,id):
    string = biaoti.objects.get(pk=id)
    name = string.user_set.all()
    temp=loader.get_template('booktest/detail.html')
    result=temp.render({'name':name,'string':string})
    return HttpResponse(result)

def add(request):
    if request=="GET":
        print('get')
        return render(request,'booktest/index.html')
    elif request=='POST':
        print('post')
        # return HttpResponse('sucess')









