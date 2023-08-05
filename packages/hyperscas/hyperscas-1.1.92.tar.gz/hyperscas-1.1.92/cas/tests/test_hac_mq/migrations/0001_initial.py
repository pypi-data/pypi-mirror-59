# Generated by Django 2.2.2 on 2019-07-03 02:22

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('username', models.CharField(max_length=30, unique=True, verbose_name='Name of User')),
                ('email', models.EmailField(max_length=100, unique=True, verbose_name='email address')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('dateJoined', models.DateTimeField(auto_now_add=True, verbose_name='date joined')),
                ('role', models.CharField(max_length=255, verbose_name='用户角色')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='UserGroup',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('group_id', models.IntegerField(default=0)),
                ('name', models.CharField(max_length=50, unique=True)),
                ('status', models.CharField(choices=[('ACTIVE', '启用'), ('DELETED', '删除'), ('PAUSED', '停用')], default='ACTIVE', max_length=20)),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('creator_id', models.IntegerField(default=1, verbose_name='创建者')),
            ],
        ),
    ]
