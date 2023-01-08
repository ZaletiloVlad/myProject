from rest_framework import serializers

from botAPI.models import CustomUser, Space, SpendingCategory, Spending, ReferralCode, SpaceLog, PersonStatus

class PersonStatusSerializer(serializers.ModelSerializer):

    class Meta:
        model = PersonStatus
        fields = ["user", "space", "grade", "is_banned"]


class UserConnectSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomUser
        fields = ["id", "name", "telegram_id"]


class UserSerializer(serializers.ModelSerializer):
    user_space = PersonStatusSerializer(many=True)

    class Meta:
        model = CustomUser
        fields = ["id", "name", "telegram_id", "user_space"]


class SpendingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Spending
        fields = "__all__"


class SpaceSerializer(serializers.ModelSerializer):
    status = PersonStatusSerializer(many=True)
    space_spending = SpendingSerializer(many=True)

    class Meta:
        model = Space
        fields = ["id", "title", "currency", "status", "space_spending"]


class SpendingCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = SpendingCategory
        fields = "__all__"


class ReferralCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReferralCode
        fields = "__all__"


class SpaceLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = SpaceLog
        fields = "__all__"

