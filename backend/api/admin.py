# # # Register your models here.
# # from django.contrib import admin
# # from .models import Registration
# # from .models import AdoptionApplication

# # admin.site.register(Registration)

# # @admin.register(AdoptionApplication)
# # class AdoptionApplicationAdmin(admin.ModelAdmin):
# #     list_display = ('full_name', 'email', 'phone', 'created_at')

# from django.contrib import admin
# from .models import Registration, AdoptionApplication, Child
# from django.core.mail import send_mail
# import random, string

# @admin.register(Registration)
# class RegistrationAdmin(admin.ModelAdmin):
#     list_display = ("father_name", "mother_name", "father_email", "is_approved", "submitted_at")
#     search_fields = ("father_name", "mother_name", "father_email")
#     list_filter = ("is_approved",)
#     readonly_fields = ("user_id", "password")

#     def save_model(self, request, obj, form, change):
#         # Check if approval status changed to True
#         if obj.is_approved and not obj.user_id:
#             # Generate credentials
#             obj.user_id = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
#             obj.password = ''.join(random.choices(string.ascii_letters + string.digits, k=10))

#             # Send approval email
#             send_mail(
#                 subject="Adoption Registration Approved",
#                 message=f"Your registration has been approved!\nUser ID: {obj.user_id}\nPassword: {obj.password}",
#                 from_email="admin@example.com",
#                 recipient_list=[obj.father_email, obj.mother_email],
#                 fail_silently=False,
#             )

#         elif not obj.is_approved and change:
#             # Send rejection email
#             send_mail(
#                 subject="Adoption Registration Declined",
#                 message="We regret to inform you that your adoption registration has been declined.",
#                 from_email="admin@example.com",
#                 recipient_list=[obj.father_email, obj.mother_email],
#                 fail_silently=False,
#             )

#         super().save_model(request, obj, form, change)


# @admin.register(Child)
# class ChildAdmin(admin.ModelAdmin):
#     list_display = ("name", "age", "gender", "location")
#     search_fields = ("name", "location", "gender")
#     list_filter = ("gender", "location")


# @admin.register(AdoptionApplication)
# class AdoptionApplicationAdmin(admin.ModelAdmin):
#     list_display = ("full_name", "email", "status", "created_at")
#     search_fields = ("full_name", "email")
#     list_filter = ("status",)


from django.contrib import admin
from django.utils.html import format_html
from django.core.mail import send_mail
from .models import Registration, AdoptionApplication, Child
import random
import string
from django.db.models import Count

# ------------------- REGISTRATION ADMIN -------------------
@admin.register(Registration)

class RegistrationAdmin(admin.ModelAdmin):
    list_display = (
        "father_name", "mother_name", "father_email", "mother_email",
        "submitted_at", "is_approved", "document_link"
    )
    list_filter = ("is_approved", "submitted_at")
    search_fields = ("father_name", "mother_name", "father_email", "mother_email")
    readonly_fields = ('submitted_at',)
    def document_link(self, obj):
        if obj.document:
            return format_html("<a href='{}' target='_blank'>View Document</a>", obj.document.url)
        return "-"
    document_link.short_description = "Document"

    actions = ["approve_registration", "deny_registration"]

    def approve_registration(self, request, queryset):
        """Approve and send email with generated user ID & password"""
        for reg in queryset:
            if not reg.is_approved:
                reg.is_approved = True
                reg.user_id = f"user_{reg.id}"
                reg.password = "".join(random.choices(string.ascii_letters + string.digits, k=8))
                reg.save()

                send_mail(
                    "Your Registration is Approved",
                    f"Dear {reg.father_name} & {reg.mother_name},\n\n"
                    f"Your application has been approved.\n"
                    f"User ID: {reg.user_id}\nPassword: {reg.password}\n\nThank you.",
                    "admin@example.com",
                    [reg.father_email, reg.mother_email],
                    fail_silently=False,
                )
        self.message_user(request, "Selected registrations approved and credentials sent.")
    approve_registration.short_description = "Approve and send credentials"

    def deny_registration(self, request, queryset):
        """Deny and send rejection email"""
        for reg in queryset:
            send_mail(
                "Your Registration is Declined",
                f"Dear {reg.father_name} & {reg.mother_name},\n\n"
                "We regret to inform you that your application has been declined.",
                "admin@example.com",
                [reg.father_email, reg.mother_email],
                fail_silently=False,
            )
            reg.delete()
        self.message_user(request, "Selected registrations declined and applicants notified.")
    deny_registration.short_description = "Deny and notify applicant"


# ------------------- ADOPTION APPLICATION ADMIN -------------------
@admin.register(AdoptionApplication)

class AdoptionApplicationAdmin(admin.ModelAdmin):
    list_display = ("user", "full_name", "email", "phone", "child", "status", "created_at")
    list_filter = ("status", "created_at", "child")
    search_fields = ("full_name", "email", "phone", "child__name", "user__username")
    readonly_fields = ('created_at',)
    actions = ["approve_adoption", "reject_adoption"]

    def approve_adoption(self, request, queryset):
        queryset.update(status="Approved")
        self.message_user(request, "Selected applications approved.")
    approve_adoption.short_description = "Approve selected adoption applications"

    def reject_adoption(self, request, queryset):
        queryset.update(status="Rejected")
        self.message_user(request, "Selected applications rejected.")
    reject_adoption.short_description = "Reject selected adoption applications"

# ------------------- CHILD ADMIN -------------------
@admin.register(Child)

class ChildAdmin(admin.ModelAdmin):
    list_display = ("name", "age", "gender", "location", "applications_count", "image_preview")
    search_fields = ("name", "location", "gender")
    list_filter = ('gender', 'location')
    def get_queryset(self, request):
        # Annotate each child with the number of related adoption applications
        qs = super().get_queryset(request)
        return qs.annotate(app_count=Count("adoptionapplication"))

    def applications_count(self, obj):
        return obj.app_count
    applications_count.short_description = "Applications"

    def image_preview(self, obj):
        if obj.image:
            return format_html("<img src='{}' style='height: 50px;' />", obj.image.url)
        return "-"
    image_preview.short_description = "Photo"