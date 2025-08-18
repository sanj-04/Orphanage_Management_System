from django.contrib import admin
from django.utils.html import format_html
from django.core.mail import send_mail
from .models import Registration, AdoptionApplication, Child
import random
import string
from django.db.models import Count
from django.contrib.auth.models import User


@admin.register(Registration)
class RegistrationAdmin(admin.ModelAdmin):
    list_display = (
        "father_name", "mother_name", "father_email", "mother_email","user",
        "submitted_at", "is_approved", "document_link"
    )
    list_filter = ("is_approved", "submitted_at")
    search_fields = ("father_name", "mother_name", "father_email", "mother_email")
    readonly_fields = ('submitted_at', 'user', 'password')

    actions = ["approve_registration", "deny_registration"]

    def document_link(self, obj):
        if obj.document:
            return format_html("<a href='{}' target='_blank'>View Document</a>", obj.document.url)
        return "-"
    document_link.short_description = "Document"
    
    def approve_registration(self, request, queryset):
        for reg in queryset:
            if not reg.is_approved:
                # Decide applicant details
                if reg.father_email:
                    username = reg.father_email.split("@")[0]
                    first_name = reg.father_name or "Parent"
                    email = reg.father_email
                elif reg.mother_email:
                    username = reg.mother_email.split("@")[0]
                    first_name = reg.mother_name or "Parent"
                    email = reg.mother_email
                else:
                    username = f"user_{reg.id}"
                    first_name = "Parent"
                    email = ""

                # Ensure unique username
                base_username = username
                counter = 1
                while User.objects.filter(username=username).exists():
                    username = f"{base_username}{counter}"
                    counter += 1

                # Generate random password
                raw_password = ''.join(random.choices(string.ascii_letters + string.digits, k=8))

                # Create user
                user = User.objects.create_user(
                    username=username,
                    first_name=first_name,
                    email=email,
                    password=raw_password
                )

                # Link registration
                reg.user = user
                reg.is_approved = True
                reg.password = raw_password  # store temporarily (not best practice but fine for project)
                reg.save()

                # Send email with credentials
                recipients = [e for e in [reg.father_email, reg.mother_email] if e]
                if recipients:
                    send_mail(
                        "Your Registration is Approved",
                        f"Dear {first_name},\n\n"
                        f"Your application has been approved.\n\n"
                        f"Username: {username}\nPassword: {raw_password}\n\n"
                        "Thank you,\nHopeNest Team",
                        "admin@example.com",
                        recipients,
                        fail_silently=False,
                    )

        self.message_user(request, "Selected registrations approved and credentials sent.")

    def deny_registration(self, request, queryset):
        for reg in queryset:
            recipients = [e for e in [reg.father_email, reg.mother_email] if e]
            if recipients:
                send_mail(
                    "Your Registration is Declined",
                    f"Dear {reg.father_name or ''} {reg.mother_name or ''},\n\n"
                    "We regret to inform you that your application has been declined.",
                    "admin@example.com",
                    recipients,
                    fail_silently=False,
                )
            reg.delete()
        self.message_user(request, "Selected registrations declined and applicants notified.")


@admin.register(AdoptionApplication)
class AdoptionApplicationAdmin(admin.ModelAdmin):
    list_display = ("user", "full_name", "email", "phone", "child", "status", "created_at")
    list_filter = ("status", "created_at", "child")
    search_fields = ("full_name", "email", "phone", "child__name", "user__username")
    readonly_fields = ('created_at',)

    actions = ["approve_adoption", "reject_adoption"]

    def approve_adoption(self, request, queryset):
        for app in queryset:
            app.status = "Approved"
            app.save()
            app.child.status = "Adopted"
            app.child.save()
        self.message_user(request, "Selected applications approved.")

    def reject_adoption(self, request, queryset):
        for app in queryset:
            app.status = "Rejected"
            app.save()
            app.child.status = "Available"
            app.child.save()
        self.message_user(request, "Selected applications rejected.")


@admin.register(Child)
class ChildAdmin(admin.ModelAdmin):
    list_display = ("name", "age", "gender", "location", "applications_count", "image_preview")
    search_fields = ("name", "location", "gender")
    list_filter = ('gender', 'location')

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.annotate(app_count=Count("applications"))

    def applications_count(self, obj):
        return obj.app_count
    applications_count.short_description = "Applications"

    def image_preview(self, obj):
        if obj.image:
            return format_html("<img src='{}' style='height: 50px;' />", obj.image.url)
        return "-"
    image_preview.short_description = "Photo"
