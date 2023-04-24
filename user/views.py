from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import CustomUser as CustomUserModel
from .serializers import CustomUserSerializers, RegisterNewUserSerializer


class UserApi(APIView):
    # create new user
    def post(self, request):
        serializer = RegisterNewUserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            if serializer.errors.get("username"):
                return Response(serializer.errors, status=status.HTTP_409_CONFLICT)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
