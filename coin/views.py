from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response


# check system available
class HealthCheckApi(APIView):
    def get(self, request):
        return Response(
            {"status": "success", "message": "Ok"}, status=status.HTTP_200_OK
        )
