import django.dispatch


candidate_application_received = django.dispatch.Signal(
    providing_args=["candidate_application"])
