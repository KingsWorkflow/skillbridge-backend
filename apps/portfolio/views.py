from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import ProjectForm, PortfolioCertificationForm


@login_required
def portfolio_view(request):
    if request.method == 'POST':
        if 'save_project' in request.POST:
            form = ProjectForm(request.POST, request.FILES)
            if form.is_valid():
                project = form.save(commit=False)
                project.user = request.user
                project.save()
                messages.success(request, 'Project added to portfolio!')
                return redirect('portfolio:portfolio')
        elif 'save_cert' in request.POST:
            cert_form = PortfolioCertificationForm(request.POST, request.FILES)
            if cert_form.is_valid():
                cert = cert_form.save(commit=False)
                cert.user = request.user
                cert.save()
                messages.success(request, 'Certification added to portfolio!')
                return redirect('portfolio:portfolio')
    else:
        form = ProjectForm()
        cert_form = PortfolioCertificationForm()
    
    # Prepare context for template compatibility
    context = {
        'user': request.user,
        'profile': request.user,  # Template uses profile.avatar, profile.title, etc.
        'projects': request.user.projects.all(),
        'certifications': request.user.certifications.all(),
        'achievements': [],  # Add achievements logic if needed
        'project_form': form,
        'cert_form': cert_form,
    }
    return render(request, 'portfolio/portfolio.html', context)