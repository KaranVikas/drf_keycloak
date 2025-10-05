from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from todo.users.models import User

class UserSerializer(serializers.ModelSerializer[User]):
    class Meta:
        model = User
        fields = ["username", "name", "url"]

        extra_kwargs = {
            "url": {"view_name": "api:user-detail", "lookup_field": "username"},
        }

class UserRegisterationSerializer(serializers.ModelSerializer):
  password = serializers.CharField(
    write_only = True,
    required = True,
    validators=[validate_password],
  )

  password_confirm = serializers.CharField(
    write_only = True,
    required = True,
  )

  email = serializers.EmailField(required=True)

  class Meta:
    model = User
    fields = ("username", "password","password_confirm","email","name")

  def validate(self, attrs):
    if attrs['password'] != attrs['password_confirm']:
      raise serializers.ValidationError({
        "password": "Password fields didn't match"
      })
    return attrs

  def validate_email(self, value):
    if User.objects.filter(email=value).exists():
      raise serializers.ValidationError(
        "A user with this email already exists."
      )
    return value

  def validate_username(self, value):
    if User.objects.filter(username=value).exists():
      raise serializers.ValidationError(
        "A user with this username already exists"
      )
    return value

  def create(self, validated_data):
    validated_data.pop('password_confirm', None)
    user = User.objects.create_user(**validated_data)
    return user
