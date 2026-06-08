from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from .forms import ExchangeProposalForm, ExchangeSessionForm, SessionRatingForm
from .models import ExchangeProposal, ExchangeSession, SkillCreditTransaction
from apps.skills.models import TeachableSkill, LearnableSkill


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
def skill_exchange(request):
    """Display skill exchange marketplace with user's skills and available listings."""
    tab = request.GET.get('tab', 'offer')
    
    # Get user's teachable and learnable skills
    user_teachable = TeachableSkill.objects.filter(
        user=request.user, is_active=True
    ).select_related('skill')
    user_learnable = LearnableSkill.objects.filter(
        user=request.user
    ).select_related('skill')
    
    # Get all active listings (teachable skills from other users)
    listings = TeachableSkill.objects.filter(
        is_active=True
    ).select_related('user', 'skill').exclude(user=request.user)
    
    # Convert to listing format for template
    listing_data = []
    for item in listings[:6]:
        listing_data.append({
            'user': item.user,
            'title': f'Teaching {item.skill.name}',
            'description': f'Proficiency: {item.get_proficiency_level_display()}',
            'category': item.skill.category,
            'category_color': 'secondary',
            'hours': item.hourly_commitment,
            'rating': item.user.reputation_score,
            'exchanges': item.user.total_hours_taught // 5,  # Approximate
            'delivery_format': 'Remote',
            'delivery_icon': 'handshake',
        })
    
    return render(request, 'exchanges/skill_exchange.html', {
        'listings': listing_data,
        'user_teachable': user_teachable,
        'user_learnable': user_learnable,
        'active_tab': tab,
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
def create_proposal(request, receiver_id):
    """Create an exchange proposal."""
    receiver = get_object_or_404(User, id=receiver_id)
    if receiver == request.user:
        messages.error(request, 'You cannot send a proposal to yourself.')
        return redirect('exchanges:skill_exchange')
    
    if request.method == 'POST':
        form = ExchangeProposalForm(request.POST)
        if form.is_valid():
            proposal = form.save(commit=False)
            proposal.proposer = request.user
            proposal.receiver = receiver
            proposal.save()
            messages.success(request, 'Proposal sent successfully!')
            return redirect('exchanges:proposal_list')
    else:
        form = ExchangeProposalForm()
        form.fields['offer_skill'].queryset = TeachableSkill.objects.filter(user=request.user, is_active=True)
        form.fields['request_skill'].queryset = LearnableSkill.objects.filter(user=receiver)
    
    return render(request, 'exchanges/proposal_form.html', {
        'form': form,
        'receiver': receiver,
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
    
    # Transfer credits: teacher earns, learner spends
    SkillCreditTransaction.objects.create(
        user=session.teacher,
        amount=10 * session.duration_hours,
        transaction_type='teach_earn',
        description=f'Taught {session.duration_hours} hours of {session.skill_taught.name}',
        related_session=session
    )
    
    SkillCreditTransaction.objects.create(
        user=session.learner,
        amount=-10 * session.duration_hours,
        transaction_type='learn_spend',
        description=f'Learned {session.duration_hours} hours of {session.skill_taught.name}',
        related_session=session
    )
    
    messages.success(request, 'Session completed and credits transferred!')
    return redirect('exchanges:proposal_list')