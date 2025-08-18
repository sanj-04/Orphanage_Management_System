
# from rest_framework import viewsets, generics, status
# from rest_framework.decorators import action, api_view
# from rest_framework.response import Response
# from rest_framework.parsers import MultiPartParser, FormParser
# from rest_framework.views import APIView
# from django.core.mail import send_mail, EmailMultiAlternatives
# from django.contrib.auth import authenticate
# from django.conf import settings
# from rest_framework.authtoken.models import Token
# from django.contrib.auth.models import User
# from rest_framework.decorators import permission_classes
# from rest_framework.permissions import IsAuthenticated
# from .models import Registration, Child, AdoptionApplication
# from .serializers import (
#     RegistrationSerializer,
#     RegisterSerializer,
#     ChildSerializer,
#     AdoptionApplicationSerializer
# )

# # ---------------------- ADMIN API ----------------------
# class RegistrationViewSet(viewsets.ModelViewSet):
#     """Admin: Manage registrations (approval handled in admin.py)."""
#     queryset = Registration.objects.all().order_by('-submitted_at')
#     serializer_class = RegistrationSerializer


# class ChildViewSet(viewsets.ModelViewSet):
#     """Admin: CRUD for children."""
#     queryset = Child.objects.all()
#     serializer_class = ChildSerializer

# def get_serializer_context(self):
#         return {"request": self.request}

# class AdoptionApplicationViewSet(viewsets.ModelViewSet):
#     """Admin: Manage adoption applications."""
#     queryset = AdoptionApplication.objects.all().order_by('-created_at')
#     serializer_class = AdoptionApplicationSerializer


# # ---------------------- PUBLIC API ----------------------
# class RegisterView(APIView):
#     """Public: Submit adoption registration request (confirmation only)."""
#     parser_classes = (MultiPartParser, FormParser)

#     def post(self, request):
#         serializer = RegisterSerializer(data=request.data)
#         if serializer.is_valid():
#             instance = serializer.save()

#             applicants = []
#             if instance.father_name and instance.father_email:
#                 applicants.append((instance.father_name, instance.father_email))
#             if instance.mother_name and instance.mother_email:
#                 applicants.append((instance.mother_name, instance.mother_email))

#             if not applicants:
#                 return Response({"error": "At least one parent's details required."}, status=400)

#             greeting_names = " and ".join([a[0] for a in applicants])
#             recipient_emails = [a[1] for a in applicants]

#             # ✅ Only confirmation email (NO credentials here)
#             subject = 'HopeNest Registration Received'
#             from_email = settings.EMAIL_HOST_USER
#             text_content = f"Dear {greeting_names},\n\nThank you for registering with HopeNest. Your application has been received and is under review."
#             html_content = f"<p>Dear <strong>{greeting_names}</strong>,</p><p>Thank you for registering with HopeNest. Your application has been received and is under review.</p>"

#             email = EmailMultiAlternatives(subject, text_content, from_email, recipient_emails)
#             email.attach_alternative(html_content, "text/html")
#             email.send()

#             return Response({"message": "Registration submitted successfully"}, status=201)

#         return Response(serializer.errors, status=400)


# class LoginView(APIView):
#     """Public: Login endpoint."""
#     def post(self, request):
#         username = request.data.get('username')
#         password = request.data.get('password')

#         if not username or not password:
#             return Response({"detail": "Both username and password are required."}, status=400)

#         user = authenticate(username=username, password=password)

#         if user is not None:
#             token, created = Token.objects.get_or_create(user=user)
#             return Response({
#                 "message": "Login successful",
#                 "token": token.key,
#                 "user_id": user.id,  # ✅ keep only this one
#                 "username": user.username,
#                 "email": user.email,
#                 "full_name": f"{user.first_name} {user.last_name}".strip() or user.username,
#                 "phone": getattr(user, "phone", None),   # optional if you extend later
#                 "address": getattr(user, "address", None),
#             }, status=status.HTTP_200_OK)

#         return Response({"detail": "Invalid username or password."}, status=401)

# class ChildListView(generics.ListAPIView):
#     """Public: List children available for adoption."""
#     queryset = Child.objects.all()
#     serializer_class = ChildSerializer

#     def get_serializer_context(self):
#             return {"request": self.request}

# @api_view(['POST'])
# @permission_classes([IsAuthenticated])  # only logged in users can adopt
# def adoption_application_view(request):
#     """Public: Submit an adoption application for a specific child."""

#     child_id = request.data.get("child")
#     user_id = request.data.get("user")

#     if not child_id:
#         return Response({"error": "Child ID is required."}, status=status.HTTP_400_BAD_REQUEST)
#     if not user_id:
#         return Response({"error": "User ID is required."}, status=status.HTTP_400_BAD_REQUEST)

#     # Check if child exists
#     try:
#         child_obj = Child.objects.get(pk=child_id)
#     except Child.DoesNotExist:
#         return Response({"error": "Invalid child ID."}, status=status.HTTP_404_NOT_FOUND)

#     # Check if user exists
#     try:
#         user_obj = User.objects.get(pk=user_id)
#     except User.DoesNotExist:
#         return Response({"error": "Invalid user ID."}, status=status.HTTP_404_NOT_FOUND)

#     # Build data for serializer
#     data = request.data.copy()
#     data["user"] = user_obj.id
#     data["child"] = child_obj.id

#     # ✅ Autofill from User model if not provided
#     if not data.get("full_name"):
#         full_name = f"{user_obj.first_name} {user_obj.last_name}".strip()
#         data["full_name"] = full_name if full_name else user_obj.username

#     if not data.get("email"):
#         data["email"] = user_obj.email or "N/A"

#     if not data.get("phone"):
#         data["phone"] = getattr(user_obj, "phone", "N/A")

#     if not data.get("address"):
#         data["address"] = getattr(user_obj, "address", "N/A")

#     serializer = AdoptionApplicationSerializer(data=data)
#     if serializer.is_valid():
#         serializer.save(user=user_obj, child=child_obj)

#         # ✅ Mark child as Pending
#         child_obj.status = "Pending"
#         child_obj.save()

#         return Response({"message": "Application submitted successfully"}, status=status.HTTP_201_CREATED)

#     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


from rest_framework import viewsets, generics, status
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.views import APIView
from django.core.mail import send_mail, EmailMultiAlternatives
from django.contrib.auth import authenticate
from django.conf import settings
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticated
from .models import Registration, Child, AdoptionApplication
from .serializers import (
    RegistrationSerializer,
    RegisterSerializer,
    ChildSerializer,
    AdoptionApplicationSerializer
)
from django.shortcuts import get_object_or_404

# ---------------------- ADMIN API ----------------------
class RegistrationViewSet(viewsets.ModelViewSet):
    """Admin: Manage registrations (approval handled in admin.py)."""
    queryset = Registration.objects.all().order_by('-submitted_at')
    serializer_class = RegistrationSerializer


class ChildViewSet(viewsets.ModelViewSet):
    """Admin: CRUD for children."""
    queryset = Child.objects.all()
    serializer_class = ChildSerializer

    def get_serializer_context(self):
        return {"request": self.request}


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

            # ✅ Confirmation email (no credentials here)
            subject = 'HopeNest Registration Received'
            from_email = settings.EMAIL_HOST_USER
            text_content = f"Dear {greeting_names},\n\nThank you for registering with HopeNest. Your application has been received and is under review."
            html_content = f"<p>Dear <strong>{greeting_names}</strong>,</p><p>Thank you for registering with HopeNest. Your application has been received and is under review.</p>"

            email = EmailMultiAlternatives(subject, text_content, from_email, recipient_emails)
            email.attach_alternative(html_content, "text/html")
            email.send()

            return Response({"message": "Registration submitted successfully"}, status=201)

        return Response(serializer.errors, status=400)


# views.py
class LoginView(APIView):
    def post(self, request, *args, **kwargs):
        try:
            print("📥 Login request data:", request.data)
            username = request.data.get("username")
            password = request.data.get("password")

            if not username or not password:
                print("❌ Missing username/password")
                return Response(
                    {"detail": "Both username and password are required."},
                    status=400
                )

            user = authenticate(username=username, password=password)
            print("🔍 Authenticated user:", user)

            if user is None:
                return Response(
                    {"detail": "Invalid username or password."},
                    status=401
                )

            # ⚡ Wrap token in try/except so it never kills response
            try:
                from rest_framework.authtoken.models import Token
                token, created = Token.objects.get_or_create(user=user)
                print("🔑 Token generated:", token.key)
                token_key = token.key
            except Exception as e:
                print("💥 Token error:", e)
                token_key = None

            # ⚡ Registration lookup (force str since user_id is CharField)
            reg = None
            try:
                reg = Registration.objects.filter(user_id=user.id).first()
                print("📄 Matched Registration:", reg)
            except Exception as e:
                print("💥 Registration fetch error:", e)

            # ✅ Decide what to send back
            if reg:
                full_name = reg.father_name or reg.mother_name or user.username
                email = reg.father_email or reg.mother_email or user.email
                phone = reg.father_phone or reg.mother_phone or None
                address = reg.address
            else:
                full_name = f"{user.first_name} {user.last_name}".strip() or user.username
                email = user.email
                phone = None
                address = None

            print("✅ Returning success response")
            return Response({
                "message": "Login successful",
                "token": token_key,
                "user_id": user.id,
                "username": user.username,
                "full_name": full_name,
                "email": email,
                "phone": phone,
                "address": address,
            }, status=200)

        except Exception as e:
            print("🔥 Unexpected error in LoginView:", e)
            return Response({"detail": f"Login failed: {e}"}, status=500)


class ChildListView(generics.ListAPIView):
    """Public: List children available for adoption."""
    queryset = Child.objects.all()
    serializer_class = ChildSerializer

    def get_serializer_context(self):
        return {"request": self.request}


# ---------------------- ADOPTION APPLICATION ----------------------
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def adoption_application_view(request):
    """Submit an adoption application with real parent details."""
    child_id = request.data.get("child")
    if not child_id:
        return Response({"error": "Child ID is required."}, status=400)

    user_obj = request.user
    child_obj = get_object_or_404(Child, pk=child_id)

    # 🔎 Try to fetch linked Registration
    reg = Registration.objects.filter(user_id=user_obj.id).first()

    data = request.data.copy()
    data["user"] = user_obj.id
    data["child"] = child_obj.id


    if reg:
        parents = []
        if reg.father_name:
            parents.append(reg.father_name)
        if reg.mother_name:
            parents.append(reg.mother_name)
        # ✅ Prefer parent details from Registration
        data["full_name"] = reg.father_name or reg.mother_name
        data["email"] = reg.father_email or reg.mother_email
        data["phone"] = reg.father_phone or reg.mother_phone
        data["address"] = reg.address
    else:
        # fallback to User object
        full_name = f"{user_obj.first_name} {user_obj.last_name}".strip()
        data["full_name"] = full_name if full_name else user_obj.username
        data["email"] = user_obj.email or f"{user_obj.username}@hopesnest.local"
        data["phone"] = getattr(user_obj, "phone", "N/A")
        data["address"] = getattr(user_obj, "address", "N/A")

    reg = getattr(user_obj, "registration", None)
    if not reg:
        return Response({"error": "Your account is not linked to a registration. Please contact admin."}, status=400)

    serializer = AdoptionApplicationSerializer(data=data)
    if serializer.is_valid():
        serializer.save(user=user_obj, child=child_obj)

        # mark child as pending
        child_obj.status = "Pending"
        child_obj.save()

        return Response({"message": "Application submitted successfully"}, status=201)

    return Response(serializer.errors, status=400)