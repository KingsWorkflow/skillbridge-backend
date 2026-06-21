from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.core.paginator import Paginator
from django.http import JsonResponse
from .forms import ExchangeProposalForm, ExchangeSessionForm, SessionRatingForm
from .models import ExchangeProposal, ExchangeSession, SkillCreditTransaction
from apps.skills.models import Skill, TeachableSkill, LearnableSkill
from apps.users.models import UserProfile


@login_required
def exchange_list(request):
    """Display user's exchanges (proposals and sessions)."""
    proposals = ExchangeProposal.objects.filter(
        Q(proposer=request.user) | Q(receiver=request.user)
    ).select_related('offer_skill', 'request_skill', 'receiver', 'proposer')

    sessions = ExchangeSession.objects.filter(
        Q(teacher=request.user) | Q(learner=request.user)
    ).select_related('skill_taught', 'teacher', 'learner')

    session_data = []
    for session in sessions:
        session_data.append({
            'skill': session.skill_taught.name,
            'with_user': session.teacher.username if session.teacher != request.user else session.learner.username,
            'time': session.scheduled_date,
            'icon': 'schedule',
        })

    return render(request, 'exchanges/exchange_list.html', {
        'proposals': proposals,
        'sessions': session_data,
    })


@login_required
def proposal_list(request):
    """Display both sent and received proposals."""
    sent_proposals = ExchangeProposal.objects.filter(
        proposer=request.user
    ).select_related('offer_skill', 'request_skill', 'receiver')

    received_proposals = ExchangeProposal.objects.filter(
        receiver=request.user
    ).select_related('offer_skill', 'request_skill', 'proposer')

    return render(request, 'exchanges/proposals.html', {
        'sent_proposals': sent_proposals,
        'received_proposals': received_proposals,
    })


@login_required
def partner_list(request):
    """
    Dynamic skill-exchange partner search.
    A partner is anyone whose teachable/learnable skills intersect with the current user's.
    Supports filters: category, min_reputation, availability.
    """
    user = request.user
    user_teachable_ids = set(user.teachable_skills.values_list('skill_id', flat=True))
    user_learnable_ids = set(user.learnable_skills.values_list('skill_id', flat=True))

    users = UserProfile.objects.exclude(pk=user.pk).prefetch_related(
        'teachable_skills__skill',
        'learnable_skills__skill',
    )

    partner_list_data = []
    for partner in users:
        partner_teachable_ids = set(partner.teachable_skills.values_list('skill_id', flat=True))
        partner_learnable_ids = set(partner.learnable_skills.values_list('skill_id', flat=True))

        i_teach_they_learn = user_teachable_ids & partner_learnable_ids
        i_learn_they_teach = user_learnable_ids & partner_teachable_ids

        if not i_teach_they_learn and not i_learn_they_teach:
            continue

        partner_list_data.append({
            'user': partner,
            'i_teach_they_learn_skills': list(Skill.objects.filter(id__in=i_teach_they_learn).values_list('name', flat=True)),
            'i_learn_they_teach_skills': list(Skill.objects.filter(id__in=i_learn_they_teach).values_list('name', flat=True)),
            'match_count': len(i_teach_they_learn) + len(i_learn_they_teach),
            'categories': list(Skill.objects.filter(id__in=list(i_teach_they_learn) + list(i_learn_they_teach)).values_list('category', flat=True).distinct()),
        })

    category = request.GET.get('category')
    min_reputation = request.GET.get('min_reputation')
    availability = request.GET.get('availability')

    if category:
        partner_list_data = [
            p for p in partner_list_data
            if any(cat.lower() == category.lower() for cat in p['categories'])
        ]

    if min_reputation:
        try:
            min_rep = float(min_reputation)
            partner_list_data = [
                p for p in partner_list_data
                if p['user'].reputation_score >= min_rep
            ]
        except ValueError:
            pass

    if availability == 'available':
        partner_list_data = [
            p for p in partner_list_data
            if p['user'].teachable_skills.filter(is_active=True, hourly_commitment__gt=0).exists()
        ]

    paginator = Paginator(partner_list_data, 9)
    page_number = request.GET.get('page') or 1
    page_obj = paginator.get_page(page_number)

    all_categories = sorted(
        {cat for p in partner_list_data for cat in p['categories']}
    )

    context = {
        'partners': page_obj,
        'categories': all_categories,
        'selected_category': category,
        'min_reputation': min_reputation or '',
        'availability': availability or '',
    }

    return render(request, 'exchanges/skill_exchange.html', context)


@login_required
def create_proposal(request, receiver_id):
    """Create an exchange proposal."""
    receiver = get_object_or_404(UserProfile, pk=receiver_id)
    if receiver == request.user:
        messages.error(request, 'You cannot send a proposal to yourself.')
        return redirect('exchanges:partner_list')

    if request.method == 'POST':
        form = ExchangeProposalForm(request.POST, user=request.user, receiver=receiver)
        if form.is_valid():
            proposal = form.save(commit=False)
            proposal.proposer = request.user
            proposal.receiver = receiver
            proposal.save()
            messages.success(request, 'Proposal sent successfully!')
            return redirect('exchanges:proposal_list')
    else:
        form = ExchangeProposalForm(user=request.user, receiver=receiver)

    selected_request_skill_name = None
    if request.method == 'POST' and form.is_valid():
        selected_request_skill = form.cleaned_data.get('request_skill')
        if selected_request_skill:
            selected_request_skill_name = selected_request_skill.skill.name
    elif 'request_skill' in request.GET:
        try:
            selected_request_skill_name = LearnableSkill.objects.get(pk=request.GET['request_skill'], user=receiver).skill.name
        except LearnableSkill.DoesNotExist:
            pass

    return render(request, 'exchanges/proposal_create.html', {
        'form': form,
        'receiver': receiver,
        'selected_request_skill_name': selected_request_skill_name,
    })


@login_required
def accept_proposal(request, proposal_id):
    proposal = get_object_or_404(ExchangeProposal, id=proposal_id, receiver=request.user)
    proposal.status = 'accepted'
    proposal.save()
    messages.success(request, 'Proposal accepted!')
    return redirect('exchanges:proposal_list')


@login_required
def reject_proposal(request, proposal_id):
    proposal = get_object_or_404(ExchangeProposal, id=proposal_id, receiver=request.user)
    proposal.status = 'rejected'
    proposal.save()
    messages.success(request, 'Proposal rejected!')
    return redirect('exchanges:proposal_list')


@login_required
def schedule_session(request, proposal_id):
    proposal = get_object_or_404(ExchangeProposal, id=proposal_id, status='accepted')

    if request.method == 'POST':
        form = ExchangeSessionForm(request.POST)
        if form.is_valid():
            session = form.save(commit=False)
            session.proposal = proposal
            session.teacher = proposal.offer_skill.user
            session.learner = proposal.request_skill.user
            session.skill_taught = proposal.offer_skill.skill
            session.save()
            messages.success(request, 'Session scheduled!')
            return redirect('exchanges:proposal_list')
    else:
        form = ExchangeSessionForm()

    return render(request, 'exchanges/schedule_session.html', {'form': form, 'proposal': proposal})


@login_required
def rate_session(request, session_id):
    session = get_object_or_404(ExchangeSession, id=session_id)

    if request.method == 'POST':
        form = SessionRatingForm(request.POST)
        if form.is_valid():
            rating = form.cleaned_data['rating']
            feedback = form.cleaned_data.get('feedback', '')

            if session.teacher == request.user:
                session.teacher_rating = rating
                session.teacher_feedback = feedback
            elif session.learner == request.user:
                session.learner_rating = rating
                session.learner_feedback = feedback

            session.save()
            messages.success(request, 'Rating submitted!')
            return redirect('exchanges:proposal_list')
    else:
        form = SessionRatingForm()

    return render(request, 'exchanges/rate_session.html', {'form': form, 'session': session})


@login_required
def complete_session(request, session_id):
    session = get_object_or_404(ExchangeSession, id=session_id)
    session.completed = True
    session.save()

    SkillCreditTransaction.objects.create(
        user=session.teacher,
        amount=10 * session.duration_hours,
        transaction_type='teach_earn',
        description=f"Taught {session.duration_hours} hours of {session.skill_taught.name}",
        related_session=session,
    )

    SkillCreditTransaction.objects.create(
        user=session.learner,
        amount=-10 * session.duration_hours,
        transaction_type='learn_spend',
        description=f"Learned {session.duration_hours} hours of {session.skill_taught.name}",
        related_session=session,
    )

    messages.success(request, 'Session completed and credits transferred!')
    return redirect('exchanges:proposal_list')