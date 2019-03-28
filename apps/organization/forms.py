import re

from django import forms

from operation.models import UserAsk

#常规的用于验证的form
# class UserAskForm(forms.Form):
#     name = forms.CharField(required=True,min_length=3)
#     mobile = forms.CharField(required=True,max_length=11,min_length=11)
#     course_name = forms.CharField(required=True,max_length=11)



class UserAskForm(forms.ModelForm):
    # 能通过继承model的form,既有form的验证功能,又具有对数据库的保存操作功能.
    class Meta:
        model = UserAsk  #model:指定model
        fields = ['name', 'mobile', 'course_name'] #要表单验证的字段

