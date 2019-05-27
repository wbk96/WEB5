from django.shortcuts import render,redirect,reverse,get_object_or_404
from django.http import HttpResponse,HttpResponseRedirect
from django.template import loader
from .models import User,biaoti,mysuser
from django.contrib.auth import authenticate,login as lgi ,logout as lgo
from django.contrib.auth.models import User as u
from django.core.mail import send_mail,EmailMultiAlternatives
from django.conf import settings
# 引入序列化加密并且有效期信息
from itsdangerous import TimedJSONWebSignatureSerializer as serializer,SignatureExpired
# 引入绘图模块
from PIL import Image,ImageDraw,ImageFont
import random,io
# Create your views here.

def checklogin(fun):
    def check(request,*args):
        # name=request.session.get('username')
        # pwd=request.session.get('userpwd')
        if request.user and request.user.is_authenticated:
            return fun(request,*args)
        else:
            return redirect(reverse('tou1:login'))
    return check

@checklogin
def index(request):
    username=request.session.get('username')
    ti=biaoti.objects.all()
    return render(request,'booktest/index.html', locals())
    # ti= biaoti.objects.all()
    # temp=loader.get_template('booktest/index.html')
    # result=temp.render({'ti':ti})
    # return HttpResponse(result)

@checklogin
def list(request,id):
    string = biaoti.objects.get(pk=id)
    name = string.user_set.all()
    if request.method=="GET":
        return render(request,'booktest/list.html',{'name':name,'id':id,'string':string})
    elif request.method=='POST':
        userid=request.POST['sex']
        username=User.objects.get(pk=userid)
        username.pool+= 1
        username.save()
        return HttpResponseRedirect('/tou1/detail/%s/'%id)

@checklogin
def detail(request,id):
    string = biaoti.objects.get(pk=id)
    name = string.user_set.all()
    temp=loader.get_template('booktest/detail.html')
    result=temp.render({'name':name,'string':string})
    # print(result)
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
        try:
            username = request.POST.get('username_req')
            pwd = request.POST.get('userpwd_req1')
            verifycode = request.POST.get('verify')

            if verifycode == request.session.get('verifycode'):
                # user= authenticate(request, username = username,password = pwd)
                # print(user,'??????')
                user = get_object_or_404(mysuser, username=username)
                if not user.is_active:
                    return render(request, 'booktest/login.html', {"error": '用户尚未激活'})
                else:
                    check = user.check_password(pwd)
                    if check:
                        lgi(request, user)
                        return redirect(reverse('tou1:index'))
                    else:
                        render(request, 'booktest/login.html', {'error': '用户名或密码错误'})
                # if user:
                #     if user.is_active:
                #         lgi(request,mysuser)
                #         return redirect(reverse('tou1:index'))
                #     else:
                #         return render(request,'booktest/login.html',{"error":'用户尚未激活'})
                # else:
                #     render(request,'booktest/login.html',{'error':'用户名或密码错误'})
            else:
                return render(request, 'booktest/login.html', {'error': '验证码错误'})
        except Exception as e:
            return render(request, 'booktest/login.html', {'error': '请输入正确的数据'})

def logout(request):
    ret=redirect(reverse('tou1:login'))
    # request.session.flush()
    lgo(request)
    return ret

def register(request):
    if request.method=='POST':
        try:
            username = request.POST.get('username')
            pwd = request.POST.get('userpwd')
            pwd2 = request.POST.get('userpwd_req')
            email = request.POST.get('email')
            error = None
            if pwd != pwd2:
                error = '密码有误'
                return render(request, 'booktest/login.html', {'error': error})
            else:
                user = mysuser.objects.create_user(username=username, password=pwd)
                user.is_active = False
                user.save()
                # url='http://127.0.0.1:8002/tou1/active/%s'%(user.id,)
                # send_mail('点击激活用户',url,settings.DEFAULT_FROM_EMAIL,[email])
                # 为了防止非人为激活，需将地址加密
                # 带有有效期的序列化
                # 得到序列化工具
                serutil = serializer(settings.SECRET_KEY)
                # 使用工具对字典对象序列化，打印的RESULT是字节型
                # result=serutil.dumps({'userid':user.id})
                # 序列化转字符串
                result = serutil.dumps({'userid': user.id}).decode('utf-8')

                mail = EmailMultiAlternatives('点击激活用户',
                                              '<a href = "http://127.0.0.1:8002/tou1/active/%s/">点击激活</a>' % (result),
                                              settings.DEFAULT_FROM_EMAIL, [email])
                mail.content_subtype = 'html'
                mail.send()
                return render(request, 'booktest/login.html', {"error": '请在一小时内激活'})
        except Exception as e:
            return render(request, 'booktest/login.html', {'error': '请输入正确的数据'})

def findpwd(request):
    if request.method=='GET':
        return render(request,'booktest/findpwd.html')
    else:
        try:
            tel=request.POST.get('tel')
            if tel.user_set.all():
                return redirect(reverse('tou1:login'))
            else:
                return render(request,'booktest/findpwd.html',{'error',"账号不存在"})
        except Exception as e:
            return redirect(reverse('tou1:findpwd'),{'error':'请重新填写'})

def active(request,info):
    serutil = serializer(settings.SECRET_KEY)
    try:
        obj=serutil.loads(info)
        id=obj['userid']
        user=get_object_or_404(mysuser,pk=id)
        user.is_active=True
        user.save()
        return redirect(reverse('tou1:login'))
    except SignatureExpired as e:
        return HttpResponse('链接失效')

def verify(request):
    # 每次请求验证码，需要使用pillow构造出图像，返回
    # 定义变量，用于画面的背景色、宽、高
    bgcolor = (random.randrange(20, 100),
               random.randrange(20, 100),
               random.randrange(20, 100))
    width = 100
    heigth = 25
    # 创建画面对象
    im = Image.new('RGB', (width, heigth), bgcolor)
    # 创建画笔对象
    draw = ImageDraw.Draw(im)
    # 调用画笔的point()函数绘制噪点
    for i in range(0, 100):
        #随机位置
        xy = (random.randrange(0, width), random.randrange(0, heigth))
        # 随机颜色
        fill = (random.randrange(0, 255), 255, random.randrange(0, 255))
        draw.point(xy, fill=fill)
    # 定义验证码的备选值
    str1 = 'ABCD123EFGHIJK456LMNOPQRS789TUVWXYZ0'
    # 随机选取4个值作为验证码
    rand_str = ''
    for i in range(0, 4):
        rand_str += str1[random.randrange(0, len(str1))]
    # 构造字体对象
    font = ImageFont.truetype('BRUSHSCI.TTF', 23)
    fontcolor = (255, random.randrange(0, 255), random.randrange(0, 255))
    # 绘制4个字
    draw.text((5, 2), rand_str[0], font=font, fill=fontcolor)
    draw.text((25, 2), rand_str[1], font=font, fill=fontcolor)
    draw.text((50, 2), rand_str[2], font=font, fill=fontcolor)
    draw.text((75, 2), rand_str[3], font=font, fill=fontcolor)
    # 释放画笔
    del draw
    request.session['verifycode'] = rand_str
    f = io.BytesIO()
    im.save(f, 'png')
    # 将内存中的图片数据返回给客户端，MIME类型为图片png
    return HttpResponse(f.getvalue(), 'image/png')


def checkuser(request):
    if request.method=='POST':
        username=request.POST.get('username_req')
        if mysuser.objects.filter(username=username).first():
            return HttpResponse('用户存在')
        else:
            return HttpResponse('用户不存在')