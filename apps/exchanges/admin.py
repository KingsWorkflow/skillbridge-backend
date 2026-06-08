from django.contrib import admin
from .models import ExchangeProposal, ExchangeSession, SkillCreditTransaction


@admin.register(ExchangeProposal)
class ExchangeProposalAdmin(admin.ModelAdmin):
    list_display = ('proposer', 'receiver', 'status', 'proposed_hours', 'created_at')
    list_filter = ('status',)
    search_fields = ('proposer__username', 'receiver__username')


@admin.register(ExchangeSession)
class ExchangeSessionAdmin(admin.ModelAdmin):
    list_display = ('proposal', 'scheduled_date', 'teacher', 'learner', 'completed')
    list_filter = ('completed',)


@admin.register(SkillCreditTransaction)
class SkillCreditTransactionAdmin(admin.ModelAdmin):
    list_display = ('user', 'amount', 'transaction_type', 'created_at')
    list_filter = ('transaction_type',)
    search_fields = ('user__username',)