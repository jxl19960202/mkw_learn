from django.urls import path,include,re_path

from .views import OrgView,AddUserAskView,OrgHomeView,OrgCourseView,OrgDescView,OrgTeacherView,AddFavView
from .views import TeacherListView,TeacherDetailView


app_name = 'organization'
urlpatterns = [
    #机构列表页
    re_path(r'^list/',OrgView.as_view(),name="list"),

    #用户咨询
    path('add_ask/', AddUserAskView.as_view(), name="add_ask"),

    #机构首页
    re_path('home/(?P<org_id>\d+)/', OrgHomeView.as_view(), name="org_home"),

    #机构课程
    re_path('course/(?P<org_id>\d+)/', OrgCourseView.as_view(), name="org_course"),

    #机构详情
    re_path('desc/(?P<org_id>\d+)/', OrgDescView.as_view(), name="org_desc"),

    #机构讲授
    re_path('teacher/(?P<org_id>\d+)/', OrgTeacherView.as_view(), name="org_teacher"),

    #是否收藏
    path('add_fav/', AddFavView.as_view(), name="add_fav"),

    #讲师列表
    re_path('teacher/list/', TeacherListView.as_view(), name="teacher_list"),

    #讲师详情页
    re_path('teacher/detail/(?P<teacher_id>\d+)/', TeacherDetailView.as_view(), name="teacher_detail"),

]