import time

from rest_framework import viewsets, status
from rest_framework.decorators import api_view, action
from rest_framework.response import Response

from botAPI.models import CustomUser, Space, SpaceLog, PersonStatus
from botAPI.serializers import UserSerializer, SpaceSerializer, UserConnectSerializer, CreatingSpaceSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer

    @action(detail=False, methods=["POST"], url_path="connect", url_name="connect")
    def connect_telegram_account(self, request):
        serializer = UserConnectSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        user, created = CustomUser.objects.get_or_create(telegram_id=data["telegram_id"])

        if created or user.name != data['name']:
            user.name = data["name"]
            user.save()
            if created:
                SpaceLog.objects.create(user=user, action=f"Добавлен пользователь")
            else:
                SpaceLog.objects.create(user=user, action=f"Иземенено имя пользователя")

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

    @action(detail=False, methods=["POST"], url_path="space_create", url_name="space_create")
    def space_create(self, request):
        user = CustomUser.objects.get(pk=request.data['id'])
        del request.data['id']
        serializer = CreatingSpaceSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        space = Space.objects.create(title=data['title'], currency=data['currency'])
        PersonStatus.objects.create(user=user, space=space, grade='A')
        SpaceLog.objects.create(user=user, action=f"Создан новый SPACE")
        return Response(CreatingSpaceSerializer(space).data, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=["POST"], url_path="get_space", url_name="get_space")
    def grt_space(self, request):
        user = CustomUser.objects.get(pk=request.data['id'])
        del request.data['id']
        print(request.data)
        space = Space.objects.get(titile=request.data)

@api_view(["GET"])
def health_check(request):
    time.sleep(1)
    return Response({"status": "Ok"}, status.HTTP_200_OK)