from django.contrib import admin, messages
from django.db.models import Count, Sum, Q, F
from django.shortcuts import render, redirect
from django.utils import timezone
from datetime import timedelta, datetime
from apps.users.models import UserProfile
from apps.skills.models import Skill, TeachableSkill
from apps.exchanges.models import ExchangeProposal, ExchangeSession
from apps.verification.models import Certificate
from collections import defaultdict
import csv


def analytics_dashboard(request):
    if not request.user.is_staff:
        messages.error(request, 'Access denied.')
        return redirect('admin:index')

    today = timezone.now().date()
    seven_days_ago = today - timedelta(days=7)
    thirty_days_ago = today - timedelta(days=30)

    total_users = UserProfile.objects.filter(is_staff=False).count()
    active_exchanges = ExchangeProposal.objects.filter(status='accepted').count()
    pending_proposals = ExchangeProposal.objects.filter(status='pending').count()
    pending_certificates = Certificate.objects.filter(status='pending').count()

    top_skills = TeachableSkill.objects.values('skill__name').annotate(
        count=Count('id')
    ).order_by('-count')[:5]

    weekly_signups = []
    weekly_completions = []
    for i in range(6, -1, -1):
        day = today - timedelta(days=i)
        day_start = datetime.combine(day, datetime.min.time())
        day_end = datetime.combine(day, datetime.max.time())
        signups = UserProfile.objects.filter(
            date_joined__range=(day_start, day_end), is_staff=False
        ).count()
        completions = ExchangeSession.objects.filter(
            completed=True,
            created_at__range=(day_start, day_end)
        ).count()
        weekly_signups.append(signups)
        weekly_completions.append(completions)

    labels_7d = [(today - timedelta(days=i)).strftime('%a') for i in range(6, -1, -1)]

    context = {
        'title': 'Analytics Dashboard',
        'total_users': total_users,
        'active_exchanges': active_exchanges,
        'pending_proposals': pending_proposals,
        'pending_certificates': pending_certificates,
        'top_skills': top_skills,
        'weekly_signups': weekly_signups,
        'weekly_completions': weekly_completions,
        'labels_7d': labels_7d,
        'has_permission': True,
    }
    return render(request, 'admin_custom/analytics_dashboard.html', context)


def bulk_verify_view(request):
    if not request.user.is_staff:
        messages.error(request, 'Access denied.')
        return redirect('admin:index')

    if request.method == 'POST' and request.FILES.get('csv_file'):
        csv_file = request.FILES['csv_file']
        if not csv_file.name.endswith('.csv'):
            messages.error(request, 'Please upload a valid CSV file.')
            return redirect('admin:bulk_verify')

        decoded = csv_file.read().decode('utf-8').splitlines()
        reader = csv.DictReader(decoded)
        approved = 0
        failed = 0
        errors = []

        for row in reader:
            email = row.get('email', '').strip().lower()
            skill_name = row.get('skill_name', '').strip()
            if not email or not skill_name:
                failed += 1
                errors.append(f"Row missing email or skill_name: {row}")
                continue
            try:
                user = UserProfile.objects.get(email=email)
                skill = Skill.objects.get(name__iexact=skill_name)
                cert, created = Certificate.objects.get_or_create(
                    user=user,
                    skill=skill,
                    defaults={
                        'issuing_organization': 'SkillBridge Bulk',
                        'issue_date': timezone.now().date(),
                        'status': 'approved',
                    }
                )
                if created:
                    approved += 1
                else:
                    failed += 1
                    errors.append(f"Certificate already exists: {email} - {skill_name}")
            except UserProfile.DoesNotExist:
                failed += 1
                errors.append(f"User not found: {email}")
            except Skill.DoesNotExist:
                failed += 1
                errors.append(f"Skill not found: {skill_name}")

        messages.success(request, f'Bulk verification complete. Approved: {approved}, Failed: {failed}')
        if errors:
            request.session['bulk_verify_errors'] = errors[:20]

    errors = request.session.pop('bulk_verify_errors', None)
    context = {
        'title': 'Bulk Verify Certificates',
        'has_permission': True,
    }
    if errors:
        context['errors'] = errors
    return render(request, 'admin_custom/bulk_verify.html', context)
