# from django.shortcuts import render
# from rest_framework.views import APIView
# from rest_framework.parsers import MultiPartParser, FormParser
# from rest_framework.response import Response
# from rest_framework import status
# from .serializers import RegisterSerializer
# from django.core.mail import EmailMultiAlternatives, send_mail
# from django.http import JsonResponse
# from django.contrib.auth.models import User
# from django.utils.crypto import get_random_string
# from django.conf import settings
# from rest_framework.authtoken.models import Token
# from django.contrib.auth import authenticate
# from rest_framework import generics, permissions
# from rest_framework.permissions import IsAuthenticated
# from rest_framework.decorators import api_view
# from rest_framework import viewsets
# from rest_framework.decorators import action
# from .models import Registration, Child, AdoptionApplication
# from .serializers import RegistrationSerializer, ChildSerializer, AdoptionApplicationSerializer
# import random, string

# class RegistrationViewSet(viewsets.ModelViewSet):
#     queryset = Registration.objects.all().order_by('-submitted_at')
#     serializer_class = RegistrationSerializer

#     @action(detail=True, methods=['post'])
#     def approve(self, request, pk=None):
#         reg = self.get_object()
#         if not reg.is_approved:
#             reg.is_approved = True
#             reg.user_id = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
#             reg.password = ''.join(random.choices(string.ascii_letters + string.digits, k=10))
#             reg.save()
#             send_mail(
#                 "Registration Approved",
#                 f"Your registration is approved!\nUser ID: {reg.user_id}\nPassword: {reg.password}",
#                 "admin@example.com",
#                 [reg.father_email, reg.mother_email]
#             )
#         return Response({"status": "approved"})

#     @action(detail=True, methods=['post'])
#     def deny(self, request, pk=None):
#         reg = self.get_object()
#         send_mail(
#             "Registration Declined",
#             "Your registration has been declined.",
#             "admin@example.com",
#             [reg.father_email, reg.mother_email]
#         )
#         reg.delete()
#         return Response({"status": "denied"})


# class ChildViewSet(viewsets.ModelViewSet):
#     queryset = Child.objects.all()
#     serializer_class = ChildSerializer


# class AdoptionApplicationViewSet(viewsets.ModelViewSet):
#     queryset = AdoptionApplication.objects.all().order_by('-created_at')
#     serializer_class = AdoptionApplicationSerializer


# def create_user_account(email, name):
#     username = email.split("@")[0] + get_random_string(4)
#     password = get_random_string(10)

#     user = User.objects.create_user(username=username, email=email, password=password)
#     user.first_name = name
#     user.save()

#     return username, password


# class RegisterView(APIView):
#     parser_classes = (MultiPartParser, FormParser)

#     def post(self, request, format=None):
#         serializer = RegisterSerializer(data=request.data)

#         if serializer.is_valid():
#             instance = serializer.save()

#             applicants = []
#             if instance.father_name and instance.father_email:
#                 applicants.append((instance.father_name, instance.father_email))
#             if instance.mother_name and instance.mother_email:
#                 applicants.append((instance.mother_name, instance.mother_email))

#             if not applicants:
#                 return Response(
#                     {"error": "At least one valid parent name and email must be provided."},
#                     status=400
#                 )

#             greeting_names = " and ".join([a[0] for a in applicants])
#             recipient_emails = [a[1] for a in applicants]

#             # Send confirmation email
#             subject = 'HopeNest Registration Received'
#             from_email = settings.EMAIL_HOST_USER

#             text_content = f"""
# Dear {greeting_names},

# Thank you for registering with HopeNest for adoption consideration.
# We have received your application and will get back to you after reviewing the details.

# Regards,
# HopeNest Team
# """

#             html_content = f"""
# <html>
# <body>
#     <h2 style="color:#4CAF50;">HopeNest - Adoption Registration</h2>
#     <p>Dear <strong>{greeting_names}</strong>,</p>
#     <p>Thank you for registering with <b>HopeNest</b> for adoption consideration.</p>
#     <p>We have received your application and will get back to you after reviewing the details.</p>
#     <br>
#     <p style="color:gray;">Warm regards,<br>HopeNest Team</p>
# </body>
# </html>
# """

#             try:
#                 email = EmailMultiAlternatives(subject, text_content, from_email, recipient_emails)
#                 email.attach_alternative(html_content, "text/html")
#                 email.send()
#             except Exception as e:
#                 print("❌ Failed to send confirmation email:", str(e))

#             # Send login credentials to first applicant
#             login_name, login_email = applicants[0]
#             try:
#                 username, password = create_user_account(login_email, login_name)

#                 login_subject = "HopeNest Login Credentials"
#                 login_message = f"""
# Hello {login_name},

# Your registration is now complete.

# Here are your login credentials for the HopeNest portal:

# Username: {username}
# Password: {password}

# Please keep these details safe and do not share them with anyone.

# You can now log in and proceed with adoption requests.

# Warm regards,  
# HopeNest Team
# """
#                 send_mail(
#                     login_subject,
#                     login_message,
#                     settings.EMAIL_HOST_USER,
#                     [login_email],
#                     fail_silently=False,
#                 )
#             except Exception as e:
#                 print("⚠️ Error sending login credentials:", str(e))

#             return Response(
#                 {"message": "Registration successful. Confirmation email sent."},
#                 status=status.HTTP_201_CREATED
#             )

#         return Response(serializer.errors, status=400)


# class LoginView(APIView):
#     def post(self, request):
#         username = request.data.get('username')
#         password = request.data.get('password')

#         if not username or not password:
#             return Response({"detail": "Both username and password are required."}, status=400)

#         user = authenticate(username=username, password=password)

#         if user is not None:
#             token, created = Token.objects.get_or_create(user=user)
#             print("Received login data:", request.data)
#             return Response({
#                 "message": "Login successful.",
#                 "token": token.key,
#                 "user_id": username,
#             }, status=200)

#         else:
#             return Response({"detail": "Invalid username or password."}, status=401)
        

# # class AdoptionApplicationView(APIView):
# #     permission_classes = [IsAuthenticated]

# #     def post(self, request):
# #         serializer = AdoptionApplicationSerializer(data=request.data)
# #         if serializer.is_valid():
# #             serializer.save(user=request.user)
# #             return Response({"message": "Application submitted successfully."}, status=status.HTTP_201_CREATED)
# #         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

# @api_view(['POST'])
# def adoption_application_view(request):
#     serializer = AdoptionApplicationSerializer(data=request.data)
#     if serializer.is_valid():
#         serializer.save()
#         return Response({"message": "Your adoption application has been submitted successfully!"}, status=status.HTTP_201_CREATED)
#     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




# class AdoptionApplicationView(APIView):
#     permission_classes = [IsAuthenticated]  # user must be logged in

#     def post(self, request):
#         user = request.user
#         full_name = request.data.get("full_name")
#         email = request.data.get("email")
#         phone = request.data.get("phone")
#         address = request.data.get("address")

#         application = AdoptionApplication.objects.create(
#             user=user,
#             full_name=full_name,
#             email=email,
#             phone=phone,
#             address=address
#         )

#         return Response({"message": "Adoption request submitted successfully."}, status=201)


# class ChildListView(generics.ListAPIView):
#     queryset = Child.objects.all()
#     serializer_class = ChildSerializer



from rest_framework import viewsets, generics, status
from rest_framework.decorators import action, api_view
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.views import APIView
from django.core.mail import send_mail, EmailMultiAlternatives
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.utils.crypto import get_random_string
from django.conf import settings
from rest_framework.authtoken.models import Token
import random, string

from .models import Registration, Child, AdoptionApplication
from .serializers import (
    RegistrationSerializer,
    RegisterSerializer,
    ChildSerializer,
    AdoptionApplicationSerializer
)

# ---------------------- ADMIN API ----------------------

class RegistrationViewSet(viewsets.ModelViewSet):
    """Admin: Manage registrations, approve or deny applications."""
    queryset = Registration.objects.all().order_by('-submitted_at')
    serializer_class = RegistrationSerializer

    @action(detail=True, methods=['post'])
    def approve(self, request, pk=None):
        reg = self.get_object()
        if not reg.is_approved:
            reg.is_approved = True
            reg.user_id = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
            reg.password = ''.join(random.choices(string.ascii_letters + string.digits, k=10))
            reg.save()

            send_mail(
                "Registration Approved",
                f"Your registration is approved!\nUser ID: {reg.user_id}\nPassword: {reg.password}",
                settings.EMAIL_HOST_USER,
                [reg.father_email, reg.mother_email]
            )
        return Response({"status": "approved"})

    @action(detail=True, methods=['post'])
    def deny(self, request, pk=None):
        reg = self.get_object()
        send_mail(
            "Registration Declined",
            "Your registration has been declined.",
            settings.EMAIL_HOST_USER,
            [reg.father_email, reg.mother_email]
        )
        reg.delete()
        return Response({"status": "denied"})


class ChildViewSet(viewsets.ModelViewSet):
    """Admin: CRUD for children."""
    queryset = Child.objects.all()
    serializer_class = ChildSerializer


class AdoptionApplicationViewSet(viewsets.ModelViewSet):
    """Admin: Manage adoption applications."""
    queryset = AdoptionApplication.objects.all().order_by('-created_at')
    serializer_class = AdoptionApplicationSerializer


# ---------------------- PUBLIC API ----------------------

def create_user_account(email, name):
    """Helper to create a user account and return credentials."""
    username = email.split("@")[0] + get_random_string(4)
    password = get_random_string(10)
    user = User.objects.create_user(username=username, email=email, password=password)
    user.first_name = name
    user.save()
    return username, password


class RegisterView(APIView):
    """Public: Submit adoption registration request."""
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

            # Confirmation email
            subject = 'HopeNest Registration Received'
            from_email = settings.EMAIL_HOST_USER
            text_content = f"Dear {greeting_names},\n\nThank you for registering..."
            html_content = f"<p>Dear <strong>{greeting_names}</strong>, Thank you for registering...</p>"

            email = EmailMultiAlternatives(subject, text_content, from_email, recipient_emails)
            email.attach_alternative(html_content, "text/html")
            email.send()

            # Login credentials for first applicant
            login_name, login_email = applicants[0]
            username, password = create_user_account(login_email, login_name)
            send_mail(
                "HopeNest Login Credentials",
                f"Username: {username}\nPassword: {password}",
                settings.EMAIL_HOST_USER,
                [login_email]
            )

            return Response({"message": "Registration successful"}, status=201)

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


# @api_view(['POST'])
# def adoption_application_view(request):
#     """Public: Submit an adoption application."""
#     serializer = AdoptionApplicationSerializer(data=request.data)
#     if serializer.is_valid():
#         serializer.save()
#         return Response({"message": "Application submitted successfully"}, status=201)
#     return Response(serializer.errors, status=400)

@api_view(['POST'])
def adoption_application_view(request):
    """Public: Submit an adoption application for a specific child."""
    
    # Make sure 'child' field is provided
    child_id = request.data.get('child')
    if not child_id:
        return Response({"error": "Child ID is required."}, status=status.HTTP_400_BAD_REQUEST)

    # Check if child exists
    try:
        child_obj = Child.objects.get(pk=child_id)
    except Child.DoesNotExist:
        return Response({"error": "Invalid child ID."}, status=status.HTTP_404_NOT_FOUND)

    # Validate and save application
    serializer = AdoptionApplicationSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(child=child_obj)  # link child to application
        return Response({"message": "Application submitted successfully"}, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ChildListView(generics.ListAPIView):
    """Public: List children available for adoption."""
    queryset = Child.objects.all()
    serializer_class = ChildSerializer
