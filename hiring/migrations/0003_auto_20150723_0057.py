# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hiring', '0002_auto_20150722_0246'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='candidateapplication',
            options={'verbose_name': 'inscri\xe7\xe3o do candidato', 'verbose_name_plural': 'inscri\xe7\xf5es dos candidatos'},
        ),
        migrations.AlterModelOptions(
            name='candidateprofile',
            options={'verbose_name': 'perfil do candidato', 'verbose_name_plural': 'perfis dos candidatos'},
        ),
        migrations.AlterModelOptions(
            name='expectedskill',
            options={'verbose_name': 'habilidade esperada', 'verbose_name_plural': 'habilidades esperadas'},
        ),
        migrations.AlterModelOptions(
            name='skillscore',
            options={'verbose_name': 'pontua\xe7\xe3o da habilidade', 'verbose_name_plural': 'pontua\xe7\xf5es das habilidades'},
        ),
        migrations.AlterField(
            model_name='candidateprofile',
            name='expected_skills',
            field=models.ManyToManyField(related_name='profiles', to='hiring.ExpectedSkill', blank=True),
        ),
        migrations.AlterField(
            model_name='expectedskill',
            name='description',
            field=models.CharField(unique=True, max_length=150, verbose_name='Habilidade desejada'),
        ),
    ]
