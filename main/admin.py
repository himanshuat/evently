from django.contrib import admin
from django.utils.html import format_html
from .models import *


admin.site.site_header = "Evently Administration"
admin.site.site_title = "Evently Admin Portal"
admin.site.index_title = "Welcome to Evently Admin"


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'full_name', 'email', 'is_active', 'image_tag')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    list_filter = ('is_active',)
    readonly_fields = ('image_tag',)

    def image_tag(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="height: 40px; width: 40px; object-fit: "cover";" />', obj.image.url)
        return ''
    image_tag.short_description = 'Profile Image'


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('name', 'organizer', 'status', 'starttime', 'endtime', 'price', 'rating')
    list_filter = ('eventtype', 'starttime')
    search_fields = ('name', 'location', 'description')
    readonly_fields = ('rating', 'is_completed')

    def rating(self, obj):
        return obj.rating or "No Rating"
    rating.short_description = 'Average Rating'


@admin.register(Attendee)
class AttendeeAdmin(admin.ModelAdmin):
    list_display = ('event', 'user', 'attendance_status')
    list_filter = ('attended',)
    search_fields = ('user__username', 'event__name')
    actions = ['mark_as_attended', 'mark_as_not_attended']

    def attendance_status(self, obj):
        status_colors = {
            'Yes': 'green',
            'No': 'red',
            'Unknown': 'gray'
        }
        color = status_colors.get(obj.attended, 'gray')
        return format_html(
            '<span style="color: {}; font-weight: bold;">{}</span>',
            color,
            obj.attended
        )
    attendance_status.short_description = "Attendance Status"

    def mark_as_attended(self, request, queryset):
        queryset.update(attended='Yes')
        self.message_user(request, "Selected attendees have been marked as 'Attended'.")
    mark_as_attended.short_description = "Mark as Attended"

    def mark_as_not_attended(self, request, queryset):
        queryset.update(attended='No')
        self.message_user(request, "Selected attendees have been marked as 'Not Attended'.")
    mark_as_not_attended.short_description = "Mark as Not Attended"


@admin.register(EventRating)
class EventRatingAdmin(admin.ModelAdmin):
    list_display = ('event', 'user', 'value', 'date')
    list_filter = ('date', 'value')
    search_fields = ('event__name', 'user__username')


@admin.register(EventRequest)
class EventRequestAdmin(admin.ModelAdmin):
    list_display = ('requester', 'event', 'status')
    list_filter = ('status', 'event')
    search_fields = ('requester__username', 'event__name')
    actions = ['bulk_approve_requests', 'bulk_decline_requests']

    def bulk_approve_requests(self, request, queryset):
        queryset.update(status='Accepted')
        self.message_user(request, "Selected requests have been approved.")
    bulk_approve_requests.short_description = "Approve Selected Requests"

    def bulk_decline_requests(self, request, queryset):
        queryset.update(status='Declined')
        self.message_user(request, "Selected requests have been declined.")
    bulk_decline_requests.short_description = "Decline Selected Requests"


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('user', 'event', 'amount', 'card_details', 'date', 'status')
    list_filter = ('status', 'date')
    search_fields = ('user__username', 'event__name', 'card_details')
