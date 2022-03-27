from .models import PhoneNumber, Account, Message
from rest_framework.serializers import ModelSerializer


class AccountSerializer(ModelSerializer):
    class Meta:
        model = Account
        fields = (
            "id",
            "username",
            "email",
        )


class PhoneNumberSerializer(ModelSerializer):
    account = AccountSerializer(many=True, read_only=True)

    class Meta:
        model = PhoneNumber
        fields = ["number", "account"]


class MessageSerializer(ModelSerializer):
    class Meta:
        model = Message
        fields = "__all__"
