from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def exchange_list(request):
    return render(request, 'exchanges/exchange_list.html', {
        'proposals': [],
        'sessions': [],
    })

def skill_exchange(request):
    return render(request, 'exchanges/skill_exchange.html', {
        'listings': [],
    })

@login_required
def proposal_create(request):
    return render(request, 'exchanges/proposal_create.html', {})

@login_required
def session_schedule(request):
    return render(request, 'exchanges/session_schedule.html', {})