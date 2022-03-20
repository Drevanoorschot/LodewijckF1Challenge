from django.shortcuts import redirect
from django.urls import reverse


def landing_page(request):
    return redirect(reverse('leaderboard'))
