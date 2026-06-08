from django.contrib import admin, messages
from .models import ExchangeProposal, ExchangeSession, SkillCreditTransaction


class ExchangeSessionInline(admin.TabularInline):
    model = ExchangeSession
    extra = 0
    fields = ('scheduled_date', 'duration_hours', 'teacher', 'learner', 'completed')
    raw_id_fields = ('teacher', 'learner', 'skill_taught')
    readonly_fields = ('scheduled_date', 'duration_hours', 'teacher', 'learner', 'skill_taught')


@admin.register(ExchangeProposal)
class ExchangeProposalAdmin(admin.ModelAdmin):
    inlines = [ExchangeSessionInline]
    list_display = (
        'id',
        'proposer',
        'receiver',
        'offer_skill',
        'request_skill',
        'status',
        'proposed_hours',
        'created_at',
    )
    list_filter = ('status', 'created_at', 'offer_skill__skill__category', 'request_skill__skill__category')
    search_fields = (
        'proposer__username',
        'receiver__username',
        'offer_skill__skill__name',
        'request_skill__skill__name',
        'message',
    )
    readonly_fields = ('created_at', 'updated_at')
    date_hierarchy = 'created_at'
    list_select_related = ('proposer', 'receiver', 'offer_skill__skill', 'request_skill__skill')
    actions = ['mark_accepted', 'mark_completed', 'mark_rejected', 'mark_cancelled']

    def mark_accepted(self, request, queryset):
        updated = queryset.filter(status='pending').update(status='accepted')
        self.message_user(request, f'{updated} proposals accepted.', messages.SUCCESS)
    mark_accepted.short_description = 'Accept selected proposals'

    def mark_completed(self, request, queryset):
        updated = queryset.filter(status='accepted').update(status='completed')
        self.message_user(request, f'{updated} proposals marked completed.', messages.SUCCESS)
    mark_completed.short_description = 'Mark selected proposals as completed'

    def mark_rejected(self, request, queryset):
        updated = queryset.filter(status='pending').update(status='rejected')
        self.message_user(request, f'{updated} proposals rejected.', messages.SUCCESS)
    mark_rejected.short_description = 'Reject selected proposals'

    def mark_cancelled(self, request, queryset):
        updated = queryset.exclude(status__in=['completed', 'cancelled']).update(status='cancelled')
        self.message_user(request, f'{updated} proposals cancelled.', messages.SUCCESS)
    mark_cancelled.short_description = 'Cancel selected proposals'


@admin.register(ExchangeSession)
class ExchangeSessionAdmin(admin.ModelAdmin):
    list_display = ('id', 'proposal', 'scheduled_date', 'teacher', 'learner', 'skill_taught', 'completed', 'created_at')
    list_filter = ('completed', 'scheduled_date', 'created_at', 'proposal__status')
    search_fields = (
        'proposal__proposer__username',
        'proposal__receiver__username',
        'teacher__username',
        'learner__username',
        'skill_taught__name',
        'notes',
    )
    readonly_fields = ('created_at',)
    list_select_related = (
        'proposal__proposer',
        'proposal__receiver',
        'teacher',
        'learner',
        'skill_taught',
    )


@admin.register(SkillCreditTransaction)
class SkillCreditTransactionAdmin(admin.ModelAdmin):
    list_display = ('user', 'amount', 'transaction_type', 'related_session', 'created_at')
    list_filter = ('transaction_type', 'created_at')
    search_fields = ('user__username', 'user__email', 'description')
    readonly_fields = ('created_at',)
    list_select_related = ('user', 'related_session')
    date_hierarchy = 'created_at'
