import time

from rest_framework import viewsets, status
from rest_framework.decorators import api_view, action
from rest_framework.response import Response

from botAPI.models import CustomUser, Space
from botAPI.serializers import UserSerializer, SpaceSerializer, UserConnectSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer

    @action(detail=False, methods=["POST"], url_path="connect", url_name="connect")
    def connect_telegram_account(self, request):
        serializer = UserConnectSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        user, created = CustomUser.objects.get_or_create(telegram_id=data["telegram_id"])
        if created:
            user.name = data["name"]
            user.save()
        return Response(UserConnectSerializer(user).data, status.HTTP_200_OK)

    # @action(detail=False, methods=["POST"], url_path="connect", url_name="connect")
    # def connect_telegram_account(self, request):
    #     serializer = ConnectSerializer(data=request.data)
    #     serializer.is_valid(raise_exception=True)
    #     data = serializer.validated_data
    #     user: CustomUser = authenticate(username=data["username"], password=data["password"])
    #
    #     if user:
    #         user.telegram_id = data["telegram_id"]
    #         user.telegram_payload = data.get("telegram_payload")
    #         user.save()
    #         return Response(ConnectSerializer(user).data, status.HTTP_200_OK)
    #
    #     return Response(status=status.HTTP_404_NOT_FOUND)


class SpaceViewSet(viewsets.ModelViewSet):
    queryset = Space.objects.all()
    serializer_class = SpaceSerializer


# def GetIdView(request, tg_id):
#     user = CustomUser.objects.get(telegram_id=tg_id)
#     id = user.id
#     return Response({tg_id: id})

@api_view(["GET"])
def health_check(request):
    time.sleep(1)
    return Response({"status": "Ok"}, status.HTTP_200_OK)