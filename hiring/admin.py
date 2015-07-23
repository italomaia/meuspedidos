from django.contrib import admin
from .models import ExpectedSkill, SkillScore, CandidateProfile


admin.site.register(CandidateProfile)
admin.site.register(ExpectedSkill)
admin.site.register(SkillScore)


