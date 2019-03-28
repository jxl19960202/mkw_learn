from datetime import datetime

from django.db import models

from organization.models import CourseOrg,Teacher
from DjangoUeditor.models import UEditorField

class Course(models.Model):
    #课程数据表
    DEGREE_CHOICES = (
        ("cj", "初级"),
        ("zj", "中级"),
        ("gj", "高级")
    )
    name = models.CharField(verbose_name="课程名",max_length=50)
    teacher = models.ForeignKey(Teacher, verbose_name='讲师', null=True, blank=True, on_delete=models.CASCADE)
    desc = models.CharField(verbose_name="课程描述",max_length=300)
    # detail = models.TextField(verbose_name="课程详情")
    detail = UEditorField(verbose_name=u'课程详情', width=600, height=300, imagePath="courses/ueditor/",
                          filePath="courses/ueditor/", default='')

    degree = models.CharField(verbose_name='难度',choices=DEGREE_CHOICES, max_length=2)
    learn_times = models.IntegerField(verbose_name="学习时长(分钟数)",default=0)
    students = models.IntegerField(verbose_name="学习人数",default=0)
    fav_nums = models.IntegerField(verbose_name="收藏人数",default=0)
    image = models.ImageField(verbose_name="封面图",upload_to="courses/%Y/%m",max_length=100)
    click_nums = models.IntegerField("点击数",default=0)
    add_time = models.DateTimeField(verbose_name="添加时间",default=datetime.now,)
    course_org = models.ForeignKey(CourseOrg, on_delete=models.CASCADE, verbose_name="所属机构", null=True, blank=True)
    category = models.CharField(verbose_name="课程类别",max_length=20, default="")
    tag = models.CharField(verbose_name='课程标签', default='', max_length=10)
    youneed_know = models.CharField(verbose_name='课程须知', max_length=300, default='')
    teacher_tell = models.CharField(verbose_name='老师告诉你', max_length=300, default='')
    is_banner = models.BooleanField('是否轮播', default=False)

    class Meta:
        verbose_name = "课程"
        verbose_name_plural = verbose_name

    def get_zj_nums(self):
        #获取课程的章节数
        return self.lesson_set.all().count()

    def get_learn_users(self):
        #获取这门课程的学习用户
        return self.usercourse_set.all()[:5]

    def get_course_lesson(self):
        #获取课程的章节
        return self.lesson_set.all()

    def __str__(self):
        return self.name


class Lesson(models.Model):
    #课程章节
    course = models.ForeignKey(Course,verbose_name='课程',on_delete=models.CASCADE)
    name = models.CharField("章节名",max_length=100)
    add_time = models.DateTimeField("添加时间",default=datetime.now)

    class Meta:
        verbose_name = "章节"
        verbose_name_plural = verbose_name

    def get_lesson_vedio(self):
        # 获取章节所有视频
        return self.video_set.all()

    def __str__(self):
        return '《{0}》课程的章节 >> {1}'.format(self.course, self.name)


class Video(models.Model):
    #课程视频
    lesson = models.ForeignKey(Lesson, verbose_name="章节",on_delete=models.CASCADE)
    name = models.CharField("视频名",max_length=100)
    add_time = models.DateTimeField("添加时间", default=datetime.now)
    url = models.CharField('访问地址', default='', max_length=200)
    learn_times = models.IntegerField("学习时长(分钟数)", default=0)

    class Meta:
        verbose_name = "视频"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class CourseResource(models.Model):
    #课程附件资源下载
    course = models.ForeignKey(Course, verbose_name="课程",on_delete=models.CASCADE)
    name = models.CharField(verbose_name="名称",max_length=100)
    download = models.FileField(verbose_name="资源文件",upload_to="course/resource/%Y/%m",max_length=100)
    add_time = models.DateTimeField(verbose_name="添加时间", default=datetime.now)

    class Meta:
        verbose_name = "课程资源"
        verbose_name_plural = verbose_name

