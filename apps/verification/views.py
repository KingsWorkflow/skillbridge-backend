from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def certificate_upload(request):
    return render(request, 'verification/certificate_upload.html', {})

@login_required
def certificate_list(request):
    return render(request, 'verification/certificate_list.html', {
        'certificates': [],
    })

@login_required
def exam_start(request):
    return render(request, 'verification/exam_start.html', {})

@login_required
def exam_submit(request):
    return render(request, 'verification/exam_submit.html', {})

@login_required
def community_verify(request, user_id, skill_id):
    return render(request, 'verification/community_verify.html', {
        'user_id': user_id,
        'skill_id': skill_id,
    })

def verification_status(request, user_id):
    return render(request, 'verification/verification_status.html', {
        'user_id': user_id,
        'verifications': [],
    })