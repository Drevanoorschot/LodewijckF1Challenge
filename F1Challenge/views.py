from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.cache import cache
from django.shortcuts import redirect
from django.urls import reverse


def landing_page(request):
    return redirect(reverse('leaderboard'))


@login_required
def clear_cache(request):
    cache.clear()
    messages.info(request, 'Cache Cleared!')
    return redirect(reverse('csv_upload'))
