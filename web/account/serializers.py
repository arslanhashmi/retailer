from rest_framework import serializers

from web.account.models import User


class UserSerializer(serializers.ModelSerializer):
    token = serializers.SerializerMethodField(source='get_token', read_only=True)

    class Meta:
        model = User
        fields = (
            'id', 'email', 'is_active', 'is_superuser', 'token',
        )

    # noinspection PyMethodMayBeStatic
    def get_token(self, user):
        return user.auth_token.key if hasattr(user, 'auth_token') else ''
