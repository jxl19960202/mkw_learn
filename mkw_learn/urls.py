"""mkw_learn URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,re_path,include
from django.views.static import serve  #处理文件的视图
# from mkw_learn.settings import STATIC_ROOT


import xadmin
from users.views import LoginView,IndexView,RegisterView,ActiveUserView,ForgetPwdView
from users.views import ResetView,ModifyPwdView
from mkw_learn.settings import MEDIA_ROOT  #导入上传文件url
from users.views import LogoutView



urlpatterns = [
    #xadmin后台管理系统
    path('xadmin/', xadmin.site.urls),

    #首页
    path('',IndexView.as_view(),name='index'),

    #登入页面
    path('login/',LoginView.as_view(),name = 'login'),

    #用户登出
    path('logout/', LogoutView.as_view(), name="logout"),

    #验证码
    path('captcha/',include('captcha.urls')),

    #注册
    path('register/',RegisterView.as_view(),name = 'register'),

    #激活链接
    re_path('active/(?P<active_code>.*)/',ActiveUserView.as_view(),name='user_active'),

    #忘记密码
    path('forget/',ForgetPwdView.as_view(),name='forget_pwd'),

    #重置密码页面
    re_path('reset/(?P<active_code>.*)/', ResetView.as_view(), name='reset_pwd'),

    #提交修改后密码的逻辑
    path('modify_pwd/', ModifyPwdView.as_view(), name='modify_pwd'),

    #处理图片显示的url,使用Django自带serve,传入参数告诉它去哪个路径找，我们有配置好的路径MEDIAROOT
    re_path(r'^media/(?P<path>.*)', serve, {"document_root": MEDIA_ROOT }),

    #课程机构
    re_path('^org/',include('organization.urls',namespace='org')),

    #课程
    re_path('^course/',include('course.urls',namespace='course')),

    #个人信息
    path("users/", include('users.urls', namespace="users")),

    #DEBUG=False,生产环境下,这里配置静态文件的视图处理
    # re_path(r'^static/(?P<path>.*)', serve, {"document_root": STATIC_ROOT}),

    #富文本编辑
    path('ueditor/', include('DjangoUeditor.urls')),
]


# 全局404页面配置
handler404 = 'users.views.pag_not_found'
# 全局500页面配置
handler500 = 'users.views.page_error'





