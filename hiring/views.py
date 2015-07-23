# coding:utf-8
from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from django.contrib import messages
from .models import ExpectedSkill, CandidateApplication
from .forms import CandidateApplicationForm, SkillForm
from .signals import candidate_application_received


def submit_application(request):
    form = CandidateApplicationForm(request.POST or None)
    forms = [
        SkillForm(
            request.POST or None,
            prefix="%d" % skill.id,
            initial={'expected_skill': skill}
        ) for skill in ExpectedSkill.objects.all()]

    if form.is_valid() and all(map(lambda f: f.is_valid(), forms)):
        candidate_application = form.save()

        for form in forms:
            skill_score = form.save(commit=False)
            skill_score.candidate_application = candidate_application
            skill_score.save()

        messages.success(request, "Seus dados foram recebidos."
                                  " Por favor, aguarde a mensagem"
                                  " de confirmação por e-mail.")

        candidate_application.send_received_signal()
        return redirect(reverse("hiring:apply"))

    context = {'form': form, 'forms': forms}
    return render(request, "hiring/apply.html", context=context)
