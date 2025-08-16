# # backend/views.py
# from django.contrib.auth import authenticate
# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework.authtoken.models import Token
# from rest_framework import status
# from django.contrib.auth.models import User

# class LoginView(APIView):
#     def post(self, request):
#         email = request.data.get('email')
#         password = request.data.get('password')

#         try:
#             user = User.objects.get(email=email)
#         except User.DoesNotExist:
#             return Response({'detail': 'Invalid email'}, status=status.HTTP_400_BAD_REQUEST)

#         user = authenticate(username=user.username, password=password)
#         if user is not None:
#             token, created = Token.objects.get_or_create(user=user)
#             return Response({'token': token.key})
#         return Response({'detail': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)
