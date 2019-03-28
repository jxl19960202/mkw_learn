from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator


#在用户点击学习之前,用户应该是登入状态,如果用户没登入,返回登入页面,用户登入进入课程章节页面
# 如果是用函数方式写的话直接加个装饰器（@login_required）就可以，但是我们是用类的方式写的，必须用继承的方式
#让评论视图,章节视图继承该类
class LoginRequiredMixin(object):
    @method_decorator(login_required(login_url='/login/'))
    def dispatch(self,request,*args,**kwargs):
        return super(LoginRequiredMixin, self).dispatch(request,*args,**kwargs)