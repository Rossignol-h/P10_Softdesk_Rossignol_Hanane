from django.contrib.auth.password_validation import validate_password
from rest_framework.validators import UniqueValidator
from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()


class RegisterSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email', 'password']
        extra_kwargs = {
                'first_name': {'required': True},
                'last_name': {'required': True},
                'email': {'required': True,
                          'validators': [UniqueValidator
                                         (queryset=User.objects.all(), message="cet email exist deja")]},
                'password': {'required': True, 'write_only': True,
                             'validators': [validate_password]}}

    def create(self, validated_data):
        return User.objects.create_user(
            validated_data["username"],
            password=validated_data["password"],
            first_name=validated_data["first_name"],
            last_name=validated_data["last_name"],
            email=validated_data["email"]
        )
