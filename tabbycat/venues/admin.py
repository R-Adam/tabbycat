from django.contrib import admin
from django import forms
from gfklookupwidget.widgets import GfkLookupWidget

from .models import (
    AdjudicatorVenueConstraint, DivisionVenueConstraint,
    InstitutionVenueConstraint, TeamVenueConstraint, Venue, VenueConstraint, VenueGroup)


class VenueGroupAdmin(admin.ModelAdmin):
    list_display = ('name', 'short_name', 'team_capacity')
    search_fields = ('name', )


admin.site.register(VenueGroup, VenueGroupAdmin)


class VenueAdmin(admin.ModelAdmin):
    list_display = ('name', 'group_name', 'priority', 'tournament')
    list_filter = ('group', 'priority', 'tournament')
    search_fields = ('name',)

    def group_name(self, obj):
        if obj.group is None:
            return None
        return obj.group.name
    group_name.short_description = 'Venue Group'

    def get_queryset(self, request):
        return super(VenueAdmin,
                     self).get_queryset(request).select_related('group')


admin.site.register(Venue, VenueAdmin)


# ==============================================================================
# VenueConstraint models
# ==============================================================================

class VenueConstraintModelForm(forms.ModelForm):
    class Meta(object):
        model = VenueConstraint
        fields = '__all__'
        widgets = {
            'subject_id': GfkLookupWidget(
                content_type_field_name='subject_content_type',
                parent_field=VenueConstraint._meta.get_field('subject_content_type'),
            )
        }


@admin.register(VenueConstraint)
class VenueConstraintAdmin(admin.ModelAdmin):
    form = VenueConstraintModelForm
    list_display = ('subject', 'group_name', 'priority')
    search_fields = ('adjudicator__name', 'adjudicator__institution__code',
            'adjudicator__institution__name', 'team__short_name', 'team__long_name',
            'institution__name', 'institution__code', 'division__name',
            'venue_group__name', 'venue_group__short_name', 'priority')
    list_filter = ('subject_content_type', 'venue_group', 'priority')

    def group_name(self, obj):
        if obj.venue_group is None:
            return None
        return obj.venue_group.name
    group_name.short_description = 'Venue Group'


class BaseVenueConstraintAdmin(admin.ModelAdmin):
    associate_field = None
    associate_search_fields = ()

    common_list_display = ('group_name', 'priority')
    common_search_fields = ('venue_group__name', 'venue_group__short_name', 'priority')
    common_list_filter = ('venue_group', 'priority')

    def group_name(self, obj):
        if obj.venue_group is None:
            return None
        return obj.venue_group.name
    group_name.short_description = 'Venue Group'

    def get_list_display(self, request):
        return (self.associate_field,) + self.common_list_display

    def get_search_fields(self, request):
        return self.associate_search_fields + self.common_search_fields

    def get_list_filter(self, request):
        return (self.associate_field,) + self.common_list_filter

    @property
    def raw_id_fields(self):
        return (self.associate_field,)


@admin.register(TeamVenueConstraint)
class TeamVenueConstraintAdmin(BaseVenueConstraintAdmin):
    associate_field = 'team'
    associate_search_fields = ('team__short_name', 'team__long_name')


@admin.register(AdjudicatorVenueConstraint)
class AdjudicatorVenueConstraintAdmin(BaseVenueConstraintAdmin):
    associate_field = 'adjudicator'
    associate_search_fields = ('adjudicator__name',)


@admin.register(InstitutionVenueConstraint)
class InstitutionVenueConstraintAdmin(BaseVenueConstraintAdmin):
    associate_field = 'institution'
    associate_search_fields = ('institution__name', 'institution__code')


@admin.register(DivisionVenueConstraint)
class DivisionVenueConstraintAdmin(BaseVenueConstraintAdmin):
    associate_field = 'division'
    associate_search_fields = ('division__name',)
