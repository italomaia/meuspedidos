# coding:utf-8
from django.db import models
from django.core.validators import MaxValueValidator
from .signals import candidate_application_received
from django.dispatch import receiver
from django.template.loader import get_template
from django.conf import settings


class CandidateProfile(models.Model):
    label = models.CharField(max_length=50, blank=False)
    min_score = models.PositiveSmallIntegerField()
    max_score = models.PositiveSmallIntegerField(
        validators=[MaxValueValidator(10)])
    expected_skills = models.ManyToManyField(
        'ExpectedSkill', related_name='profiles', blank=True)

    class Meta:
        verbose_name = u'perfil do candidato'
        verbose_name_plural = u'perfis dos candidatos'

    def __unicode__(self):
        return self.label

    def fits_profile(self, candidate_application):
        # fetch scores for each of the expected skills
        scores = SkillScore.objects.filter(
            candidate_application=candidate_application)
        expected_skills = self.expected_skills.all()
        scores = scores.filter(expected_skill__in=expected_skills)

        # then check that all of them are withing expected score
        min_score, max_score = self.min_score, self.max_score
        return all(map(
            lambda s: min_score <= s.skill_level <= max_score,
            list(scores)
        ))


class CandidateApplication(models.Model):
    name = models.CharField(u"Nome", max_length=100, blank=False)
    email = models.EmailField(u"E-mail", max_length=100, blank=False)
    expected_skills = models.ManyToManyField(
        'ExpectedSkill', through='SkillScore', related_name='candidates', blank=True)

    class Meta:
        verbose_name = u'inscrição do candidato'
        verbose_name_plural = u'inscrições dos candidatos'

    def __unicode__(self):
        return u"%s - %s" % (self.email, self.name)

    def get_profile(self):
        queryset = SkillScore.objects.filter(candidate_application=self)

    def send_received_signal(self):
        candidate_application_received.send(
            sender=self.__class__, candidate_application=self)


class SkillScore(models.Model):
    skill_level = models.PositiveSmallIntegerField(
        u"Proficiência", default=0, validators=[MaxValueValidator(10)])
    expected_skill = models.ForeignKey('ExpectedSkill')
    candidate_application = models.ForeignKey('CandidateApplication')

    class Meta:
        verbose_name = u'pontuação da habilidade'
        verbose_name_plural = u'pontuações das habilidades'

    def __unicode__(self):
        return u"%02d - %s - %s" % (
            self.skill_level,
            self.expected_skill,
            self.candidate_application.name)


class ExpectedSkill(models.Model):
    description = models.CharField(
        u"Habilidade desejada", max_length=150, unique=True)

    class Meta:
        verbose_name = u'habilidade esperada'
        verbose_name_plural = u'habilidades esperadas'

    def __unicode__(self):
        return self.description


@receiver(candidate_application_received, sender=CandidateApplication)
def notify_candidate(sender, candidate_application, *args, **kwargs):
    from django.core.mail import send_mail

    ca = candidate_application
    profiles = filter(
        lambda m: m[0],
        [
            (profile.fits_profile(ca), profile.label)
            for profile in CandidateProfile.objects.all()
        ])

    subject = u'Obrigado por se candidatar'
    template = get_template("hiring/confirmation_email.html")

    for profile in profiles:
        context = {'job': profile[1]}
        content = template.render(context=context)
        send_mail(
            subject, content,
            settings.DEFAULT_FROM_EMAIL,
            [ca.email], fail_silently=True)

    if not profiles:
        context = {'job': "programador"}
        content = template.render(context=context)
        send_mail(
            subject, content,
            settings.DEFAULT_FROM_EMAIL,
            [ca.email], fail_silently=True)
