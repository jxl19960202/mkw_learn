from django.shortcuts import render
from django.views.generic.base import View
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger   #分页
from django.http import HttpResponse
from django.db.models import Q

from .models import CityDict,CourseOrg,Teacher
from .forms import UserAskForm
from operation.models import UserAsk,UserFavorite
from course.models import Course

# Create your views here.



class OrgView(View):
    #机构列表页
    def get(self,request):
        all_city = CityDict.objects.all()
        all_orgs = CourseOrg.objects.all()

        # 机构搜索功能
        search_keywords = request.GET.get('keywords', '')
        if search_keywords:
            # 在name字段进行操作,做like语句的操作。i代表不区分大小写
            # or操作使用Q
            all_orgs = all_orgs.filter(Q(name__icontains=search_keywords) | Q(desc__icontains=search_keywords))

        #机构关键字查询
        search_keywords = request.GET.get('keywords', '')
        if search_keywords:
            # 名字,描述包含关键字查询  Q的与或非查询 contains包含查询,前面加i,表示不区分大小写
            all_course = all_orgs.filter(Q(name__icontains=search_keywords) | Q(desc__icontains=search_keywords))

        #根据所在城市以及机构类型进行筛选
        city_id = request.GET.get('city','')
        if city_id:
            all_orgs = all_orgs.filter(city_id=city_id)

        category = request.GET.get('ct', '')
        if category:
            all_orgs = all_orgs.filter(category=category)

        org_count = all_orgs.count()   #all_org 的queryset集中有几个元素


        #点击数最高的5个课程机构
        all_hot_orgs = all_orgs.order_by('-click_nums')[:5]   #order_by('-click_nums'),括号内  加- :从大到小,不加,从小到大

        #根据学生人数 课程数进行排序
        sort = request.GET.get('sort','')
        if sort == "students":
            all_orgs = all_orgs.order_by('-students')
        elif sort == "courses":
            all_orgs = all_orgs.order_by('-course_nums')

        #分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        # Paginator() 传入一个可迭代参数,一个数字(1页显示的元素个数)
        # 如 p= Paginator([1,2,3,4,5,6], 2, request=request)  分为3页,及[1,2],[3,4],[5,6]
        p = Paginator(all_orgs, 5, request=request)
        orgs = p.page(page)

        return render(request, "org-list.html", {
            "all_orgs": orgs,
            "all_citys": all_city,
            "org_count": org_count,
            "city_id":city_id,
            "ct":category,
            "hot_orgs":all_hot_orgs,
            "sort":sort
        })


class AddUserAskView(View):
    """
    用户添加咨询
    """
    def post(self, request):
        userask_form = UserAskForm(request.POST)
        if userask_form.is_valid():
            user_ask = userask_form.save(commit=True)
            # 如果保存成功,返回json字符串,后面content type是告诉浏览器返回的数据类型
            return HttpResponse('{"status":"success"}', content_type='application/json')
        else:
            # 如果保存失败，返回json字符串,并将form的报错信息通过msg传递到前端
            return HttpResponse('{"status":"fail", "msg":"添加出错"}', content_type='application/json')


class OrgHomeView(View):
    '''机构首页'''

    def get(self,request,org_id):
        current_page = 'home'   #用户给前端标记
        # 根据id找到课程机构
        course_org = CourseOrg.objects.get(id=int(org_id))
        # 反向查询到课程机构的所有课程和老师
        all_courses = course_org.course_set.all()[:4]
        all_teacher = course_org.teacher_set.all()[:2]

        #进入机构home页面,点击数加1
        course_org.click_nums += 1
        course_org.save()

        #判断是否收藏
        has_fav = False
        if request.user.is_authenticated:
            if UserFavorite.objects.filter(user=request.user, fav_id=course_org.id, fav_type=2):
                has_fav = True

        return render(request,'org-detail-homepage.html',{
            'course_org':course_org,
            'all_courses':all_courses,
            'all_teacher':all_teacher,
            'current_page': current_page,
            'has_fav': has_fav
        })


class OrgCourseView(View):
    """
   机构课程列表页
    """
    def get(self, request, org_id):
        current_page = 'desc'
        # 根据id取到课程机构
        course_org = CourseOrg.objects.get(id= int(org_id))
        # 通过课程机构找到课程。内建的变量，找到指向这个字段的外键引用
        all_courses = course_org.course_set.all()

        #判断是否收藏
        has_fav = False
        if request.user.is_authenticated:
            if UserFavorite.objects.filter(user=request.user, fav_id=course_org.id, fav_type=2):
                has_fav = True

        return render(request, 'org-detail-course.html',{
           'all_courses':all_courses,
            'course_org': course_org,
            'current_page': current_page,
            'has_fav': has_fav
        })


class OrgDescView(View):
    '''机构介绍页'''
    def get(self, request, org_id):
        current_page = 'desc'
        # 根据id取到课程机构
        course_org = CourseOrg.objects.get(id= int(org_id))

        #判断是否收藏
        has_fav = False
        if request.user.is_authenticated:
            if UserFavorite.objects.filter(user=request.user, fav_id=course_org.id, fav_type=2):
                has_fav = True
        return render(request, 'org-detail-desc.html',{
            'course_org': course_org,
            'current_page':current_page,
            'has_fav': has_fav
        })


class OrgTeacherView(View):
    """
   机构教师页
    """
    def get(self, request, org_id):
        current_page = 'teacher'
        course_org = CourseOrg.objects.get(id= int(org_id))
        all_teacher = course_org.teacher_set.all()

        #判断是否收藏
        has_fav = False
        if request.user.is_authenticated:
            if UserFavorite.objects.filter(user=request.user, fav_id=course_org.id, fav_type=2):
                has_fav = True

        return render(request, 'org-detail-teachers.html',{
           'all_teacher':all_teacher,
            'course_org': course_org,
            'current_page':current_page,
            'has_fav':has_fav
        })


class AddFavView(View):
    """
    用户收藏和取消收藏
    """
    def post(self, request):
        id = request.POST.get('fav_id', 0)         # 防止后边int(fav_id)时出错
        type = request.POST.get('fav_type', 0)     # 防止int(fav_type)出错

        if not request.user.is_authenticated:
            # 未登录时返回json提示未登录，跳转到登录页面是在ajax中做的
            return HttpResponse('{"status":"fail", "msg":"用户未登录"}', content_type='application/json')

        exist_record = UserFavorite.objects.filter(user=request.user, fav_id=int(id), fav_type=int(type))
        if exist_record:
            # 如果记录已经存在，表示用户取消收藏
            exist_record.delete() #删除数据表中的记录

            #取消收藏,收藏数减一,当收藏数小于0,变为0
            #课程收藏数
            if int(type) == 1:
                course = Course.objects.get(id=int(id))
                course.fav_nums -= 1
                if course.fav_nums < 0:
                    course.fav_nums = 0
                course.save()
            #机构收藏数
            elif int(type) == 2:
                org = CourseOrg.objects.get(id=int(id))
                org.fav_nums -= 1
                if org.fav_nums < 0:
                    org.fav_nums = 0
                org.save()
            #讲师收藏数
            elif int(type) == 3:
                teacher = Teacher.objects.get(id=int(id))
                teacher.fav_nums -= 1
                if teacher.fav_nums < 0:
                    teacher.fav_nums = 0
                teacher.save()

            return HttpResponse('{"status":"success", "msg":"收藏"}', content_type='application/json')
        else:
            #收藏记录不存在,进行收藏
            user_fav = UserFavorite()
            if int(id) > 0 and int(type) > 0:
                user_fav.user = request.user
                user_fav.fav_id = int(id)
                user_fav.fav_type = int(type)
                user_fav.save()

                #收藏数加1
                #课程收藏数加1
                if int(type) == 1:
                    course = Course.objects.get(id=int(id))
                    course.fav_nums += 1
                    course.save()
                #课程机构收藏数加1
                elif int(type) == 2:
                    org = CourseOrg.objects.get(id=int(id))
                    org.fav_nums += 1
                    org.save()
                #讲师收藏数加1
                elif int(type) == 3:
                    teacher = Teacher.objects.get(id=int(id))
                    teacher.fav_nums += 1
                    teacher.save()

                return HttpResponse('{"status":"success", "msg":"已收藏"}', content_type='application/json')
            else:
                return HttpResponse('{"status":"fail", "msg":"收藏出错"}', content_type='application/json')


class TeacherListView(View):
    def get(self, request):
        all_teachers = Teacher.objects.all()

        # 搜索功能
        search_keywords = request.GET.get('keywords', '')
        if search_keywords:
            # 在name字段进行操作,做like语句的操作。i代表不区分大小写
            # or操作使用Q
            all_teachers = all_teachers.filter(name__icontains=search_keywords)

        # 总共有多少老师使用count进行统计
        teacher_nums = all_teachers.count()

        # 人气排序
        sort = request.GET.get('sort','')
        if sort:
            if sort == 'hot':
                all_teachers = all_teachers.order_by('-click_nums')

        #讲师排行榜
        sorted_teacher = Teacher.objects.all().order_by('-click_nums')[:3]
        # 进行分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(all_teachers, 1, request=request)
        teachers = p.page(page)

        return render(request, "teachers-list.html", {
            "all_teachers": teachers,
            "teacher_nums": teacher_nums,
            'sorted_teacher':sorted_teacher,
            'sort':sort,
        })



class TeacherDetailView(View):
    #讲师详情页
    def get(self, request, teacher_id):
        teacher = Teacher.objects.get(id=int(teacher_id))
        all_course = Course.objects.filter(teacher=teacher)

        #进入讲师详情页,点击数加1
        teacher.click_nums += 1
        teacher.save()

        # 讲师排行榜
        sorted_teacher = Teacher.objects.all().order_by('-click_nums')[:3]
        return render(request, 'teacher-detail.html', {
            'teacher': teacher,
            'all_course': all_course,
            'sorted_teacher': sorted_teacher,
        })


















































