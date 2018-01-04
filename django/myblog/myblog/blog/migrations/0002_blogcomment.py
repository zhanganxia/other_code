# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='BlogComment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('create_time', models.DateTimeField(verbose_name='创建时间', auto_now_add=True)),
                ('update_time', models.DateTimeField(verbose_name='修改时间', auto_now=True)),
                ('is_delete', models.BooleanField(verbose_name='是否删除', default=False)),
                ('user_name', models.CharField(verbose_name='评论者的名字', max_length=100)),
                ('user_email', models.EmailField(verbose_name='评论者邮箱', max_length=255)),
                ('body', models.TextField(verbose_name='评论内容')),
                ('article', models.ForeignKey(verbose_name='评论所属文章', to='blog.Article')),
            ],
            options={
                'verbose_name': '文章评论',
                'verbose_name_plural': '文章评论',
                'db_table': 'blog_comment',
            },
        ),
    ]
