
# from rest_framework import viewsets, generics, status
# from rest_framework.decorators import action, api_view
# from rest_framework.response import Response
# from rest_framework.parsers import MultiPartParser, FormParser
# from rest_framework.views import APIView
# from django.core.mail import send_mail, EmailMultiAlternatives
# from django.contrib.auth import authenticate
# from django.conf import settings
# from rest_framework.authtoken.models import Token
# import random, string
# from django.contrib.auth.models import User

# from .models import Registration, Child, AdoptionApplication
# from .serializers import (
#     RegistrationSerializer,
#     RegisterSerializer,
#     ChildSerializer,
#     AdoptionApplicationSerializer
# )

# # ---------------------- ADMIN API ----------------------

# class RegistrationViewSet(viewsets.ModelViewSet):
#     """Admin: Manage registrations, approve or deny applications."""
#     queryset = Registration.objects.all().order_by('-submitted_at')
#     serializer_class = RegistrationSerializer

#     @action(detail=True, methods=['post'])
#     def approve(self, request, pk=None):
#         """Approve registration, create ONE user account, and send same credentials to both parents if available."""
#         reg = self.get_object()
#         if not reg.is_approved:
#             reg.is_approved = True

#             # Generate one set of credentials for the family
#             username = f"user_{reg.id}"
#             password = get_random_string(10)

#             # Create user account (if not exists)
#             user, created = User.objects.get_or_create(
#                 username=username,
#                 defaults={"email": reg.father_email or reg.mother_email}
#             )
#             if created:
#                 user.set_password(password)
#                 user.first_name = f"{reg.father_name} & {reg.mother_name}" if reg.mother_name else reg.father_name
#                 user.save()

#             # Store credentials in Registration model for reference
#             reg.user_id = username
#             reg.password = password
#             reg.save()

#             # Collect all available parent emails
#             recipient_emails = []
#             if reg.father_email:
#                 recipient_emails.append(reg.father_email)
#             if reg.mother_email and reg.mother_email not in recipient_emails:
#                 recipient_emails.append(reg.mother_email)

#             # Send same credentials to both
#             send_mail(
#                 "HopeNest Login Credentials",
#                 f"Dear {reg.father_name} & {reg.mother_name},\n\n"
#                 f"Your application has been approved.\n\n"
#                 f"Here are your login credentials:\n"
#                 f"Username: {username}\nPassword: {password}\n\n"
#                 f"Please log in to continue.",
#                 settings.EMAIL_HOST_USER,
#                 recipient_emails,
#                 fail_silently=False,
#             )

#         return Response({"status": "approved"})


#     @action(detail=True, methods=['post'])
#     def deny(self, request, pk=None):
#         """Deny registration and notify applicant."""
#         reg = self.get_object()
#         recipient_emails = []
#         if reg.father_email:
#             recipient_emails.append(reg.father_email)
#         if reg.mother_email:
#             recipient_emails.append(reg.mother_email)

#         send_mail(
#             "Registration Declined",
#             f"Dear {reg.father_name} & {reg.mother_name},\n\n"
#             "We regret to inform you that your application has been declined.",
#             settings.EMAIL_HOST_USER,
#             recipient_emails
#         )
#         reg.delete()
#         return Response({"status": "denied"})


# class ChildViewSet(viewsets.ModelViewSet):
#     """Admin: CRUD for children."""
#     queryset = Child.objects.all()
#     serializer_class = ChildSerializer


# class AdoptionApplicationViewSet(viewsets.ModelViewSet):
#     """Admin: Manage adoption applications."""
#     queryset = AdoptionApplication.objects.all().order_by('-created_at')
#     serializer_class = AdoptionApplicationSerializer


# # ---------------------- PUBLIC API ----------------------

# class RegisterView(APIView):
#     """Public: Submit adoption registration request."""
#     parser_classes = (MultiPartParser, FormParser)

#     def post(self, request):
#         serializer = RegisterSerializer(data=request.data)
#         if serializer.is_valid():
#             instance = serializer.save()  # Save Registration object

#             # Collect parent names + emails
#             applicants = []
#             if instance.father_name and instance.father_email:
#                 applicants.append((instance.father_name, instance.father_email))
#             if instance.mother_name and instance.mother_email:
#                 applicants.append((instance.mother_name, instance.mother_email))

#             if not applicants:
#                 return Response({"error": "At least one parent's details required."}, status=400)

#             greeting_names = " and ".join([a[0] for a in applicants])
#             recipient_emails = [a[1] for a in applicants]

#             # ✅ Send confirmation email (no credentials here)
#             subject = 'HopeNest Registration Received'
#             from_email = settings.EMAIL_HOST_USER
#             text_content = f"Dear {greeting_names},\n\nYour registration has been received. Please wait for admin approval."
#             html_content = f"<p>Dear <strong>{greeting_names}</strong>,<br>Your registration has been received. Please wait for admin approval.</p>"

#             email = EmailMultiAlternatives(subject, text_content, from_email, recipient_emails)
#             email.attach_alternative(html_content, "text/html")
#             email.send()

#             return Response({"message": "Registration submitted. Confirmation email sent."}, status=201)

#         return Response(serializer.errors, status=400)



# class LoginView(APIView):
#     """Public: Login endpoint."""
#     def post(self, request):
#         username = request.data.get('username')
#         password = request.data.get('password')
#         if not username or not password:
#             return Response({"detail": "Both username and password are required."}, status=400)

#         user = authenticate(username=username, password=password)
#         if user:
#             token, created = Token.objects.get_or_create(user=user)
#             return Response({
#                 "message": "Login successful",
#                 "token": token.key,
#                 "user_id": username
#             })
#         return Response({"detail": "Invalid username or password."}, status=401)


# # @api_view(['POST'])
# # def adoption_application_view(request):
# #     """Public: Submit an adoption application for a specific child."""
# #     child_id = request.data.get('child')
# #     if not child_id:
# #         return Response({"error": "Child ID is required."}, status=status.HTTP_400_BAD_REQUEST)

# #     try:
# #         child_obj = Child.objects.get(pk=child_id)
# #     except Child.DoesNotExist:
# #         return Response({"error": "Invalid child ID."}, status=status.HTTP_404_NOT_FOUND)

# #     serializer = AdoptionApplicationSerializer(data=request.data)
# #     if serializer.is_valid():
# #         serializer.save(child=child_obj)
# #         return Response({"message": "Application submitted successfully"}, status=status.HTTP_201_CREATED)

# #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# @api_view(['POST'])
# def adoption_application_view(request):
#     child_id = request.data.get('child')
#     user_id = request.data.get('user')

#     if not child_id or not user_id:
#         return Response({"error": "Child ID and User ID required."}, status=400)

#     try:
#         child = Child.objects.get(pk=child_id, status="Available")
#     except Child.DoesNotExist:
#         return Response({"error": "Child not available."}, status=404)

#     user = User.objects.get(pk=user_id)

#     # Save application
#     application = AdoptionApplication.objects.create(
#         user=user,
#         full_name=request.data.get("full_name", user.username),
#         email=request.data.get("email", user.email),
#         phone=request.data.get("phone", ""),
#         address=request.data.get("address", ""),
#         user_message=request.data.get("message", ""),
#         child=child
#     )

#     # mark child as pending
#     child.status = "Pending"
#     child.save()

#     return Response({"message": "Application submitted successfully"}, status=201)


# class ChildListView(generics.ListAPIView):
#     """Public: List children available for adoption."""
#     queryset = Child.objects.all()
#     serializer_class = ChildSerializer


from rest_framework import viewsets, generics, status
from rest_framework.decorators import action, api_view
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.views import APIView
from django.core.mail import send_mail, EmailMultiAlternatives
from django.contrib.auth import authenticate
from django.conf import settings
from rest_framework.authtoken.models import Token

from .models import Registration, Child, AdoptionApplication
from .serializers import (
    RegistrationSerializer,
    RegisterSerializer,
    ChildSerializer,
    AdoptionApplicationSerializer
)

# ---------------------- ADMIN API ----------------------
class RegistrationViewSet(viewsets.ModelViewSet):
    """Admin: Manage registrations (approval handled in admin.py)."""
    queryset = Registration.objects.all().order_by('-submitted_at')
    serializer_class = RegistrationSerializer


class ChildViewSet(viewsets.ModelViewSet):
    """Admin: CRUD for children."""
    queryset = Child.objects.all()
    serializer_class = ChildSerializer


class AdoptionApplicationViewSet(viewsets.ModelViewSet):
    """Admin: Manage adoption applications."""
    queryset = AdoptionApplication.objects.all().order_by('-created_at')
    serializer_class = AdoptionApplicationSerializer


# ---------------------- PUBLIC API ----------------------
class RegisterView(APIView):
    """Public: Submit adoption registration request (confirmation only)."""
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            instance = serializer.save()

            applicants = []
            if instance.father_name and instance.father_email:
                applicants.append((instance.father_name, instance.father_email))
            if instance.mother_name and instance.mother_email:
                applicants.append((instance.mother_name, instance.mother_email))

            if not applicants:
                return Response({"error": "At least one parent's details required."}, status=400)

            greeting_names = " and ".join([a[0] for a in applicants])
            recipient_emails = [a[1] for a in applicants]

            # ✅ Only confirmation email (NO credentials here)
            subject = 'HopeNest Registration Received'
            from_email = settings.EMAIL_HOST_USER
            text_content = f"Dear {greeting_names},\n\nThank you for registering with HopeNest. Your application has been received and is under review."
            html_content = f"<p>Dear <strong>{greeting_names}</strong>,</p><p>Thank you for registering with HopeNest. Your application has been received and is under review.</p>"

            email = EmailMultiAlternatives(subject, text_content, from_email, recipient_emails)
            email.attach_alternative(html_content, "text/html")
            email.send()

            return Response({"message": "Registration submitted successfully"}, status=201)

        return Response(serializer.errors, status=400)


class LoginView(APIView):
    """Public: Login endpoint."""
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        if not username or not password:
            return Response({"detail": "Both username and password are required."}, status=400)

        user = authenticate(username=username, password=password)
        if user:
            token, created = Token.objects.get_or_create(user=user)
            return Response({
                "message": "Login successful",
                "token": token.key,
                "user_id": username
            })
        return Response({"detail": "Invalid username or password."}, status=401)


@api_view(['POST'])
def adoption_application_view(request):
    """Public: Submit an adoption application for a specific child."""
    child_id = request.data.get('child')
    if not child_id:
        return Response({"error": "Child ID is required."}, status=status.HTTP_400_BAD_REQUEST)

    try:
        child_obj = Child.objects.get(pk=child_id)
    except Child.DoesNotExist:
        return Response({"error": "Invalid child ID."}, status=status.HTTP_404_NOT_FOUND)

    serializer = AdoptionApplicationSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(child=child_obj)
        return Response({"message": "Application submitted successfully"}, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ChildListView(generics.ListAPIView):
    """Public: List children available for adoption."""
    queryset = Child.objects.all()
    serializer_class = ChildSerializer
