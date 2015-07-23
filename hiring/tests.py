# coding:utf-8

from django.core import mail
from django.contrib import messages
from django.test import TestCase
from django.core.urlresolvers import reverse
from random import choice


class TestSubmissionForm(TestCase):
    def create_expected_skill(self, description):
        from hiring.models import ExpectedSkill

        skill = ExpectedSkill(description=description)
        skill.save()
        return skill

    def test_used_template(self):
        url = reverse("hiring:apply")
        resp = self.client.get(url)
        self.assertTemplateUsed(resp, "hiring/apply.html")

    def test_form_is_rendered(self):
        url = reverse("hiring:apply")
        resp = self.client.get(url)
        self.assertContains(resp, "<form")

    def test_form_has_form(self):
        url = reverse("hiring:apply")
        resp = self.client.get(url)
        context = resp.context
        self.assertIsNotNone(context["form"])

    def test_form_has_name_field(self):
        url = reverse("hiring:apply")
        resp = self.client.get(url)
        context = resp.context
        form = context["form"]

        self.assertIsNotNone(form)
        self.assertIsNotNone(form.fields.get('name'))

    def test_form_has_email_field(self):
        url = reverse("hiring:apply")
        resp = self.client.get(url)
        context = resp.context
        form = context["form"]

        self.assertIsNotNone(form)
        self.assertIsNotNone(form.fields.get('email'))

    def test_candidate_skill_forms_are_rendered(self):
        skill_a = self.create_expected_skill("HTML")
        skill_b = self.create_expected_skill("Javascript")

        url = reverse("hiring:apply")
        resp = self.client.get(url)

        self.assertContains(resp, "skill_level")
        self.assertContains(resp, skill_a.description)
        self.assertContains(resp, skill_b.description)

    def test_if_skills_form_message_is_showed_if_expected_skill_is_registered(self):
        self.create_expected_skill("HTML")
        url = reverse("hiring:apply")
        resp = self.client.get(url)
        self.assertContains(resp, "Nos informe qual")

    def test_if_skills_form_message_is_hidden_if_no_expected_skill_is_registered(self):
        url = reverse("hiring:apply")
        resp = self.client.get(url)
        self.assertNotContains(resp, "Nos informe qual")


class TestApplicationSubmission(TestCase):
    def create_skill(self, description):
        from hiring.models import ExpectedSkill

        skill = ExpectedSkill(description=description)
        skill.save()
        return skill

    def create_skills(self):
        return [
            self.create_skill("HTML"),
            self.create_skill("Javascript")
        ]

    def create_candidate_data(self):
        return {"name": "john doe", "email": "john@doe.com"}

    def create_profile(self, label, skills):
        from hiring.models import CandidateProfile

        profile = CandidateProfile(label=label, min_score=7, max_score=10)
        profile.save()

        for skill in skills:
            profile.expected_skills.add(skill)

    def test_sets_message_on_success(self):
        url = reverse("hiring:apply")
        data = self.create_candidate_data()
        resp = self.client.post(url, data=data, follow=True)
        self.assertContains(resp, u"Seus dados foram recebidos")

    def test_post_submit_without_profile_nor_skills(self):
        from hiring.models import CandidateApplication

        url = reverse("hiring:apply")
        data = self.create_candidate_data()
        resp = self.client.post(url, data=data)
        queryset = CandidateApplication.objects.filter(email=data["email"])

        # redirect means success
        self.assertRedirects(resp, url)

        # e-mail was sent
        self.assertEqual(len(mail.outbox), 1)

        # candidate application was created
        self.assertIsNotNone(queryset.first())

    def test_post_submit_with_skills(self):
        from hiring.models import *

        url = reverse("hiring:apply")
        skills = self.create_skills()
        data = self.create_candidate_data()

        for skill in skills:
            data["%d-skill_level" % skill.id] = 5
            data["%d-expected_skill" % skill.id] = skill.id

        self.client.post(url, data=data)
        application = CandidateApplication.objects.get(email=data["email"])
        queryset = SkillScore.objects.filter(candidate_application=application)
        self.assertEqual(queryset.count(), 2)
        self.assertEqual(
            queryset.filter(expected_skill__in=skills).count(), 2)

        assert all(map(
            lambda v: v == 5,
            queryset.filter(expected_skill__in=skills)
            .values_list('skill_level', flat=True)
        ))

    def test_post_submit_with_profile_and_skills_sends_one_email(self):
        url = reverse("hiring:apply")
        skills = self.create_skills()
        profile = self.create_profile("programador front-end", skills)
        data = self.create_candidate_data()

        for skill in skills:
            data["%d-skill_level" % skill.id] = choice([7, 10])
            data["%d-expected_skill" % skill.id] = skill.id

        self.client.post(url, data=data)

        # e-mail was sent
        self.assertEqual(len(mail.outbox), 1)

    def test_post_submit_when_candidate_fits_multiple_profiles_sends_multiple_emails(self):
        url = reverse("hiring:apply")
        skills = self.create_skills()
        self.create_profile("designer", [skills[0]])
        self.create_profile("programador front-end", [skills[1]])
        data = self.create_candidate_data()

        for skill in skills:
            data["%d-skill_level" % skill.id] = choice([7, 10])
            data["%d-expected_skill" % skill.id] = skill.id

        self.client.post(url, data=data)

        # e-mail was sent
        self.assertEqual(len(mail.outbox), 2)
