from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth import authenticate, login

from src.iam.models import LibraryUser
from src.iam.serializers import RegistrationSerializer, LoginSerializer, UserProfileSerializer


@api_view(['POST'])
@permission_classes([AllowAny])
def api_user_registration(request):
    serializer = RegistrationSerializer(data=request.data)
    if serializer.is_valid():
        validated_data = serializer.validated_data
        user = User.objects.create_user(
            username=validated_data.get('username'),
            password=validated_data.get('password')
        )

        LibraryUser.objects.create(
            user=user,
            is_student=validated_data.get('role') == 'student',
            is_librarian=validated_data.get('role') == 'librarian'
        )

        token = Token.objects.create(user=user)
        response_data = {
            "token": str(token)
        }

        return Response(response_data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([AllowAny])
def api_user_login(request):
    serializer = LoginSerializer(data=request.data)
    if serializer.is_valid():
        user = authenticate(username=serializer.validated_data.get('username'),
                            password=serializer.validated_data.get('password'))
        if user:
            login(request, user)
            token = Token.objects.get_or_create(user=user)
            return Response({'token': str(token)}, status=status.HTTP_200_OK)
        else:
            return Response({'message': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def api_user_profile(request):
    library_user = LibraryUser.objects.filter(user=request.user).first()
    return Response(UserProfileSerializer(library_user).data, status=status.HTTP_200_OK)
