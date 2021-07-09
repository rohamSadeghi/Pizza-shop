from django.contrib import admin
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

from apps.pizzas.models import Pizza, PizzaRate, PizzaComment


class ApprovedListFilter(admin.SimpleListFilter):
    # Human-readable title which will be displayed in the
    # right admin sidebar just above the filter options.
    title = _('approved')

    # Parameter for the filter that will be used in the URL query.
    parameter_name = 'approved'

    def lookups(self, request, model_admin):
        """
        Returns a list of tuples. The first element in each
        tuple is the coded value for the option that will
        appear in the URL query. The second element is the
        human-readable name for the option that will appear
        in the right sidebar.
        """
        return (
            ('approved', _('approved')),
            ('not-approved', _('not approved')),
        )

    def queryset(self, request, queryset):
        """
        Returns the filtered queryset based on the value
        provided in the query string and retrievable via
        `self.value()`.
        """
        # to decide how to filter the queryset.
        if self.value() == 'approved':
            queryset = queryset.exclude(approved_user__isnull=True)
            return queryset
        if self.value() == 'not-approved':
            queryset = queryset.filter(approved_user__isnull=True)
            return queryset


@admin.register(Pizza)
class PizzaAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "price", "price_discount", "is_enable")
    search_fields = ('name', )
    list_filter = ('is_enable', )


@admin.register(PizzaRate)
class PizzaRateAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "pizza", "rate", "created_time")
    list_select_related = ('user', 'pizza')
    search_fields = ('user__username', 'pizza__name')
    autocomplete_fields = ('user', 'pizza')


@admin.register(PizzaComment)
class PizzaCommentAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "pizza", "is_approved", "created_time")
    list_select_related = ['user', 'pizza']
    search_fields = ('user__username', 'pizza__name')
    autocomplete_fields = ('user', 'pizza')
    list_filter = (ApprovedListFilter, )
    actions = ['set_approved', 'set_unapproved']

    def set_approved(self, request, queryset):
        queryset.filter(
            approved_user__isnull=True
        ).update(
            approved_user=request.user,
            approved_time=timezone.now()
        )

    def set_unapproved(self, request, queryset):
        queryset.filter(
            approved_user__isnull=False
        ).update(
            approved_user=None,
            approved_time=None
        )
