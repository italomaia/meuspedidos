# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('hiring', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CandidateProfile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('label', models.CharField(max_length=50)),
                ('min_score', models.PositiveSmallIntegerField()),
                ('max_score', models.PositiveSmallIntegerField(validators=[django.core.validators.MaxValueValidator(10)])),
                ('expected_skills', models.ManyToManyField(related_name='profiles', to='hiring.ExpectedSkill')),
            ],
        ),
        migrations.AlterField(
            model_name='candidateapplication',
            name='expected_skills',
            field=models.ManyToManyField(related_name='candidates', through='hiring.SkillScore', to='hiring.ExpectedSkill', blank=True),
        ),
        migrations.AlterField(
            model_name='skillscore',
            name='skill_level',
            field=models.PositiveSmallIntegerField(default=0, verbose_name='Profici\xeancia', validators=[django.core.validators.MaxValueValidator(10)]),
        ),
    ]
