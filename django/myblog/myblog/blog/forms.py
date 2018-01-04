from django import forms
from blog.models import Article,BlogComment

class BlogCommentForm(forms.ModelForm):
    '''forms用户评论模型类'''
    class Meta:
        model = BlogComment
        fields = ['user_name','user_email','body']

        widgets = {
            'user_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '请输入昵称',
                'aria-describedby': 'sizing-addon1',
            }),
            'user_email': froms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '请输入邮箱',
                'aria-describedby': 'sizing-addon1',
            }),
            'body': forms.Textarea(attrs={'placeholder':'让我来说两句'})
        }