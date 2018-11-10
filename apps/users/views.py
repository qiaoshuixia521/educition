from django.shortcuts import render
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.hashers import make_password,check_password
from utils.email_send import send_register_email
from django.http import HttpResponseRedirect
# Create your views here.

from .models import UserProfile,EmailVerifyRecord,Banner
from django.db.models import Q
from django.views.generic.base import View #基于类实现的视图函数
from django.http import HttpResponse
from pure_pagination import Paginator,EmptyPage,PageNotAnInteger


from .form import LoginForm,RegisterForm,ForgetPwdForm,ModifyPwdForm,UploadImageForm,UserInfoForm
from utils.mixin_utils import LoginRequiredMixin
import json
from operation.models import UserCourse,UserFavorite,Course,UserMessage
from organization.models import CourseOrg,Teacher
from django.shortcuts import render_to_response
#邮箱和用户名都可以登录
#基于ModelBackend类，因为他又authenticate方法
class CustomBackend(ModelBackend):
        def authenticate(self,request,username=None,password=None,**kwargs):
            try:
                #不希望用户存在两个，get只能有一个，两个是get是被的以一种原因，Q为使用并集查询
                user=UserProfile.objects.get(Q(username=username)|Q(email=username))
                #由于django后台对密码进行了加密，所以不能使用password==password
                #UserProfile继承的AbstractUser中有def check_password(self,raw_pawweord)

                if user.check_password(password):
                    return user
            except Exception as e:
                return None


#基于方法实现的登录
# def user_login(request):
#     if request.method=='POST':
#         #获取用户提交的用户名和密码
#         user_name=request.POST.get('username',None)
#         pass_word=request.POST.gte('password',None)
#         #成功的话返回user对象，失败的话返回None
#         user=authenticate(username=user_name,password=pass_word)
#         #如果不是null说明验证成功
#         if user is not None:
#             #登录
#             login(request,'index.html')
#         else:
#             return render(request,'login.html',{'msg':'用户名或密码错误'})
#     elif request.method=='GET':
#         return render(request,'login.html')

#将user_login方法的实现改为类的实现
class LoginView(View):


    def get(self,request):
        return render(request,'login.html')

    def post(self,request):
        login_form = LoginForm(request.POST)
        #获取用户提交的用户名和密码
        if login_form.is_valid():
            user_name = request.POST.get('username', None)
            pass_word = request.POST.get('password', None)
            # 成功返回user对象，失败None
            user = authenticate(username=user_name, password=pass_word)
            # 如果不是null说明验证成功
            if user is not None:
                # 登录
                #只有注册激活后才能登录
                if user.is_active:
                    login(request, user)
                    return render(request, 'index.html')


            else:
                return render(request,'login.html',{'msg':'用户名或密码错误','login_form':login_form})
        #from.is_valid()已经判断不合法了，所以这里不需要在返回错误信息到前段了
        else:
            return render(request,'login.html',{'login_form':login_form})


#用户注册
class RegisterView(View):
    def get(self,request):
        register_form=RegisterForm()
        return render(request,'register.html',{'register_form':register_form})


    def post(self,request):
        register_form=RegisterForm(request.POST)
        if register_form.is_valid():
            user_name=request.POST.get('email',None)
            #如果用户已经存在，则提示错误信息
            if UserProfile.objects.filter(email=user_name):
                return render(request,'register.html',{'register_form':register_form,'msg':'用户名已经存在'})
            pass_word=request.POST.get('password',None)
            #实例化一个user_profile对象
            user_profile=UserProfile()
            user_profile.username=user_name
            user_profile.email=user_name
            user_profile.is_active=False
            #保存导数据库的密码加密
            user_profile.password=make_password(pass_word)
            user_profile.save()
            send_register_email(user_name,'register')#发送邮件
            return render(request,'login.html')
        else:
            return render(request,'register.html',{'register_form':register_form})

#用户激活
class ActiveUserView(View):
    def get(self,request,active_code):
        #查询邮箱验证记录是否存在
        all_record=EmailVerifyRecord.objects.filter(code=active_code)

        if all_record:
            for record in all_record:
                #获取到对应的邮箱
                email=record.email
                #查找到邮箱对应的user
                user=UserProfile.objects.get(email=email)
                user.is_active=True
                user.save()
        #验证码不对的时候跳转到激活失败页面
        else:
            return render(request,'active_fail.html')
        return render(request,"login.html",)



class ForgetPwdView(View):
    '''找回密码'''
    def get(self,request):
        forget_form=ForgetPwdForm()
        return render(request,'forgetpwd.html',{'forget_form':forget_form})

    def post(self,request):
        forget_form=ForgetPwdForm(request.POST)
        if forget_form.is_valid():
            email =request.POST.get('email',None)
            send_register_email(email,'forget')
            return render(request,'send_success.html')
        else:
            return render(request,'forgetpwd.html',{'forget_form':forget_form})



class ResetView(View):
    def get(self,request,active_code):
        all_records=EmailVerifyRecord.objects.filter(code=active_code)
        if all_records:
            for record in all_records:
                email=record.email
                return render(request,'password_reset.html',{'email':email})
        else:
            return render(request,"active_fail.html")
        return render(request,"login.html")


class ModifyPwdView(View):
    def post(self,request):
        modify_form=ModifyPwdForm(request.POST)
        if modify_form.is_valid():
            pwd1=request.POST.get("password1",'')
            pwd2=request.POST.get('password2','')
            email=request.POST.get('email','')
            if pwd1 !=pwd2:
                return render(request,"password_reset.html",{"email":email,"msg":"密码不一致"})
            user=UserProfile.objects.get(email=email)
            user.password=make_password(pwd2)
            user.save()

            return render(request,"login.html")
        else:
            email = request.POST.get("email","")
            return render(request,"password_reset.html",{"email":email,"modify_form":modify_form})


class UserinfoView(LoginRequiredMixin,View):
    '''用户个人信息'''
    def get(self,request):
        return render(request,'usercenter-info.html',{

        })

class UploadImageView(LoginRequiredMixin,View):
    '''用户图形上传'''
    def post(self,request):
        #上传的文件都在request.FILES里面获取，所以这里要多传一个参数
        image_form=UploadImageForm(request.POST,request.FILES)
        if image_form.is_valid():
            image=image_form.cleaned_data['image']
            request.user.iamge=image
            request.user.save()
            return HttpResponse('{"status":"success"}',content_type="application/json")
        else:
            return HttpResponse('{"status":"fail"}',content_type="application/json")


class UpdatePwdView(View):

        """
        个人中心修改用户密码
        """

        def post(self, request):
            modify_form = ModifyPwdForm(request.POST)
            if modify_form.is_valid():
                pwd1 = request.POST.get("password1", "")
                pwd2 = request.POST.get("password2", "")
                if pwd1 != pwd2:
                    return HttpResponse('{"status":"fail","msg":"密码不一致"}', content_type='application/json')
                user = request.user
                user.password = make_password(pwd2)
                user.save()

                return HttpResponse('{"status":"success"}', content_type='application/json')
            else:
                return HttpResponse(json.dumps(modify_form.errors), content_type='application/json')


class SendEmailCodeView(LoginRequiredMixin,View):
    '''发送邮箱修改验证码'''
    def get(self,request):
        email=request.GET.get('email','')
        if UserProfile.objects.filter(email=email):
            return HttpResponse('{"email":"邮箱已存在"}',content_type='application/json')
        send_register_email(email,'update_email')
        return HttpResponse('{"status":"success"}',content_type='application/json')


class UpdateEmailView(LoginRequiredMixin,View):
    '''修改邮箱'''
    def post(self,request):
        email=request.POST.get("email","")
        code=request.POST.get("code","")

        existed_records=EmailVerifyRecord.objects.filter(email=email,code=code,send_type='update_email')
        if existed_records:
            user=request.user
            user.email=email
            user.save()
            return HttpResponse('{"status":"success"}',content_type='application/json')
        else:
            return HttpResponse('{"emial":"验证码无效"}',content_type='appliction/json')

class UserInfoView(LoginRequiredMixin,View):
    '''用户个人信息'''
    def get(self,request):
        return render(request,'usercenter-info.html')
    def post(self,request):
        user_info_form=UserInfoForm(request.POST,instance=request.user)
        if user_info_form.is_valid():
            user_info_form.save()
            return HttpResponse('{"status":"success"}',content_type='application/json')
        else:
            return HttpResponse(json.dumps(user_info_form.errors),content_type='application/json')


class MyCourseView(LoginRequiredMixin,View):
    '''我的课程'''
    def get(self,request):
        user_courses=UserCourse.objects.filter(user=request.user)
        return render(request,"usercenter-mycourse.html",{
            "user_courses":user_courses,
        })


class MyFavOrgView(LoginRequiredMixin,View):
    '''我收藏的课程机构'''
    def get(self,request):
        org_list = []
        fav_orgs = UserFavorite.objects.filter(user=request.user, fav_type=2)
        # 上面的fav_orgs只是存放了id。我们还需要通过id找到机构对象
        for fav_org in fav_orgs:
            # 取出fav_id也就是机构的id。
            org_id = fav_org.fav_id
            # 获取这个机构对象
            org = CourseOrg.objects.get(id=org_id)
            org_list.append(org)
        return render(request, "usercenter-fav-org.html", {
            "org_list": org_list,
        })


class MyFavTeacherView(LoginRequiredMixin,View):
    '''我的收藏的授课讲师'''
    def get(self,request):
        teacher_list=[]
        fav_teachers=UserFavorite.objects.filter(user=request.user,fav_type=3)
        for fav_teacher in fav_teachers:
            teacher_id = fav_teacher.fav_id
            teacher = Teacher.objects.get(id=teacher_id)
            teacher_list.append(teacher)
        return render(request, "usercenter-fav-teacher.html", {
            "teacher_list": teacher_list,
        })


class MyFavCourseView(LoginRequiredMixin,View):
    '''我收藏的课程'''

    def get(self, request):
        course_list = []
        fav_courses = UserFavorite.objects.filter(user=request.user, fav_type=1)
        for fav_course in fav_courses:
            course_id = fav_course.fav_id
            course = Course.objects.get(id=course_id)
            course_list.append(course)

        return render(request, 'usercenter-fav-course.html', {
            "course_list": course_list,
        })


class MyMessageView(LoginRequiredMixin,View):
    '''我的消息'''

    def get(self, request):
        all_message = UserMessage.objects.filter(user=request.user.id)

        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(all_message, 4, request=request)
        messages = p.page(page)
        return render(request, "usercenter-message.html", {
            "messages": messages,
        })


class LogoutView(View):
    '''用户登出'''
    def get(self,request):
        logout(request)
        from django.urls import reverse
        return HttpResponseRedirect(reverse('index'))


class IndexView(View):
    '''首页'''
    def get(self,request):
        #轮播图
        all_banners=Banner.objects.all().order_by('index')
        #课程
        courses=Course.objects.filter(is_banner=False)[:6]
        #轮播课程
        banner_courses=Course.objects.filter(is_banner=True)[:3]
        #课程机构
        course_orgs=Course.objects.all()[:15]
        return render(request,'index.html',{
            'all_banners':all_banners,
            'courses':courses,
            'banner_courses':banner_courses,
            'course_orgs':course_orgs,
        })


def page_not_fond(request):
    #全局404处理函数
    response=render_to_response('404.html',{})
    response.status_code=404
    return response


def page_error(request):
    #全局500处理函数
    from django.shortcuts import render_to_response
    response=render_to_response('500.html',{})
    response.status_code=500
    return response