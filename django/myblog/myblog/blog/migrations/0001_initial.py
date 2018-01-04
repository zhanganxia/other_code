# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('create_time', models.DateTimeField(verbose_name='创建时间', auto_now_add=True)),
                ('update_time', models.DateTimeField(verbose_name='修改时间', auto_now=True)),
                ('is_delete', models.BooleanField(verbose_name='是否删除', default=False)),
                ('title', models.CharField(verbose_name="'标题'", max_length=70)),
                ('body', models.TextField(verbose_name='正文')),
                ('status', models.CharField(verbose_name='文章状态', max_length=1, choices=[('d', 'part'), ('p', 'Published')])),
                ('abstract', models.CharField(verbose_name='摘要', max_length=54, blank=True, null=True, help_text='可选项，若为空格则摘取正文前54个字符')),
                ('views', models.PositiveIntegerField(verbose_name='浏览器', default=0)),
                ('likes', models.PositiveIntegerField(verbose_name='点赞数', default=0)),
                ('topped', models.BooleanField(verbose_name='置顶', default=False)),
            ],
            options={
                'verbose_name': '文章',
                'verbose_name_plural': '文章',
                'db_table': 'blog_article',
            },
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('create_time', models.DateTimeField(verbose_name='创建时间', auto_now_add=True)),
                ('update_time', models.DateTimeField(verbose_name='修改时间', auto_now=True)),
                ('is_delete', models.BooleanField(verbose_name='是否删除', default=False)),
                ('name', models.CharField(verbose_name='类名', max_length=20)),
            ],
            options={
                'verbose_name': '文章分类',
                'verbose_name_plural': '文章分类',
                'db_table': 'blog_category',
            },
        ),
        migrations.AddField(
            model_name='article',
            name='category',
            field=models.ForeignKey(verbose_name='分类', null=True, on_delete=django.db.models.deletion.SET_NULL, to='blog.Category'),
        ),
    ]
