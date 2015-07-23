# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CandidateApplication',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100, verbose_name='Nome')),
                ('email', models.EmailField(max_length=100, verbose_name='E-mail')),
            ],
        ),
        migrations.CreateModel(
            name='ExpectedSkill',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('description', models.CharField(max_length=150, verbose_name='Habilidade desejada')),
            ],
        ),
        migrations.CreateModel(
            name='SkillScore',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('skill_level', models.PositiveSmallIntegerField(verbose_name='Profici\xeancia', validators=[django.core.validators.MaxValueValidator(10)])),
                ('candidate_application', models.ForeignKey(to='hiring.CandidateApplication')),
                ('expected_skill', models.ForeignKey(to='hiring.ExpectedSkill')),
            ],
        ),
        migrations.AddField(
            model_name='candidateapplication',
            name='expected_skills',
            field=models.ManyToManyField(related_name='candidates', through='hiring.SkillScore', to='hiring.ExpectedSkill'),
        ),
    ]
