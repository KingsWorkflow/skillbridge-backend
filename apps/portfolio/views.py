from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def portfolio(request):
    return render(request, 'portfolio/portfolio.html', {
        'projects': [],
        'certifications': [],
        'achievements': [],
    })

@login_required
def project_list(request):
    return render(request, 'portfolio/project_list.html', {
        'projects': [],
    })

@login_required
def project_create(request):
    return render(request, 'portfolio/project_create.html', {})

@login_required
def certification_list(request):
    return render(request, 'portfolio/certification_list.html', {
        'certifications': [],
    })

@login_required
def certification_create(request):
    return render(request, 'portfolio/certification_create.html', {})