from rest_framework import serializers

from botAPI.models import CustomUser, Space, SpendingCategory, Spending, ReferralCode, SpaceLog, PersonStatus

class PersonStatusSerializer(serializers.ModelSerializer):
    space = serializers.SlugRelatedField(slug_field='title', read_only=True)
    user = serializers.SlugRelatedField(slug_field='name', read_only=True)

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
        fields = ["id", "category", "user", "currency", "expense", "space"]


class NewSpendingSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(slug_field='title', read_only=True)
    user = serializers.SlugRelatedField(slug_field='name', read_only=True)
    class Meta:
        model = Spending
        fields = ["id", "category", "user", "currency", "expense", "space"]


class SpaceSerializer(serializers.ModelSerializer):
    status = PersonStatusSerializer(many=True)
    space_spending = SpendingSerializer(many=True)

    class Meta:
        model = Space
        fields = ["id", "title", "currency", "status", "space_spending"]


class CreatingSpaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Space
        fields = ["id", "title", "currency"]

class SpendingCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = SpendingCategory
        fields = ["id", "title", "space"]


class ReferralCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReferralCode
        fields = ["id", "code", "expiration_time", "user", "space"]


class SpaceLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = SpaceLog
        fields = "__all__"

